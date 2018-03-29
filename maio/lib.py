'''
File: lib.py

Module: ``maio.lib``
'''

# pylint:

from collections import OrderedDict


MIMETYPE_EXTENSION = {
    'image': OrderedDict([
        # GIF
        ('image/gif', ('.gif',)),
        ('image/gi_', ('.gif',)),
        
        # JPG
        ('image/jpeg', ('.jpg', '.jpeg')),
        ('image/pjpeg', ('.pjpg', '.pjpeg')),
        ('image/jpg', ('.jpg', '.jpeg')),
        ('image/jp_', ('.jpg', '.jpeg')),
        ('application/jpg', ('.jpg', '.jpeg')),
        ('application/x-jpg', ('.jpg', '.jpeg')),
        ('image/pipeg', ('.jpg', '.jpeg')),
        ('image/vnd.swiftview-jpeg', ('.jpg', '.jpeg')),
        
        # JPEG 2000
        ('image/jp2', ('.jp2', '.j2k', '.jpf')),
        ('image/jpx', ('.jpx',)),
        ('image/jpm', ('.jpm',)),
        
        # PNG
        ('image/png', ('.png',)),
        
        # TIFF
        ('image/tiff', ('.tiff', '.tif')),
        ('image/x-tiff', ('.tiff', '.tif')),
        ('image/tif', ('.tif', '.tiff')),
        ('image/x-tif', ('.tif', '.tiff')),
        ('application/tif', ('.tif', '.tiff')),
        ('application/x-tif', ('.tif', '.tiff')),
        ('application/tiff', ('.tiff', '.tif')),
        ('application/x-tiff', ('.tiff', '.tif')),
        
        # BMP
        ('image/bmp', ('.bmp',)),
        ('image/x-windows-bmp', ('.bmp',)),
        
        # PCX
        ('image/vnd.zbrush.pcx', ('.pcx',)),
        ('image/x-pcx', ('.pcx',)),
        ('application/pcx', ('.pcx',)),
        ('application/x-pcx', ('.pcx',)),
        ('image/pcx', ('.pcx',)),
        ('image/x-pc-paintbrush', ('.pcx',)),
        ('image/x-pcx', ('.pcx',)),
        ('zz-application/zz-winassoc-pcx', ('.pcx',)),
        
        # PPM
        ('image/x-portable-pixmap', ('.ppm', '.pbm', '.pgm', '.pnm')),
        ('image/x-portable-bitmap', ('.pbm', '.ppm', '.pgm', '.pnm')),
        ('image/x-portable-graymap', ('.pgm', '.ppm', '.pbm', '.pnm')),
        ('image/x-portable-anymap', ('.pnm', '.ppm', '.pbm', '.pgm')),
        ('application/ppm', ('.ppm', '.pbm', '.pgm', '.pnm')),
        ('application/x-ppm', ('.ppm', '.pbm', '.pgm', '.pnm')),
        ('image/x-p', ('.ppm', '.pbm', '.pgm', '.pnm')),
        ('image/x-ppm', ('.ppm', '.pbm', '.pgm', '.pnm')),
        
        # WEBP
        ('image/webp', ('.webp',)),
        
        # PPM
        ('image/x-portable-bitmap', ('.ppm', '.pbm', '.pgm', '.pnm')),
        ('image/x-portable-graymap', ('.ppm', '.pbm', '.pgm', '.pnm')),
        ('image/x-portable-pixmap', ('.ppm', '.pbm', '.pgm', '.pnm')),
        ('image/x-portable-anymap', ('.ppm', '.pbm', '.pgm', '.pnm')),
        
        #XBM
        ('image/x-xbitmap', ('.xbm',)),
        ('image/xbm', ('.xbm',)),
    ]),
}
