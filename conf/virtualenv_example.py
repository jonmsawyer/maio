'''
File: virtualenv_example.py

Module: ``conf.virtualenv_example``

Python Virtual Environment settings.

Requires ``virtualenvwrapper-win``::

    D:\\> pip install virtualenv virtualenvwrapper virtualenvwrapper-win
    D:\\> mkvirtualenv <the name>

Copy and rename this file from to ``virtualenv.py`` and change the settings below.
'''

#: Set this to be the directory path to the root of your virtualenv
#: ``WORKON_HOME`` environment variable folder. Usually this will be
#: ``D:/PythonVirtualEnvironments``.
#:
#: .. note::
#:
#:     Use forward slashes in the :data:`PATH` value, even on Windows.
#:
#: Default::
#:
#:     path = 'D:/PythonVirtualEnvironments'
path = 'D:/PythonVirtualEnvironments'

#: The name of the virtualenv to use. To list the available virtualenv's,
#: execute::
#:
#:     D:\> lsvirtualenv
#:
#: Default::
#:
#:     name = 'MyVirtualEnv'
name = 'maio_dev'
