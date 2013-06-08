# -*- coding: utf-8 -*-
#
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

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django_extensions.db.models import TimeStampedModel
from guardian.models import User

class Inventario(models.Model):

    lugar = models.CharField(max_length=255, default='Bodega')
    puede_comprar = models.NullBooleanField(default=False, blank=True, null=True)
    
    def __unicode__(self):
        
        return u"Inventario de {0}".format(self.nombre)
    
    def buscar_item(self, item_template):
        
        qs = self.items.filter(plantilla=item_template)
        r = list(qs[:1])
        if r:
            return r[0]
        return Item(inventario=self, plantilla=item_template)
    
    def get_absolute_url(self):
        
        """Obtiene la URL absoluta"""
        
        return reverse('inventario', args=[self.id])

class ItemType(TimeStampedModel):
    
    nombre = models.CharField(max_length=255)
    
    def __unicode__(self):
        
        return self.nombre
    
    def get_absolute_url(self):
        
        return reverse('inventario-index')

class ItemTemplate(TimeStampedModel):
    
    """"""
    
    descripcion = models.CharField(max_length=255)
    marca = models.CharField(max_length=32, null=True, blank=True)
    modelo = models.CharField(max_length=32, null=True, blank=True)
    notas = models.TextField(null=True, blank=True)
    suppliers = models.ManyToManyField("Proveedor", null=True, blank=True,
                                       related_name='plantillas')
    precio_de_venta = models.DecimalField(max_digits=10, decimal_places=2,
                                          default=0)
    costo = models.DecimalField(max_digits=10, decimal_places=2,
                                          default=0)
    unidad_de_medida = models.CharField(max_length=32, null=True, blank=True)
    impuestos = models.DecimalField(max_digits=10, decimal_places=2,
                                          default=0)
    activo = models.BooleanField(default=True)
    item_type = models.ManyToManyField(ItemType, related_name='items')
    
    def __unicode__(self):
        
        return self.descripcion
    
    def get_absolute_url(self):
        
        """Obtiene la URL absoluta"""
        
        return reverse('itemtemplate', args=[self.id])

class Proveedor(models.Model):
    
    name = models.CharField(verbose_name=_(u"descripción"), max_length=255)
    
    def __unicode__(self):
        
        return self.name

class Item(TimeStampedModel):
    
    plantilla = models.ForeignKey(ItemTemplate, related_name='items')
    inventario = models.ForeignKey(Inventario, related_name='items')
    cantidad = models.IntegerField(default=0)
    
    def disminuir(self, cantidad):
        
        self.cantidad -= cantidad
        self.save()
    
    def incrementar(self, cantidad):
    
        self.cantidad += cantidad
        self.save()
    
    def __unicode__(self):
        
        return u'{0} en {1}'.format(self.plantilla.descripcion,
                                    self.inventario.lugar)

class Requisicion(TimeStampedModel):
    
    inventario = models.ForeignKey(Inventario, related_name='requisiciones',
                                   null=True, blank=True)
    cantidad = models.IntegerField()
    aprobada = models.BooleanField(default=False)
    entregada = models.BooleanField(default=False)
    usuario = models.ForeignKey(User, related_name="requisiciones",
                                null=True, blank=True)
    
    def __unicode__(self):
        
        return u'Requisición de {0}'.format(self.inventario.lugar)

class ItemRequsicion(TimeStampedModel):
    
    requisicion = models.ForeignKey(Requisicion, related_name='items')
    item = models.ForeignKey(ItemTemplate, related_name='requisiciones')
    cantidad = models.IntegerField()
    entregada = models.BooleanField(default=False)

class Transferencia(TimeStampedModel):
    
    requisicion = models.ForeignKey(Requisicion, related_name='transferencias',
                                    null=True, blank=True)
    origen = models.ForeignKey(Inventario, related_name='salidas',
                               null=True, blank=True)
    destino = models.ForeignKey(Inventario, related_name='entradas',
                                null=True, blank=True)
    aplicada = models.NullBooleanField(default=False, null=True, blank=True)
    usuario = models.ForeignKey(User, related_name="transferencias",
                                null=True, blank=True)
    
    def __unicode__(self):
        
        return u'Transferencia desde {0} hacia {1}'.format(self.origen.lugar,
                                                           self.origen.lugar)

class Transferido(TimeStampedModel):
    
    transferencia = models.ForeignKey(Transferencia,
                                      related_name='transferidos')
    item = models.ForeignKey(ItemTemplate, related_name='transferidos')
    cantidad = models.IntegerField()
    aplicada = models.BooleanField(default=False)
    
    def __unicode__(self):
        
        return u'Transferir {1} {0}'.format(self.item.description,
                                            self.cantidad)

class Compra(TimeStampedModel):
    
    inventario = models.ForeignKey(Inventario, blank=True, null=True,
                                   related_name='compras')
    ingresada = models.BooleanField(default=False)
    proveedor = models.CharField(max_length=255, blank=True, null=True)
    
    def __unicode__(self):
        
        return u"Compra efectuada el {0}".format(self.created)

class ItemComprado(TimeStampedModel):
    
    compra = models.ForeignKey(Compra, related_name='compras')
    ingresado = models.BooleanField(default=False)

class ItemAction(TimeStampedModel):
    
    """Crea un registro de cada movimiento efectuado por un :class:`User`
    en un :class:`Item`"""
    
    user = models.ForeignKey(User)
    action = models.TextField()
    item = models.ForeignKey(ItemTemplate, related_name='acciones')
