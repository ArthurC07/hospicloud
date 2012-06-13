#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file has been automatically generated, changes may be lost if you
# go and generate it again. It was generated with the following command:
# manage.py dumpscript

import datetime
from decimal import Decimal
from django.contrib.contenttypes.models import ContentType

def run():

    from treemenus.models import Menu

    treemenus_menu_1 = Menu()
    treemenus_menu_1.name = u'root'
    treemenus_menu_1.save()

    treemenus_menu_2 = Menu()
    treemenus_menu_2.name = u'persona'
    treemenus_menu_2.save()

    from treemenus.models import MenuItem

    treemenus_menuitem_1 = MenuItem()
    treemenus_menuitem_1.parent = None
    treemenus_menuitem_1.caption = u'root'
    treemenus_menuitem_1.url = u''
    treemenus_menuitem_1.named_url = u''
    treemenus_menuitem_1.level = 0
    treemenus_menuitem_1.rank = 0
    treemenus_menuitem_1.menu = treemenus_menu_1
    treemenus_menuitem_1.save()

    treemenus_menuitem_2 = MenuItem()
    treemenus_menuitem_2.parent = None
    treemenus_menuitem_2.caption = u'root'
    treemenus_menuitem_2.url = u''
    treemenus_menuitem_2.named_url = u''
    treemenus_menuitem_2.level = 0
    treemenus_menuitem_2.rank = 0
    treemenus_menuitem_2.menu = treemenus_menu_2
    treemenus_menuitem_2.save()

    treemenus_menuitem_3 = MenuItem()
    treemenus_menuitem_3.parent = treemenus_menuitem_1
    treemenus_menuitem_3.caption = u'Enfermer\xeda'
    treemenus_menuitem_3.url = u''
    treemenus_menuitem_3.named_url = u'nightingale-index'
    treemenus_menuitem_3.level = 1
    treemenus_menuitem_3.rank = 4
    treemenus_menuitem_3.menu = treemenus_menu_1
    treemenus_menuitem_3.save()

    treemenus_menuitem_4 = MenuItem()
    treemenus_menuitem_4.parent = treemenus_menuitem_1
    treemenus_menuitem_4.caption = u'Admisiones'
    treemenus_menuitem_4.url = u''
    treemenus_menuitem_4.named_url = u'admision-index '
    treemenus_menuitem_4.level = 1
    treemenus_menuitem_4.rank = 3
    treemenus_menuitem_4.menu = treemenus_menu_1
    treemenus_menuitem_4.save()

    treemenus_menuitem_5 = MenuItem()
    treemenus_menuitem_5.parent = treemenus_menuitem_1
    treemenus_menuitem_5.caption = u'Examenes'
    treemenus_menuitem_5.url = u''
    treemenus_menuitem_5.named_url = u'examen-index '
    treemenus_menuitem_5.level = 1
    treemenus_menuitem_5.rank = 2
    treemenus_menuitem_5.menu = treemenus_menu_1
    treemenus_menuitem_5.save()

    treemenus_menuitem_6 = MenuItem()
    treemenus_menuitem_6.parent = treemenus_menuitem_1
    treemenus_menuitem_6.caption = u'Inicio'
    treemenus_menuitem_6.url = u''
    treemenus_menuitem_6.named_url = u'home'
    treemenus_menuitem_6.level = 1
    treemenus_menuitem_6.rank = 0
    treemenus_menuitem_6.menu = treemenus_menu_1
    treemenus_menuitem_6.save()

    treemenus_menuitem_7 = MenuItem()
    treemenus_menuitem_7.parent = treemenus_menuitem_1
    treemenus_menuitem_7.caption = u'Pacientes'
    treemenus_menuitem_7.url = u''
    treemenus_menuitem_7.named_url = u'persona-index'
    treemenus_menuitem_7.level = 1
    treemenus_menuitem_7.rank = 1
    treemenus_menuitem_7.menu = treemenus_menu_1
    treemenus_menuitem_7.save()

    treemenus_menuitem_8 = MenuItem()
    treemenus_menuitem_8.parent = treemenus_menuitem_1
    treemenus_menuitem_8.caption = u'B\xfasqueda'
    treemenus_menuitem_8.url = u''
    treemenus_menuitem_8.named_url = u'haystack_search'
    treemenus_menuitem_8.level = 1
    treemenus_menuitem_8.rank = 5
    treemenus_menuitem_8.menu = treemenus_menu_1
    treemenus_menuitem_8.save()

    treemenus_menuitem_9 = MenuItem()
    treemenus_menuitem_9.parent = treemenus_menuitem_2
    treemenus_menuitem_9.caption = u'Agregar Examen'
    treemenus_menuitem_9.url = u''
    treemenus_menuitem_9.named_url = u'examen-agregar persona.id'
    treemenus_menuitem_9.level = 1
    treemenus_menuitem_9.rank = 0
    treemenus_menuitem_9.menu = treemenus_menu_2
    treemenus_menuitem_9.save()

    treemenus_menuitem_10 = MenuItem()
    treemenus_menuitem_10.parent = treemenus_menuitem_2
    treemenus_menuitem_10.caption = u'Ver Datos Personales'
    treemenus_menuitem_10.url = u''
    treemenus_menuitem_10.named_url = u'persona-view-id persona.id'
    treemenus_menuitem_10.level = 1
    treemenus_menuitem_10.rank = 1
    treemenus_menuitem_10.menu = treemenus_menu_2
    treemenus_menuitem_10.save()

    treemenus_menuitem_11 = MenuItem()
    treemenus_menuitem_11.parent = treemenus_menuitem_2
    treemenus_menuitem_11.caption = u'Examenes'
    treemenus_menuitem_11.url = u''
    treemenus_menuitem_11.named_url = u'examen-persona-lista persona.id'
    treemenus_menuitem_11.level = 1
    treemenus_menuitem_11.rank = 2
    treemenus_menuitem_11.menu = treemenus_menu_2
    treemenus_menuitem_11.save()

    treemenus_menuitem_12 = MenuItem()
    treemenus_menuitem_12.parent = treemenus_menuitem_2
    treemenus_menuitem_12.caption = u'Admitir Paciente'
    treemenus_menuitem_12.url = u''
    treemenus_menuitem_12.named_url = u'admision-persona-agregar persona.id'
    treemenus_menuitem_12.level = 1
    treemenus_menuitem_12.rank = 3
    treemenus_menuitem_12.menu = treemenus_menu_2
    treemenus_menuitem_12.save()

    treemenus_menu_1.root_item = treemenus_menuitem_1
    treemenus_menu_1.save()

    treemenus_menu_2.root_item = treemenus_menuitem_2
    treemenus_menu_2.save()

