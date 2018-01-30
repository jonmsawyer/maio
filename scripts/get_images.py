#!/usr/bin/env python
import os
import sys
import hashlib

os.environ['DJANGO_SETTINGS_MODULE'] = 'maio.settings'
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.insert(0, BASE_DIR)

import magic
from PIL import Image

from django.conf import settings
import django
django.setup()

from maio_core.models import File

MAIO_SETTINGS = settings.MAIO_SETTINGS

mimetype_extension = {
    'image': {
        'image/gif': '.gif',
        'image/jpeg': '.jpg',
        'image/pjpeg': '.jpg',
        'image/png': '.png',
        'image/svg+xml': '.svg',
        'image/tiff': '.tiff',
        'image/bmp': '.bmp',
        'image/x-windows-bmp': '.bmp',
        'image/x-tiff': '.tiff',
    }
}

def usage():
    print("Usage:")
    print("")
    print("%s DIR" % (sys.argv[0],))
    print("")
    print("    DIR")
    print("    The directory to recursively walk for images to store in the database.")
    print("")

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
    for key, value in mimetype_extension['image'].items():
        if mimetype == key:
            return True
    return False

if len(sys.argv) == 1:
    print("Please provide a directory to recursively walk for pictures.")
    print("")
    usage()
    exit(1)

directory = sys.argv[1]

if not os.path.isdir(directory):
    print("\"%s\" is not a valid directory." % (directory,))
    print("")
    usage()
    exit(1)

mime = magic.Magic(mime=True)

for root, subdirs, files in os.walk(directory):
    for filename in files:
        try:
            file_path = os.path.join(root, filename)#.decode('utf-8')
        except UnicodeDecodeError as e:
            if "'utf8' codec can't decode bytes" in str(e):
                print("Error processing %s, unreadable file name ..." % (os.path.join(root, filename),))
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
                print('file %s does not exist' % (file_path,))
                continue
            else:
                raise
        except UnicodeDecodeError as e:
            print("File: ", file_path)
            raise
        except:
            raise

        if not is_image(mimetype):
            print('%s is not a valid image type... (it might be a symlink?)' % (file_path,))
            continue

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
            if im.mode != "RGB":
                im = im.convert("RGB")
        except IOError as e:
            print('Error in processing %s ...' % (file_path,), end='')
            if 'truncated' in str(e):
                print('truncated')
                truncated = True
                pass
            elif 'cannot identify image file' in str(e):
                print('invalid image file')
                continue
            elif 'No such file or directory' in str(e):
                print('no such file or directory')
                continue
            else:
                raise

        # get md5sum
        md5sum = hashlib.md5()
        with open(file_path, 'rb') as fh:
            md5sum.update(fh.read())
        md5 = md5sum.hexdigest()

        # process thumbnail
        thumb_dir = mk_md5_dir(md5, settings.MAIO_SETTINGS['thumbnail_directory'])
        thumb = os.path.join(thumb_dir,
                             md5 + '.jpg')
        if not os.path.isfile(thumb):
            im.thumbnail((128, 128), Image.ANTIALIAS)
            im.save(thumb)

        print(md5sum.hexdigest(), mimetype, file_path)

        # save file information to the database
        try:
            file_path_hash = hashlib.md5()
            file_path_hash.update(file_path.encode('utf-8'))
            fph = file_path_hash.hexdigest()

            f = File(mime_type=mimetype, size=sfile.st_size, mtime=sfile.st_mtime,
                     md5sum=md5, tn_path=thumb, file_path=file_path, file_path_hash=fph)
            f.save()
        except django.db.utils.IntegrityError:
            f = File.objects.get(file_path_hash=fph)
            if sfile.st_mtime == f.mtime:
                print("Already in database and up-to-date, skipping %s ..." % (file_path,))
                continue
            f.mime_type = mimetype
            f.size = sfile.st_size
            f.mtime = sfile.st_mtime
            f.md5sum = md5
            f.tn_path = thumb
            f.save()
        except:
            raise