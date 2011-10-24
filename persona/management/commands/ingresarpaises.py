# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand

import csv
from persona.models import Pais


class Command(BaseCommand):

    def handle(self, **kwargs):
        
        paises = csv.reader(open('paises.csv'))
        for pais in paises:
            print "Adding {0}".format(pais[0])
            country = Pais()
            country.nombre = pais[0]
            country.order = pais[1]
            country.save()
