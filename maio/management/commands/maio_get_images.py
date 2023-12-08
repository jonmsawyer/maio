'''
:File: maio_get_images.py
:Module: ``maio.management.commands.maio_get_images.py``
'''

# pylint:

import os
import sys
import hashlib
from pprint import pprint
from getpass import getpass
from datetime import datetime

import magic
from PIL import Image
import pytz

from django.conf import settings
from django.core.management.base import CommandError
import django.db.utils

from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from maio import lib
from maio.models import File
from maio.models import Media
from maio.models import Tag

from ._base import MaioBaseCommand


class Command(MaioBaseCommand):
    '''
    This class is extended from :mod:`MaioBaseCommand` and is the driver for Maio's
    Django command to ingest images into Maio. Call this command with::
        $ manage.py maio_get_images /path/to/images/dir [options]
    
    For help, and to see other options, issue::
        $ manage.py maio_get_images --help
    '''
    args = '<None>'
    help = 'Scrapes images into Maio in one or more directories.'
    
    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('username', type=str, metavar='USERNAME',
                            help=('Set owner of each file to %(metavar)s'))
        
        parser.add_argument('directories', nargs='+', type=str, metavar='DIRECTORIES',
                            help=('Scrape images from %(metavar)s'))
        
        # Optional arguments
        
        # Tagging
        parser.add_argument('--tag-directories', '-td', action='store_true',
                            help=('Tag the supplied directories for Image Tags. Does not tag '
                                  'subdirectories under the supplied directories.'))
        
        parser.add_argument('--tag-subfolders', '-ts', action='store_true',
                            help=('Tag the subdirectories under the supplied directories. Does '
                                  'not tag the supplied directories.'))
        
        parser.add_argument('--tag-filenames', '-tf', action='store_true',
                            help=('Tag the file names of the files.'))
        
        parser.add_argument('--tag-all', '-ta', action='store_true',
                            help=('Equivalent to options -td -ts -tf.'))
        
        parser.add_argument('--tags', '-t', nargs='*', type=str, metavar='TAG',
                            help=('Tag each image with %(metavar)s.'))
        
        # Meta
        parser.add_argument('--love', '-lv', action='store_true',
                            help=('Mark each image with a "Love" rating.'))
        
        parser.add_argument('--like', '-lk', action='store_true',
                            help=('Mark each image with a "Like" rating.'))
        
        parser.add_argument('--rating', '-r', type=int, metavar='RATING',
                            help=('Rate each image with %(metavar)s. Choices are integers '
                                  'from 0 to 5, inclusive.'))
        
        parser.add_argument('--author', '-a', type=str, metavar='AUTHOR',
                            help=('Set the %(metavar)s for each image.'))
        
        parser.add_argument('--url', '-u', type=str, metavar='URL',
                            help=('Set the %(metavar)s for each image.'))
        
        parser.add_argument('--source', '-s', type=str, metavar='SOURCE',
                            help=('Set the %(metavar)s for each image.'))
        
        parser.add_argument('--copyright', '-cr', type=str, metavar='COPYRIGHT',
                            help=('Set the %(metavar)s for each image.'))
        
        parser.add_argument('--comment', '-co', type=str, metavar='COMMENT',
                            help=('Set the %(metavar)s for each image.'))
        
        parser.add_argument('--set-inactive', '-si', action='store_true',
                            help=('By default, all images are set to an active state. '
                                  'Use this flag to set each image as inactive.'))
        
        parser.add_argument('--set-hidden', '-sh', action='store_true',
                            help=('By default, all images are not hidden. '
                                  'Use this flag to set each image as hidden.'))
        
        parser.add_argument('--set-deleted', '-sd', action='store_true',
                            help=('By default, all images are not delete. '
                                  'Use this flag to set each image as deleted.'))
    
    def handle(self, *args, **kwargs):
        # shortcut settings
        MAIO_SETTINGS = settings.MAIO_SETTINGS
        TIME_ZONE = settings.TIME_ZONE
        TZ = pytz.timezone(TIME_ZONE)
        
        def mk_md5_dir(md5, root):
            '''
            Make MD5 directory. Makes 3 directories under ``root``, where the first 2 characters
            in ``md5`` make up the first directory, the next 2 characters make up the second
            directory, and the next 2 characters make up the third directory.
            
            :returns: (str) The path to final directory structure.
            '''
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
            '''
            Check to see if the supplied ``mimetype`` is an image, according to
            ``lib.MIMETYPE_EXTENSION``.
            
            :returns: (bool) True if ``mimetype`` is an image, False otherwise.
            '''
            for key, value in lib.MIMETYPE_EXTENSION['image'].items():
                if mimetype == key:
                    return True
            return False
        
        # grab the username from the options
        username = kwargs.get('username')
        
        # tag flag options
        tag_directories = kwargs.get('tag_directories')
        tag_subfolders = kwargs.get('tag_subfolders')
        tag_filenames = kwargs.get('tag_filenames')
        tag_all = kwargs.get('tag_all')
        tags_input = kwargs.get('tags')
        is_loved = kwargs.get('love')
        is_liked = kwargs.get('like')
        rating = kwargs.get('rating')
        author = kwargs.get('author')
        url = kwargs.get('url')
        source = kwargs.get('source')
        copyright = kwargs.get('copyright')
        comment = kwargs.get('comment')
        set_inactive = kwargs.get('set_inactive')
        set_hidden = kwargs.get('set_hidden')
        set_deleted = kwargs.get('set_deleted')
        
        if set_inactive:
            is_active = False
        else:
            is_active = True
        if set_hidden:
            is_hidden = True
        else:
            is_hidden = False
        if set_deleted:
            is_deleted = True
        else:
            is_deleted = False
        kwargs.update({'is_active': is_active,
                       'is_hidden': is_hidden,
                       'is_deleted': is_deleted})
        
        if not rating:
            rating = 0
        
        if tags_input is None:
            tags_input = []
        
        # validate user
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            self.out('User {} does not exist.'.format(username))
            self.out('')
            exit(1)
        
        # grab the directories to scrape images from
        directories = kwargs.get('directories', [])
        
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
                    # read and join the file path
                    try:
                        file_path = os.path.join(root, filename)
                    except UnicodeDecodeError as e:
                        if "'utf8' codec can't decode bytes" in str(e):
                            self.out('Error processing {}, unreadable file name ...'
                                     .format(os.path.join(root, filename)))
                            continue
                        raise
                    except:
                        raise
                    
                    self.out('For file: {}'.format(file_path))
                    
                    # get mime type
                    try:
                        mimetype = mime.from_file(file_path)
                    except IOError as e:
                        if 'File does not exist' in str(e):
                            self.out('file {} does not exist'.format(file_path))
                            continue
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
                            filename_ext = file_path.split('.')[-1]
                        except IndexError:
                            filename_ext = ''
                    else:
                        filename_ext = filename_ext.replace('.', '')
                    
                    # get name of file
                    name_of_file = file_path.split(os.sep)[-1].split('.')[:-1][0]
                    
                    # stat file
                    sfile = os.stat(file_path)
                    
                    # obtain modified datetime
                    mtime = TZ.localize(datetime.fromtimestamp(sfile.st_mtime))
                    
                    # open image and check to make sure its width and height values
                    # are within configured constraints
                    try:
                        im = Image.open(file_path)
                        
                        # this next if/elif statement looks backwards, but it's not.
                        
                        # we want to continue onto the next image if the user chooses
                        # 'and' and the image's x 'or' y are out of range.
                        if MAIO_SETTINGS.get('images_min_inclusive', 'and').lower() == 'and':
                            if im.size[0] < MAIO_SETTINGS.get('images_min_width', 200) or \
                               im.size[1] < MAIO_SETTINGS.get('images_min_height', 200):
                                    continue
                        # we want to continue onto the next image if the user chooses
                        # 'or' and the image's x 'and' y are both out of range.
                        elif MAIO_SETTINGS.get('images_min_inclusive', 'and').lower() == 'or':
                            if im.size[0] < MAIO_SETTINGS.get('images_min_width', 200) and \
                               im.size[1] < MAIO_SETTINGS.get('images_min_height', 200):
                                    continue
                        im.load()
                        if im.mode != 'RGB':
                            im = im.convert('RGB')
                    except IOError as e:
                        self.out('Error in processing {} ...'.format(file_path))
                        if 'truncated' in str(e):
                            self.out('truncated')
                            continue
                        elif 'cannot identify image file' in str(e):
                            self.out('invalid image file')
                            continue
                        elif 'No such file or directory' in str(e):
                            self.out('no such file or directory')
                            continue
                        else:
                            raise
                    
                    # get md5sum hash of the image
                    md5sum = hashlib.md5()
                    with open(file_path, 'rb') as fh:
                        md5sum.update(fh.read())
                    md5 = md5sum.hexdigest()
                    
                    # make filestore directories if they don't exist                   
                    if not os.path.isdir(MAIO_SETTINGS['filestore_directory']):
                        # ./filestore
                        os.mkdir(MAIO_SETTINGS['filestore_directory'])
                    if not os.path.isdir(os.path.join(MAIO_SETTINGS['filestore_directory'],
                                                      'media')):
                        # ./filestore/media
                        os.mkdir(os.path.join(MAIO_SETTINGS['filestore_directory'],
                                              'media'))
                    if not os.path.isdir(os.path.join(MAIO_SETTINGS['filestore_directory'],
                                                      'media', 'images')):
                        # ./filestore/media/images
                        os.mkdir(os.path.join(MAIO_SETTINGS['filestore_directory'],
                                              'media', 'images'))
                    if not os.path.isdir(os.path.join(MAIO_SETTINGS['filestore_directory'],
                                                      'thumbnails')):
                        # ./filestore/thumbnails
                        os.mkdir(os.path.join(MAIO_SETTINGS['filestore_directory'],
                                              'thumbnails'))
                    
                    # process and save image to filestore
                    img_dir = mk_md5_dir(md5, os.path.join(MAIO_SETTINGS['filestore_directory'],
                                                           'media', 'images'))
                    img = os.path.join(img_dir, md5+'.'+filename_ext)
                    if not os.path.isfile(img):
                        try:
                            # copy the image to the filestore if it doesn't already exist
                            im.save(img)
                        except TypeError:
                            # TODO: file is probably a gif movie, just skip this sort of error
                            #       and deal with this later
                            continue
                    file_path = img
                    width = im.width
                    height = im.height
                    if comment:
                        comment = comment + '\n\n-----------------\n\n' + str(im.info)
                    else:
                        if str(im.info):
                            comment = str(im.info)
                    
                    # process and save thumbnail to filestore
                    thumb_dir = mk_md5_dir(md5, os.path.join(MAIO_SETTINGS['filestore_directory'],
                                                             'thumbnails'))
                    thumb = os.path.join(thumb_dir, md5+'.jpg')
                    if not os.path.isfile(thumb):
                        im.thumbnail((300, 300), Image.ANTIALIAS)
                        im.save(thumb)
                    tn_width = im.width
                    tn_height = im.height
                    
                    # close image file
                    im.close()
                    
                    # process tag flags
                    tags = [] + tags_input
                    if tag_all or tag_directories:
                        # split up a directory such as
                        #     C:\Users\bob\Pictures
                        # into
                        #     ['C:', 'Users', 'bob', 'Pictures']
                        dir_tags = directory.split(os.sep)
                        
                        # don't include Windows drive letters
                        #     ['C:', 'Users', 'bob', 'Pictures']
                        # into
                        #     ['Users', 'bob', 'Pictures']
                        if ':' in dir_tags[0]:
                            dir_tags = dir_tags[1:]
                        
                        tags.extend(dir_tags)
                    
                    if tag_all or tag_subfolders:
                        # split up a directory such as
                        #     C:\Users\bob\Pictures\foo\bar\baz\beef.jpg
                        # where the supplied directory is
                        #     C:\Users\bob\Pictures
                        # into
                        #     ['foo', 'bar', 'baz', 'beef.jpg']
                        dir_tags = os.path.join(root, filename) \
                                          .replace(directory+os.sep, '') \
                                          .split(os.sep)
                        
                        # don't include the filename for this option
                        #     ['foo', 'bar', 'baz']
                        dir_tags = dir_tags[:-1]
                        
                        tags.extend(dir_tags)
                    
                    if tag_all or tag_filenames:
                        # split up a directory such as
                        #     C:\Users\bob\Pictures\foo\bar\baz\beef.jpg
                        # where the supplied directory is
                        #     C:\Users\bob\Pictures
                        # into
                        #     ['foo', 'bar', 'baz', 'beef.jpg']
                        dir_tags = os.path.join(root, filename) \
                                          .replace(directory+os.sep, '') \
                                          .split(os.sep)
                        
                        # get only the filename for this option
                        #     ['beef.jpg']
                        dir_tags = dir_tags[-1:]
                        
                        # split the filename from the extension
                        #     ['beef', 'jpg']
                        dir_tags = dir_tags[0].split('.')
                        
                        tags.extend(dir_tags)
                    
                    # save file information to the database
                    try:
                        filestore = MAIO_SETTINGS['filestore_directory']
                        thumb_uri = thumb.replace(filestore, '').replace(os.sep, '/')
                        file_uri = file_path.replace(filestore, '').replace(os.sep, '/')
                        
                        self.out(md5sum.hexdigest(), mimetype, filename,
                                 file_path, file_uri, thumb_uri)
                        
                        if filename_ext == '':
                            filename_ext = None
                        
                        f = File(**{'md5sum': md5,
                                    'original_name': name_of_file,
                                    'original_extension': filename_ext,
                                    'mime_type': mimetype,
                                    'size': sfile.st_size,
                                    'mtime': sfile.st_mtime,
                                    'tn_path': thumb_uri,
                                    'file_path': file_uri,
                                    'date_modified': mtime,})
                        f.save()
                    except django.db.utils.IntegrityError:
                        f = File.objects.get(md5sum=md5)
                        if sfile.st_mtime == f.mtime:
                            self.out('Already in database and up-to-date, skipping {}'
                                     .format(file_path))
                            self.out('')
                            continue
                        else:
                            self.out('Already in database and not up-to-date, processing {}'
                                     .format(file_path))
                            f.mtime = sfile.st_mtime
                            f.date_modified = mtime
                            f.save()
                    except:
                        raise
                    
                    media = Media(**{'file': f,
                                     'media_type': 'image',
                                     'owner': user,
                                     'name': name_of_file,
                                     'extension': filename_ext,
                                     'mtime': sfile.st_mtime,
                                     'size': sfile.st_size,
                                     'date_modified': mtime,
                                     'width': width,
                                     'height': height,
                                     'tn_width': tn_width,
                                     'tn_height': tn_height,
                                     'is_loved': is_loved,
                                     'is_liked': is_liked,
                                     'rating': rating,
                                     'author': author,
                                     'url': url,
                                     'source': source,
                                     'copyright': copyright,
                                     'comment': comment,
                                     'is_active': is_active,
                                     'is_hidden': is_hidden,
                                     'is_deleted': is_deleted})
                    media.save()
                    
                    self.out('Tagging tags {} to "{}.{}"'
                             .format(tags, name_of_file, filename_ext))
                    self.out('')
                    
                    # tag the image
                    for tag in tags:
                        # get DB tag if exists, if not create it
                        try:
                            tag = tag.lower()
                            t = Tag.objects.get(name=tag)
                        except Tag.DoesNotExist:
                            t = Tag(name=tag)
                            t.save()
                        
                        # now associate the tag to the image
                        media.tags.add(t)
