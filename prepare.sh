#!/usr/bin/env sh
python manage.py syncdb
python manage.py createcachetable cache
python manage.py rebuild_index
python manage.py migrate spital