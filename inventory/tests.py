from django.test import TestCase
from inventory.models import Inventario, ItemTemplate


class InventoryTest(TestCase):
    def setUp(self):

        Inventario.objects.create(nombre=u'Principal', puede_comprar=True)
        Inventario.objects.create(nombre=u'Secundario')

        ItemTemplate.objects.create(descripcion=u'Apples')
        ItemTemplate.objects.create(descripcion=u'Pears')
