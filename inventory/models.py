# -*- coding: utf-8 -*-
#
# Copyright (C) 2011-2016 Carlos Flores <cafg10@gmail.com>
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
from __future__ import unicode_literals

from decimal import Decimal

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Sum, QuerySet, F
from django.db.models.functions import Coalesce
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel

from hospinet.utils import get_current_month_range


@python_2_unicode_compatible
class Inventario(models.Model):
    class Meta:
        permissions = (
            ('inventario', _('Permite al usuario gestionar inventario')),
        )

    lugar = models.CharField(max_length=255, default='Bodega')
    puede_comprar = models.NullBooleanField(default=False, blank=True,
                                            null=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return _(u"Inventario de {0}").format(self.lugar)

    def buscar_item(self, item_template):
        item = self.items.filter(plantilla=item_template).first()

        if not item:
            item = Item(inventario=self, plantilla=item_template)
            item.save()

        return item

    def descargar(self, item_template, cantidad, user=None):
        item = self.buscar_item(item_template)
        item.disminuir(cantidad, user)

    def cargar(self, item_template, cantidad, user=None):
        item = self.buscar_item(item_template)
        item.aumentar(cantidad, user)

    def get_absolute_url(self):
        """Obtiene la URL absoluta"""

        return reverse('inventario', args=[self.id])

    def requisiciones_pendientes(self):
        return self.requisiciones.filter(entregada=False).all()

    def transferencias_entrantes(self):
        return self.entradas.filter(aplicada=False).all()

    def transferencias_salientes(self):
        return self.salidas.filter(aplicada=False).all()


@python_2_unicode_compatible
class ItemType(TimeStampedModel):
    nombre = models.CharField(max_length=255)
    consulta = models.BooleanField(default=True,
                                   verbose_name=_(
                                       'Aparece en Cargos de Consulta'))

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('item-type', args=[self.id])


@python_2_unicode_compatible
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
    costo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    unidad_de_medida = models.CharField(max_length=32, null=True, blank=True)
    impuestos = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    activo = models.BooleanField(default=True)
    item_type = models.ManyToManyField(ItemType, related_name='items',
                                       blank=True)
    comision = models.DecimalField(decimal_places=2, max_digits=4,
                                   default=Decimal("30.00"))
    comision2 = models.DecimalField(decimal_places=2, max_digits=4,
                                    default=Decimal("10.00"))

    def __str__(self):
        return self.descripcion

    def get_absolute_url(self):
        """Obtiene la URL absoluta"""

        return reverse('itemtemplate', args=[self.id])

    def get_types(self):
        return u"\n".join([t.nombre for t in self.item_type.all()])


@python_2_unicode_compatible
class Proveedor(models.Model):
    """
    Represents someone that sells stuff or provides a service to the company
    """

    class Meta:
        ordering = ('name', 'rtn')

    name = models.CharField(verbose_name=_("Nombre Completo de la Empresa"),
                            max_length=255)
    rtn = models.CharField(max_length=255, blank=True)
    direccion = models.CharField(max_length=255, blank=True)
    contacto = models.CharField(max_length=255, blank=True)
    telefono = models.CharField(max_length=255, blank=True)
    constancia_de_pagos_a_cuenta = models.FileField(blank=True, null=True,
                                                    upload_to='inventory/provider/%Y/%m/%d')

    def __str__(self):
        return _('{0} - {1}').format(self.name, self.rtn)

    def get_absolute_url(self):
        return reverse('proveedor', args=[self.id])


@python_2_unicode_compatible
class Item(TimeStampedModel):
    plantilla = models.ForeignKey(ItemTemplate, related_name='items',
                                  verbose_name='Item')
    inventario = models.ForeignKey(Inventario, related_name='items')
    vencimiento = models.DateTimeField(default=timezone.now)
    cantidad = models.IntegerField(default=0)

    def disminuir(self, cantidad, user=None):
        self.cantidad -= cantidad

        transaccion = Transaccion()

        transaccion.item = self
        transaccion.cantidad = -abs(cantidad)
        transaccion.user = user
        transaccion.save()

        self.save()

    def incrementar(self, cantidad, user=None):
        self.cantidad += cantidad

        transaccion = Transaccion()

        transaccion.item = self
        transaccion.cantidad = abs(cantidad)
        transaccion.user = user
        transaccion.save()

        self.save()

    def movimiento(self, inicio, fin):
        return Transaccion.objects.filter(
            created__range=(inicio, fin),
            item=self
        ).aggregate(total=Coalesce(Sum('cantidad'), Decimal()))['total']

    def movimiento_mes(self):
        fin, inicio = get_current_month_range()

        return self.movimiento(inicio, fin)

    def get_absolute_url(self):
        """Obtiene la URL absoluta"""

        return reverse('inventario', args=[self.inventario.id])

    def __str__(self):
        return '{0} en {1}'.format(self.plantilla.descripcion,
                                   self.inventario.lugar)


@python_2_unicode_compatible
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

    def __str__(self):
        return _('Requisición Número {1} de {0}').format(self.inventario.lugar,
                                                         self.id)

    def buscar_item(self, item_template):
        item = self.items.filter(item=item_template).first()

        if item:
            return item
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


@python_2_unicode_compatible
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

    def __str__(self):
        origen = destino = ''
        if self.origen:
            origen = self.origen.lugar
        if self.destino:
            destino = self.destino.lugar
        return _('Transferencia desde {0} hacia {1}').format(origen, destino)

    def transferir(self):

        for item in self.transferidos.all():

            if item.aplicada:
                continue

            self.destino.cargar(item.item, item.cantidad, self.usuario)
            self.origen.descargar(item.item, item.cantidad, self.usuario)
            requisicion = self.requisicion.buscar_item(item.item)

            requisicion.disminuir(item.cantidad)

            item.aplicada = True
            item.save()

        self.aplicada = True

    def get_absolute_url(self):

        """Obtiene la URL absoluta"""

        return reverse('transferencia', args=[self.id])


@python_2_unicode_compatible
class Transferido(TimeStampedModel):
    transferencia = models.ForeignKey(Transferencia,
                                      related_name='transferidos')
    item = models.ForeignKey(ItemTemplate, related_name='transferidos')
    cantidad = models.IntegerField()
    aplicada = models.BooleanField(default=False)

    def __str__(self):
        return _('Transferir {1} {0}').format(self.item.descripcion,
                                              self.cantidad)

    def get_absolute_url(self):
        """Obtiene la URL absoluta"""

        return reverse('transferencia', args=[self.transferencia.id])


@python_2_unicode_compatible
class Compra(TimeStampedModel):
    inventario = models.ForeignKey(Inventario, blank=True, null=True,
                                   related_name='compras')
    ingresada = models.BooleanField(default=False)
    proveedor = models.ForeignKey(Proveedor, blank=True, null=True)
    cotizacion = models.ForeignKey('Cotizacion', blank=True, null=True)

    def __str__(self):
        return _(u"Compra efectuada el {0}").format(self.created)

    def get_absolute_url(self):
        """Obtiene la URL absoluta"""

        return reverse('compra', args=[self.id])

    def transferir(self):
        for comprado in self.items.all():
            self.inventario.cargar(comprado.item, comprado.cantidad)

    def total(self):

        return self.items.aggregate(
            total=Coalesce(
                Sum(F('precio') * F('cantidad'), output_field=models.DecimalField()),
                Decimal()
            )
        )['total']


class ItemComprado(TimeStampedModel):
    compra = models.ForeignKey(Compra, related_name='items')
    item = models.ForeignKey(ItemTemplate, related_name='comprado', blank=True,
                             null=True)
    ingresado = models.BooleanField(default=False)
    cantidad = models.IntegerField(default=0)
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def get_absolute_url(self):
        """Obtiene la URL absoluta"""

        return self.compra.get_absolute_url()


class ItemAction(TimeStampedModel):
    """Crea un registro de cada movimiento efectuado por un :class:`User`
    en un :class:`Item`"""

    user = models.ForeignKey(User)
    action = models.TextField()
    item = models.ForeignKey(ItemTemplate, related_name='acciones')


@python_2_unicode_compatible
class TipoVenta(TimeStampedModel):
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    incremento = models.DecimalField(max_digits=10, decimal_places=2,
                                     default=0)
    disminucion = models.DecimalField(max_digits=10, decimal_places=2,
                                      default=0)
    predeterminada = models.BooleanField(default=False)

    def __str__(self):
        return self.descripcion


@python_2_unicode_compatible
class Historial(TimeStampedModel):
    inventario = models.ForeignKey(Inventario, related_name='historiales')

    def __str__(self):
        return _('{0} el {1}').format(self.inventario.lugar,
                                      self.fecha.strftime('%d/%m/Y'))

    def get_absolute_url(self):
        """Obtiene la URL absoluta"""

        return reverse('historial', args=[self.id])


@python_2_unicode_compatible
class ItemHistorial(TimeStampedModel):
    historial = models.ForeignKey(Historial, related_name='items')
    item = models.ForeignKey(ItemTemplate, related_name='historicos')
    cantidad = models.IntegerField(default=0)

    def __str__(self):
        return _('{0} {1} el {2}').format(self.item.descripcion,
                                          self.historial.inventario.lugar,
                                          self.historial.created.strftime(
                                              '%d/%m/Y'))


class Transaccion(TimeStampedModel):
    item = models.ForeignKey(Item)
    cantidad = models.IntegerField(default=0)
    user = models.ForeignKey(User, blank=True, null=True)


class CotizacionQuerySet(QuerySet):
    """
    Contains shortcuts for querying :class:`Cotizacion`
    """
    def pendientes(self):
        """
        Filters the :class:`Cotizacion` only handling those pending
        """
        return self.filter(
            comprada=False,
            denegada=False,
            autorizada=False,
        )

    def autorizadas(self):
        return self.filter(
            comprada=False,
            autorizada=True,
        )

    def compradas(self):
        return self.filter(
            comprada=True,
        )


@python_2_unicode_compatible
class Cotizacion(TimeStampedModel):
    proveedor = models.ForeignKey(Proveedor)
    vencimiento = models.DateTimeField(auto_now_add=True)
    autorizada = models.BooleanField(default=False)
    denegada = models.BooleanField(default=False)
    comprada = models.BooleanField(default=False)
    inventario = models.ForeignKey(Inventario, blank=True, null=True)

    objects = CotizacionQuerySet.as_manager()

    def __str__(self):
        return _('Cotización de {0}').format(self.proveedor)

    def get_absolute_url(self):
        return reverse('cotizacion-view', args=[self.id])

    def total(self):

        return self.itemcotizado_set.aggregate(
            total=Coalesce(
                Sum(F('precio') * F('cantidad'), output_field=models.DecimalField()),
                Decimal()
            )
        )['total']


class ItemCotizado(TimeStampedModel):
    cotizacion = models.ForeignKey(Cotizacion)
    item = models.ForeignKey(ItemTemplate)
    cantidad = models.IntegerField(default=0)
    precio = models.DecimalField(max_digits=11, decimal_places=2, default=0)

    def get_absolute_url(self):
        return self.cotizacion.get_absolute_url()
