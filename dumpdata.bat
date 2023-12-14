rem Backup development data.
py manage.py dumpdata --format json --indent 4 -o .fixtures/0003_admin.json admin
py manage.py dumpdata --format json --indent 4 -o .fixtures/0012_auth.json auth
py manage.py dumpdata --format json --indent 4 -o .fixtures/0002_contenttypes.json contenttypes
py manage.py dumpdata --format json --indent 4 -o .fixtures/0002_maio.json maio
py manage.py dumpdata --format json --indent 4 -o .fixtures/0001_sessions.json sessions
rem Backup all data.
py manage.py dumpdata --format json --indent 4 --natural-foreign --natural-primary -o .fixtures/all.json
