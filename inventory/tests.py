from __future__ import unicode_literals
from django.test import TestCase
from inventory.models import Inventario, ItemTemplate


class InventoryTest(TestCase):
    def setUp(self):

        Inventario.objects.create(nombre='Principal', puede_comprar=True)
        Inventario.objects.create(nombre='Secundario')

        ItemTemplate.objects.create(descripcion='Apples')
        ItemTemplate.objects.create(descripcion='Pears')
