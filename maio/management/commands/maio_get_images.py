import os
import sys
import hashlib
from pprint import pprint

import magic
from PIL import Image

from django.conf import settings
from django.core.management.base import CommandError
import django.db.utils

from maio import lib
from maio.models.File import File
from maio.models.ImageFile import ImageFile

from ._base import MaioBaseCommand


class Command(MaioBaseCommand):
    args = '<None>'
    help = 'Scrapes images in one or more directories.'
    
    def add_arguments(self, parser):
        # Optional arguments
        parser.add_argument('--no-copy', '-nc', action='store_true',
                            help=('Do not copy images to the filestore'))
        # Positional arguments
        parser.add_argument('directory', nargs='+', type=str, metavar='DIRECTORY',
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
        
        directory = kwargs.get('directory', '')
        self.out('Directory is:', directory)
        no_copy = kwargs.get('no_copy')
        self.out('No copy:', no_copy)
        
        if not os.path.isdir(directory[0]):
            self.out('"{}" is not a valid directory.'.format(directory))
            self.out('')
            exit(1)
        
        mime = magic.Magic(mime=True)
        
        for root, subdirs, files in os.walk(directory[0]):
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
                
                if not is_image(mimetype):
                    self.out('{} is not a valid image type... (it might be a symlink?)'
                             .format(file_path))
                    continue
                
                # get file extension
                filename_ext = lib.MIMETYPE_EXTENSION['image'].get(mimetype)[0]
                if filename_ext is None:
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
                
                # process image
                if no_copy is False:
                    img_dir = mk_md5_dir(md5, settings.MAIO_SETTINGS['images_directory'])
                    img = os.path.join(img_dir, md5 + lib.MIMETYPE_EXTENSION['image'][mimetype][0])
                    if not os.path.isfile(img):
                        im.save(img)
                    file_path = img
                
                # process thumbnail
                thumb_dir = mk_md5_dir(md5, settings.MAIO_SETTINGS['thumbnail_directory'])
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
                
                self.out(md5sum.hexdigest(), mimetype, filename, file_path)
                
                # save file information to the database
                try:
                    thumb_uri = thumb.replace(BASE_DIR, '').replace(os.sep, '/')
                    file_uri = file_path.replace(BASE_DIR, '').replace(os.sep, '/')
                    file_path_md5sum = hashlib.md5()
                    file_path_md5sum.update(file_path.encode('utf-8'))
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
                    
                    f = File(**{
                             'media_class': 'image',
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
                    fn = ImageFile(**{
                                   'file': f,
                                   'name': name,
                                   'extension': extension,
                                   'mtime': sfile.st_mtime,
                                   'width': width,
                                   'height': height,
                                   'comments': comments
                                   })
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
