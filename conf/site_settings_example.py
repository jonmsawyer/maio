import os


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '50 random characters'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Application definition

ALLOWED_HOSTS = []

MAIO_INSTALLED_APPS = []

MAIO_MIDDLEWARE = []

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db', 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATIC_URL = '/static/'

MAIO_SETTINGS = {
    # The directory where Maio will store the media and thumbnails.
    'filestore_directory': os.path.join(BASE_DIR, 'filestore'),
    
    # Restrict the importing of an image if that image's width is less than N.
    'images_min_width': 200,
    
    # Restrict the importing of an image if that image's height is less than N.
    'images_min_height': 200,
    
    # Set to 'and' if you want both images_min_* to fail in order to exclude an image.
    # With 'and', if one of the dimensions fail and the other passes, the image will
    # be included. Set to 'or' if you want one of images_min_* to fail in order to
    # exclude an image. With 'or', if one of the dimensions fail, regardless of the
    # other dimension, the image will be excluded from import.
    'images_min_inclusive': 'and',
}

STATICFILES_DIRS = [
    MAIO_SETTINGS['filestore_directory'],
]
