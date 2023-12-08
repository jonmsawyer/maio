'''
File: site_settings_example.py

Module: ``maio.conf.site_settings_example``

Copy and rename this file to ``site_settings.py`` to configure local site settings.
'''

import os
from pathlib import Path


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Execute the lines below in a Python shell to generate your secret key.
# >>> from random import choice
# >>> from string import printable
# >>> ''.join([choice(printable[:-6]) for _ in range(66)])
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '66 character secret key'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Application definition

ALLOWED_HOSTS = ['localhost']

# DATABASES
# A dictionary containing the settings for all databases to be used with Django. It is a nested
# dictionary whose contents map a database alias to a dictionary containing the options for an
# individual database. The DATABASES setting must configure a default database; any number of
# additional databases may also be specified.
DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': 'maio',
        'HOST': r'HOSTNAME\SQLEXPRESS',
        #'PORT': '1433',
        'USER': 'maio',
        'PASSWORD': '*********',
        'OPTIONS': {
            # driver
            # String. ODBC Driver to use ("ODBC Driver 17 for SQL Server" etc). See
            # http://msdn.microsoft.com/en-us/library/ms130892.aspx. Default is "SQL Server" on
            # Windows and "FreeTDS" on other platforms.
            'driver': 'ODBC Driver 17 for SQL Server',

            # isolation_level
            'isolation_level': 'READ UNCOMMITTED',

            # unicode_results
            'unicode_results': True,
        },
        'AUTOCOMMIT': True,
        'ATOMIC_REQUESTS': True,
        'Trusted_Connection': True,
    },
}

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Maio specific settings

MAIO_SETTINGS = {
    'filestore_directory': os.path.join(BASE_DIR, 'filestore'),
    'images_min_width': 200,
    'images_min_height': 200,
    'images_min_inclusive': 'OR',
}
