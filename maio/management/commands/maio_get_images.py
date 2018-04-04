import os
import sys
import hashlib
from pprint import pprint
from getpass import getpass

import magic
from PIL import Image

from django.conf import settings
from django.core.management.base import CommandError
import django.db.utils

from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from maio import lib
from maio.models.File import File
from maio.models.ImageFile import ImageFile

from ._base import MaioBaseCommand


class Command(MaioBaseCommand):
    args = '<None>'
    help = 'Scrapes images in one or more directories.'
    
    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('username', nargs=1, type=str, metavar='USERNAME',
                            help=('Set owner of each file to %(metavar)s'))
        
        parser.add_argument('directories', nargs='+', type=str, metavar='DIRECTORIES',
                            help=('Scrape images from %(metavar)s'))
    
    def handle(self, *args, **kwargs):
        BASE_DIR = settings.BASE_DIR
        MAIO_SETTINGS = settings.MAIO_SETTINGS
        
        def mk_md5_dir(md5, root):
            if len(md5) == 32:
                part1 = md5[0:2]
                part2 = md5[2:4]
                part3 = md5[4:6]
                dirtomake = os.path.join(root, part1, part2, part3)
                if os.path.isdir(dirtomake):
                    return dirtomake
                if os.path.isdir(root):
                    os.makedirs(dirtomake)
                    return dirtomake
        
        def is_image(mimetype):
            for key, value in lib.MIMETYPE_EXTENSION['image'].items():
                if mimetype == key:
                    return True
            return False
        
        # grab the username from the options
        username = kwargs.get('username', [''])[0]
        
        # grab the directories to scrape images from
        directories = kwargs.get('directories', [])
        
        # get the User object from the username
        password = getpass('Password for "{}": '.format(username), self.stdout)
        user = authenticate(username=username, password=password)
        if not user:
            self.out('Could not authenticate user "{}". Please try again.'.format(username))
            self.out('')
            exit(1)
        
        # walk through each directory and make sure each one exists
        for directory in directories:
            if not os.path.isdir(directory):
                self.out('"{}" is not a valid directory.'.format(directory))
                self.out('')
                exit(1)
        
        # set up mime Magic
        mime = magic.Magic(mime=True)
        
        # walk through each directory, scraping images
        for directory in directories:
            # for each directory's files
            for root, subdirs, files in os.walk(directory):
                # for each file
                for filename in files:
                    try:
                        file_path = os.path.join(root, filename)
                    except UnicodeDecodeError as e:
                        if "'utf8' codec can't decode bytes" in str(e):
                            self.out('Error processing {}, unreadable file name ...'
                                     .format(os.path.join(root, filename)))
                            continue
                        else:
                            raise
                    except:
                        raise
                    
                    # get mime type
                    try:
                        mimetype = mime.from_file(file_path)
                    except IOError as e:
                        if 'File does not exist' in str(e):
                            self.out('file {} does not exist'.format(file_path))
                            continue
                        else:
                            raise
                    except UnicodeDecodeError as e:
                        self.out('File: ', file_path)
                        raise
                    except:
                        raise
                    
                    # make sure the mimetype is an image rather than something that looks like
                    # an image
                    if not is_image(mimetype):
                        self.out('{} is not a valid image type... (it might be a symlink?)'
                                 .format(file_path))
                        continue
                    
                    # get file extension
                    filename_ext = lib.MIMETYPE_EXTENSION['image'].get(mimetype, [[]])[0]
                    if filename_ext in (None, [[]]):
                        try:
                            filename_ext = '.' + file_path.split('.')[-1]
                        except IndexError:
                            filename_ext = ''
                    
                    # get name of file
                    name_of_file = file_path.split(os.sep)[-1].replace(filename_ext, '')
                    
                    # stat file
                    sfile = os.stat(file_path)
                    
                    # open image
                    truncated = False
                    try:
                        im = Image.open(file_path)
                        if MAIO_SETTINGS.get('images_min_inclusive', '').lower() == 'and':
                            if im.size[0] < MAIO_SETTINGS.get('images_min_width', 0) or \
                               im.size[1] < MAIO_SETTINGS.get('images_min_height', 0):
                                continue
                        elif MAIO_SETTINGS.get('images_min_inclusive', '').lower() == 'or':
                            if im.size[0] < MAIO_SETTINGS.get('images_min_width', 0) and \
                               im.size[1] < MAIO_SETTINGS.get('images_min_height', 0):
                                continue
                        else:
                            pass
                        im.load()
                        if im.mode != 'RGB':
                            im = im.convert('RGB')
                    except IOError as e:
                        self.out('Error in processing {} ...'.format(file_path))
                        if 'truncated' in str(e):
                            self.out('truncated')
                            truncated = True
                            pass
                        elif 'cannot identify image file' in str(e):
                            self.out('invalid image file')
                            continue
                        elif 'No such file or directory' in str(e):
                            self.out('no such file or directory')
                            continue
                        else:
                            raise
                    
                    # get md5sum
                    md5sum = hashlib.md5()
                    with open(file_path, 'rb') as fh:
                        md5sum.update(fh.read())
                    md5 = md5sum.hexdigest()
                    
                    # make filestore directories if they don't exist
                    if not os.path.isdir(MAIO_SETTINGS['filestore_directory']):
                        os.mkdir(MAIO_SETTINGS['filestore_directory'])
                    
                    if not os.path.isdir(os.path.join(MAIO_SETTINGS['filestore_directory'],
                                                      'media')):
                        os.mkdir(os.path.join(MAIO_SETTINGS['filestore_directory'], 'media'))
                    
                    if not os.path.isdir(os.path.join(MAIO_SETTINGS['filestore_directory'],
                                                      'media', 'images')):
                        os.mkdir(os.path.join(MAIO_SETTINGS['filestore_directory'],
                                              'media', 'images'))
                    
                    if not os.path.isdir(os.path.join(MAIO_SETTINGS['filestore_directory'],
                                                      'thumbnails')):
                        os.mkdir(os.path.join(MAIO_SETTINGS['filestore_directory'], 'thumbnails'))
                    
                    # process image
                    img_dir = mk_md5_dir(md5, os.path.join(MAIO_SETTINGS['filestore_directory'],
                                                           'media', 'images'))
                    img = os.path.join(img_dir, md5 + lib.MIMETYPE_EXTENSION['image'][mimetype][0])
                    if not os.path.isfile(img):
                        im.save(img)
                    file_path = img
                    
                    # process thumbnail
                    thumb_dir = mk_md5_dir(md5, os.path.join(MAIO_SETTINGS['filestore_directory'],
                                                             'thumbnails'))
                    thumb = os.path.join(thumb_dir, md5 + '.jpg')
                    if not os.path.isfile(thumb):
                        im.thumbnail((128, 128), Image.ANTIALIAS)
                        im.save(thumb)
                    
                    # save the width, height, and comments
                    width = im.width
                    height = im.height
                    comments = str(im.info)
                    
                    # close image file
                    im.close()
                    
                    # save file information to the database
                    try:
                        filestore = MAIO_SETTINGS['filestore_directory']
                        thumb_uri = thumb.replace(filestore, '').replace(os.sep, '/')
                        file_uri = file_path.replace(filestore, '').replace(os.sep, '/')
                        file_path_md5sum = hashlib.md5()
                        file_path_md5sum.update(file_uri.encode('UTF-8'))
                        fph = file_path_md5sum.hexdigest()
                        
                        try:
                            name_of_file_parts = name_of_file.split('.')
                            if len(name_of_file_parts) != 1:
                                name = '.'.join(name_of_file_parts[0:-1])
                                extension = name_of_file_parts[-1]
                            else:
                                raise Exception('File must have an extension')
                        except (Exception, IndexError):
                            name = name_of_file
                            extension = None
                    
                        self.out(md5sum.hexdigest(), mimetype, filename,
                                 file_path, file_uri, thumb_uri)
                        self.out('\n')
                        
                        f = File(**{'media_class': 'image',
                                    'name': name,
                                    'extension': extension,
                                    'mime_type': mimetype,
                                    'num_bytes': sfile.st_size,
                                    'mtime': sfile.st_mtime,
                                    'md5sum': md5,
                                    'tn_path': thumb_uri,
                                    'file_path': file_uri,
                                    'file_path_md5sum': fph})
                        f.save()
                        fn = ImageFile(**{'file': f,
                                          'owner': user,
                                          'name': name,
                                          'extension': extension,
                                          'mtime': sfile.st_mtime,
                                          'width': width,
                                          'height': height,
                                          'comments': comments})
                        fn.save()
                    except django.db.utils.IntegrityError:
                        f = File.objects.get(file_path_md5sum=fph)
                        if sfile.st_mtime == f.mtime:
                            self.out('Already in database and up-to-date, skipping {} ...'
                                     .format(file_path))
                            continue
                        f.mime_type = mimetype
                        f.size = sfile.st_size
                        f.mtime = sfile.st_mtime
                        f.md5sum = md5
                        f.tn_path = thumb
                        f.save()
                    except:
                        raise
