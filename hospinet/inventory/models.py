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

from decimal import Decimal
from datetime import date

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.db import models
from django_extensions.db.models import TimeStampedModel
from django.contrib.auth.models import User


class Inventario(models.Model):
    class Meta:
        permissions = (
            ('inventario', 'Permite al usuario gestionar inventario'),
        )

    lugar = models.CharField(max_length=255, default='Bodega')
    puede_comprar = models.NullBooleanField(default=False, blank=True,
                                            null=True)

    def __unicode__(self):
        return u"Inventario de {0}".format(self.lugar)

    def buscar_item(self, item_template):
        item = self.items.filter(plantilla=item_template).first()

        if item:
            return item

        return Item(inventario=self, plantilla=item_template)

    def get_absolute_url(self):
        """Obtiene la URL absoluta"""

        return reverse('inventario', args=[self.id])

    def requisiciones_pendientes(self):
        return self.requisiciones.filter(entregada=False).all()

    def transferencias_entrantes(self):
        return self.entradas.filter(aplicada=False).all()

    def transferencias_salientes(self):
        return self.salidas.filter(aplicada=False).all()


class ItemType(TimeStampedModel):
    nombre = models.CharField(max_length=255)
    consulta = models.BooleanField(default=True,
                                   verbose_name='Aparece en Cargos de Consulta')

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
    suppliers = models.ManyToManyField("Proveedor", blank=True,
                                       related_name='plantillas')
    precio_de_venta = models.DecimalField(max_digits=10, decimal_places=2,
                                          default=0)
    costo = models.DecimalField(max_digits=10, decimal_places=2,
                                default=0)
    unidad_de_medida = models.CharField(max_length=32, null=True, blank=True)
    impuestos = models.DecimalField(max_digits=10, decimal_places=2,
                                    default=0)
    activo = models.BooleanField(default=True)
    item_type = models.ManyToManyField(ItemType, related_name='items',
                                       blank=True)
    comision = models.DecimalField(decimal_places=2, max_digits=4,
                                   default=Decimal("30.00"))
    comision2 = models.DecimalField(decimal_places=2, max_digits=4,
                                    default=Decimal("10.00"))

    def __unicode__(self):
        return self.descripcion

    def get_absolute_url(self):
        """Obtiene la URL absoluta"""

        return reverse('itemtemplate', args=[self.id])

    def get_types(self):
        return u"\n".join([t.nombre for t in self.item_type.all()])


class Proveedor(models.Model):
    name = models.CharField(verbose_name=_(u"descripción"), max_length=255)

    def __unicode__(self):
        return self.name


class Item(TimeStampedModel):
    plantilla = models.ForeignKey(ItemTemplate, related_name='items',
                                  verbose_name='Item')
    inventario = models.ForeignKey(Inventario, related_name='items')
    vencimiento = models.DateTimeField(default=timezone.now)
    cantidad = models.IntegerField(default=0)

    def disminuir(self, cantidad):
        self.cantidad -= cantidad
        self.save()

    def incrementar(self, cantidad):
        self.cantidad += cantidad
        self.save()

    def get_absolute_url(self):
        """Obtiene la URL absoluta"""

        return reverse('inventario', args=[self.inventario.id])

    def __unicode__(self):
        return u'{0} en {1}'.format(self.plantilla.descripcion,
                                    self.inventario.lugar)


class Requisicion(TimeStampedModel):
    inventario = models.ForeignKey(Inventario, related_name='requisiciones',
                                   null=True, blank=True)
    aprobada = models.NullBooleanField(default=False)
    entregada = models.NullBooleanField(default=False)
    usuario = models.ForeignKey(User, related_name="requisiciones",
                                null=True, blank=True)

    def get_absolute_url(self):
        """Obtiene la URL absoluta"""

        return reverse('requisicion', args=[self.id])

    def __unicode__(self):
        return u'Requisición Número {1} de {0}'.format(self.inventario.lugar,
                                                       self.id)

    def buscar_item(self, item_template):
        qs = self.items.filter(item=item_template)
        r = list(qs[:1])
        if r:
            return r[0]
        return ItemRequisicion(requisicion=self, item=item_template)


