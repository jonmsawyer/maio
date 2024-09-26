# Maio: Media All-in-One

Version: development, super-pre-alpha, not-even-ready-for-testing. I am not looking for
contributions at this time, unless you know who you are. But, you are welcome to submit
pull requests. I just reserve the right to politely deny pull requests as this project
is not quite yet ready for public contribution.

## Warning: Maio is under heavy development, the following instructions may no longer apply.

## Installing Maio

Maio is being developed with cross platform support in mind. I've developed Maio in both
the Linux and Windows environments using (PostgreSQL)[https://www.postgresql.org/] and
(MSSQL Server)[https://www.microsoft.com/en-us/sql-server/].

### Create a Maio virtual environment

I like to use `virtualenv` for virtual environments.

`$ pip install virtualenv virtualenvwrapper virtualenvwrapper-win`

`$ mkvirtualenv maio`

After the `maio` virtual environment is created, you'll automatically be in the environment:

`(maio) $`

### Get dependencies

In the global Python environment:

 * Python-Magic: `$ sudo pip install python-magic python-magic-bin` - for mime type calculations

### Install the Requirements

In the virtual environment:

`(maio) $ pip install -r requirements.txt`

### Using MySQL

You will first need a MySQL database server.

Using MySQL as your database:

`(maio) $ pip install MySQL-python`

#### You will also need

 * MySQL if you are going to use MySQL
 * PostgreSQL if you are going to use PostgreSQL
 * Python 3.12+

### Get the Maio source code

```
$ cd /path/to # this will be Maio's base directory
$ git clone https://github.com/jonmsawyer/maio.git
```

### Set up your database

 * Using one of `MySQL`, `PostgreSQL`, `MSSQL` or `SQLite3`: Create the database, user,
   and password for Maio.

### Edit your config

 * Rename `conf/site_settings_example.py` to `conf/site_settings.py`
 * Edit `conf/site_settings.py` and read each configuration parameter carefully
 * Besure to set your `DATABASES` attribute:

```python
DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.postgresql', # or 'mysql', or 'sqlite3'.
    'NAME': 'maio', # Or path to database file if using sqlite3.
    'USER': 'maio',
    'PASSWORD': 'maio', # Change this password
    'HOST': 'localhost',
    'PORT': '',
  }
}
```

Change the to the database driver, username, and password you have set for yourself.
DON'T USE THESE SETTINGS ON A PRODUCTION WEB SERVER!

 * Change the secret key:

```python
SECRET_KEY = '+&-8p_beejspfe!8#b_q&eiw%zw-^_96^h=3gvt7%_^9m$z+=a'
```
   * Hint: use the following Python code to generage a `SECRET_KEY`:
```python
from string import printable
from random import choice
''.join([choice(printable[:-6]) for x in range(50)])
```

Change this to something else. DON'T USE THIS KEY ON A PRODUCTION WEB SERVER!

 * Change the Maio-specific settings:

```python
MAIO_SETTINGS = {
    'thumbnail_directory': os.path.join(BASE_DIR, 'filestore', 'thumbnails'),
    'media_directory': os.path.join(BASE_DIR, 'filestore', 'media'),
    'images_directory': os.path.join(BASE_DIR, 'filestore', 'media', 'images'),
    'images_min_width': 200,
    'images_min_height': 200,
    'images_min_inclusive': 'OR',
}
```

Note: Make sure the webserver or uWSGI process owner has read/write access to the directories
listed in `MAIO_SETTINGS`.

### Sync the database tables

 * Now run a Django command to create Maio's database structure:

```bash
$ cd ~/maio
$ ./manage.py migrate
```

### Get images (audio and video are not supported yet)

```bash
$ cd ~/maio
$ ./scripts/getpics.py ~/Pictures
```

### Run the server

~~~
$ cd ~/maio
$ ./manage.py runserver 8080
~~~

### Run Maio

In your browser, go to http://maio.hostname.local:8080/ and enjoy!

# Notes

Maio requires `FFmpeg`. If you are running windows, use scoop: `scoop install ffmpeg`.
