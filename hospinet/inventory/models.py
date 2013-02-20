# -*- coding: utf-8 -*-
# Copyright (C) 2011-2013 Carlos Flores <cafg10@gmail.com>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library. If not, see <http://www.gnu.org/licenses/>.

import datetime
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django_extensions.db.models import TimeStampedModel

class Localidad(models.Model):

    """Representa un lugar físico"""

    name = models.CharField(max_length=255)

    def __unicode__(self):

        return self.name

class Inventario(models.Model):

    localidad = models.ForeignKey('localidad', null=True, blank=True,
                                 related_name='inventarios')

    def __unicode__(self):

        return u"Inventario de {0}".format(localidad.nombre)
    
class ItemTemplate(TimeStampedModel):

    """"""

    descripcion = models.CharField(max_length=255)
    marca = models.CharField(max_length=32, null=True, blank=True)
    modelo = models.CharField(max_length=32, null=True, blank=True)
    numero_de_parte = models.CharField(max_length=32, null=True, blank=True)
    notas = models.TextField(null=True, blank=True)
    suppliers = models.ManyToManyField("Proveedor", null=True, blank=True,
                                       related_name='plantillas')
    
    def get_absolute_url(self):
        
        """Obtiene la URL absoluta"""
        
        return reverse('inventory-item-template', args=[self.id])

class Proveedor(models.Model):

    name = models.CharField(verbose_name=_(u"descripción"), max_length=255)

    def __unicode__(self):

        return self.name

class Item(TimeStampedModel):

    plantilla = models.ForeignKey('ItemTemplate', related_name='items')
    inventario = models.ForeignKey('Inventario', related_name='items')

class Transferencia(TimeStampedModel):

    origen = models.ForeignKey('Inventario', related_name='salidas')
    destino = models.ForeignKey('Inventario', related_name='entradas')
    tipo_de_transaccion = models.CharField(max_length=1, choices=ESTADOS_CIVILES,
                                           blank=True)
    aplicada = models.BooleanField(default=False)
    item = models.ForeignKey('ItemTemplate', related_name='transferencias')
    cantidad = models.IntegerField()

    def aplicar(self):

        if self.aplicada:

            return

        self.aplicada = True
        self.save()
        # TODO: Add code to find out which one is the correct Item to update

class Requisicion(TimeStampedModel):

    inventario = model.ForeignKey('Inventario', related_name='requisiciones')
    item = models.ForeignKey('ItemTemplate', related_name='transferencias')
    cantidad = models.IntegerField()
    aprobada = models.BooleanField(default=False)
    entregada = models.BooleanField(default=True)

    def entregar(self):

        if self.entregada:

            return

        self.entregada = True
        self.save()
        # TODO: Add code to find out which one is the correct Item to update
