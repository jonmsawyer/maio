"""
WSGI config for maio project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os
import sys
import site

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "maio.settings")
env_path = os.path.dirname(os.path.dirname(__file__))
if env_path not in sys.path:
    sys.path.insert(0, env_path)

from conf import virtualenv

try:
    venv = os.path.join(virtualenv.PATH, virtualenv.NAME)
    activate_this = os.path.join(venv, 'Scripts', 'activate_this.py')
    new_site = os.path.join(venv, 'Lib', 'site-packages')
    if not os.path.isfile(activate_this):
        raise Exception("Invalid Python Virtual Environment `%s'. Please be sure that the "
                        "`%s' virtual environment exists before continuing." % (venv, venv))
except AttributeError as e:
    raise Exception(r"Could not read the attributes of your conf\virtualenv.py module. Please be "
                    "sure that the `path` and `name' attributes are defined and valid.")
except ImportError as e:
    raise Exception(r"Could not import `conf\virtualenv.py module. Please rename "
                    r"`conf\virtualenv.py.example' to `conf\virtualenv.py' and set the `path' and "
                    "`name' attributes for your configuration.")

# Add the site-packages of the chosen virtualenv to work with
site.addsitedir(new_site)

# Activate your virtual env
exec(open(activate_this).read(), dict(__file__=activate_this))

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
