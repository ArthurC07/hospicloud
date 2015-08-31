#!/usr/bin/env sh
python manage.py syncdb
python manage.py createcachetable cache
python manage.py migrate
python manage.py createsuperuser
