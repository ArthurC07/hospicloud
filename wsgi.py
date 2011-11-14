# -*- coding: utf-8 -*-
import os
import sys
program, subplace = os.path.split(os.path.dirname(__file__))
#program, subplace = os.path.split(program)
path = os.path.dirname(__file__)
sys.path.append(program)

if path not in sys.path:
    sys.path.append(path)

import settings

import django.core.management
django.core.management.setup_environ(settings)
utility = django.core.management.ManagementUtility()
command = utility.fetch_command('runserver')

command.validate()

import django.conf
import django.utils

django.utils.translation.activate(django.conf.settings.LANGUAGE_CODE)

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()