#!/usr/bin/env sh
python manage.py syncdb
python manage.py createcachetable cache
python manage.py migrate
python manage.py rebuild_index
chmod 777 whoosh_index
python manage.py createsuperuser