class ItemRequisicion(TimeStampedModel):
    requisicion = models.ForeignKey(Requisicion, related_name='items')
    item = models.ForeignKey(ItemTemplate, related_name='requisiciones')
    cantidad = models.IntegerField()
    entregada = models.BooleanField(default=False)
    pendiente = models.IntegerField(default=0)

    def get_absolute_url(self):
        """Obtiene la URL absoluta"""

        return reverse('item-requisicion-create', args=[self.requisicion.id])

    def disminuir(self, cantidad):
        self.pendiente -= cantidad
        self.save()

    def incrementar(self, cantidad):
        self.pendiente += cantidad

        if self.pendiente >= self.cantidad:
            self.entregada = True

        self.save()


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
        origen = destino = ''
        if self.origen:
            origen = self.origen.lugar
        if self.destino:
            destino = self.destino.lugar
        return u'Transferencia desde {0} hacia {1}'.format(origen, destino)

    def transferir(self):

        for item in self.transferidos.all():

            if item.aplicada:
                continue

            destino = self.destino.buscar_item(item.item)
            origen = self.origen.buscar_item(item.item)
            requisicion = self.requisicion.buscar_item(item.item)

            destino.incrementar(item.cantidad)
            origen.disminuir(item.cantidad)
            requisicion.disminuir(item.cantidad)

            item.aplicada = True
            item.save()

        self.aplicada = True

    def get_absolute_url(self):

        """Obtiene la URL absoluta"""

        return reverse('transferencia', args=[self.id])


class Transferido(TimeStampedModel):
    transferencia = models.ForeignKey(Transferencia,
                                      related_name='transferidos')
    item = models.ForeignKey(ItemTemplate, related_name='transferidos')
    cantidad = models.IntegerField()
    aplicada = models.BooleanField(default=False)

    def __unicode__(self):
        return u'Transferir {1} {0}'.format(self.item.descripcion,
                                            self.cantidad)

    def get_absolute_url(self):
        """Obtiene la URL absoluta"""

        return reverse('transferencia', args=[self.transferencia.id])


class Compra(TimeStampedModel):
    inventario = models.ForeignKey(Inventario, blank=True, null=True,
                                   related_name='compras')
    ingresada = models.BooleanField(default=False)
    proveedor = models.CharField(max_length=255, blank=True, null=True)

    def __unicode__(self):
        return u"Compra efectuada el {0}".format(self.created)

    def get_absolute_url(self):
        """Obtiene la URL absoluta"""

        return reverse('compra', args=[self.id])

    def transferir(self):
        for comprado in self.items.all():
            item = self.inventario.buscar_item(comprado.item)
            item.incrementar(comprado.cantidad)
            item.save()


class ItemComprado(TimeStampedModel):
    compra = models.ForeignKey(Compra, related_name='items')
    item = models.ForeignKey(ItemTemplate, related_name='comprado', blank=True,
                             null=True)
    ingresado = models.BooleanField(default=False)
    cantidad = models.IntegerField(default=0)

    def get_absolute_url(self):
        """Obtiene la URL absoluta"""

        return self.compra.get_absolute_url()


class ItemAction(TimeStampedModel):
    """Crea un registro de cada movimiento efectuado por un :class:`User`
    en un :class:`Item`"""

    user = models.ForeignKey(User)
    action = models.TextField()
    item = models.ForeignKey(ItemTemplate, related_name='acciones')


class TipoVenta(TimeStampedModel):
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    incremento = models.DecimalField(max_digits=10, decimal_places=2,
                                     default=0)
    disminucion = models.DecimalField(max_digits=10, decimal_places=2,
                                      default=0)

    def __unicode__(self):
        return self.descripcion


class Historial(TimeStampedModel):
    inventario = models.ForeignKey(Inventario, related_name='historiales')

    def __unicode__(self):
        return u'{0} el {1}'.format(self.inventario.lugar,
                                    self.fecha.strftime('%d/%m/Y'))

    def get_absolute_url(self):
        """Obtiene la URL absoluta"""

        return reverse('historial', args=[self.id])


class ItemHistorial(TimeStampedModel):
    historial = models.ForeignKey(Historial, related_name='items')
    item = models.ForeignKey(ItemTemplate, related_name='historicos')
    cantidad = models.IntegerField(default=0)

    def __unicode__(self):
        return u'{0} {1} el {2}'.format(self.item.descripcion,
                                        self.historial.inventario.lugar,
                                        self.historial.created.strftime('%d/%m/Y'))
