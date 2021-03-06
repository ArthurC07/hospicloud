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

from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Sum, F
from django.db.models.expressions import ExpressionWrapper, When, Case
from django.db.models.functions import Coalesce
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel

from hospinet.utils import get_current_month_range
from inventory import managers


@python_2_unicode_compatible
class Inventario(models.Model):
    class Meta:
        permissions = (
            ('inventario', _('Permite al usuario gestionar inventario')),
        )

    lugar = models.CharField(max_length=255, default='Bodega')
    puede_comprar = models.BooleanField(default=False)
    activo = models.BooleanField(default=True)
    ciudad = models.ForeignKey('users.Ciudad', blank=True, null=True)

    objects = managers.InventarioManager()

    def __str__(self):
        return _(u"Inventario de {0}").format(self.lugar)

    def items(self):

        return self.item_set.prefetch_related(
            'plantilla',
        ).annotate(
            valor=ExpressionWrapper(
                F('cantidad') * F('plantilla__costo'),
                output_field=models.DecimalField()
            )
        )

    def buscar_item(self, item_template):
        item = self.item_set.filter(plantilla=item_template).first()

        if not item:
            item = Item(inventario=self, plantilla=item_template)
            item.save()

        return item

    def descargar(self, item_template, cantidad, user=None):
        item = self.buscar_item(item_template)
        if not item.plantilla.servicio:
            item.disminuir(cantidad, user)

    def cargar(self, item_template, cantidad, user=None):
        item = self.buscar_item(item_template)
        if not item.plantilla.servicio:
            item.incrementar(cantidad, user)

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
    consulta = models.BooleanField(
        default=True,
        verbose_name=_('Aparece en Cargos de Consulta')
    )

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('item-type', args=[self.id])


@python_2_unicode_compatible
class ItemTemplate(TimeStampedModel):
    descripcion = models.CharField(max_length=255)
    marca = models.CharField(max_length=32, null=True, blank=True)
    modelo = models.CharField(max_length=32, null=True, blank=True)
    notas = models.TextField(null=True, blank=True)
    suppliers = models.ManyToManyField("Proveedor", blank=True,
                                       related_name='plantillas')
    precio_de_venta = models.DecimalField(max_digits=12, decimal_places=4,
                                          default=0)
    costo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    unidad_de_medida = models.CharField(max_length=32, null=True, blank=True)
    impuestos = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    servicio = models.BooleanField(default=False)
    activo = models.BooleanField(default=True)
    item_type = models.ManyToManyField(ItemType, related_name='items',
                                       blank=True)

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
    inventario = models.ForeignKey(Inventario)
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
    denegada = models.BooleanField(default=False)
    entregada = models.BooleanField(default=False)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)

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
    aplicada = models.NullBooleanField(default=False)
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


class AnomaliaTransferencia(TimeStampedModel):
    """
    Registers the problems present in a  :class:`Transferencia
    """
    transferencia = models.ForeignKey(Transferencia)
    item = models.ForeignKey(Transferido)
    cantidad = models.IntegerField(default=0)
    detalle = models.TextField()

    def get_absolute_url(self):
        return self.transferencia.get_absolute_url()


@python_2_unicode_compatible
class Compra(TimeStampedModel):
    """
    Describes a series of items that have been bought and will be transfered to
    a certain :class:`Inventario`
    """
    inventario = models.ForeignKey(Inventario, blank=True, null=True,
                                   related_name='compras')
    ingresada = models.BooleanField(default=False)
    proveedor = models.ForeignKey(Proveedor, blank=True, null=True)
    cotizacion = models.ForeignKey('Cotizacion', blank=True, null=True)
    comprobante = models.FileField(
        upload_to='inventory/compra/comprobante/%Y/%m/%d', blank=True, null=True
    )
    metodo_de_pago = models.FileField(
        upload_to='inventory/compra/pago/%Y/%m/%d', blank=True, null=True
    )
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)

    def __str__(self):
        if self.proveedor:
            return _("Compra a {0}").format(self.proveedor.name)
        return _('Compra').format()

    def get_absolute_url(self):
        """Obtiene la URL absoluta"""

        return reverse('compra', args=[self.id])

    def transferir(self):
        for comprado in self.items().all():
            self.inventario.cargar(comprado.item, comprado.cantidad)

    def total(self):
        """
        Shows the total amount that the bought items represent in monetary value
        :return: DecimalField
        """
        return self.items().aggregate(
            total=Coalesce(
                Sum(F('precio') * F('cantidad'),
                    output_field=models.DecimalField()),
                Decimal()
            )
        )['total']

    def items(self):
        return self.itemcomprado_set.annotate(
            valor=ExpressionWrapper(
                F('precio') * F('cantidad'),
                output_field=models.DecimalField()
            )
        )


@python_2_unicode_compatible
class ItemComprado(TimeStampedModel):
    """
    Describes a :class:`ItemTemplate` that was bought as part of a
    :class:`Compra`
    """
    compra = models.ForeignKey(Compra)
    item = models.ForeignKey(ItemTemplate, related_name='comprado', blank=True,
                             null=True)
    ingresado = models.BooleanField(default=False)
    cantidad = models.IntegerField(default=0)
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.item.descripcion

    def get_absolute_url(self):
        """Obtiene la URL absoluta"""

        return self.compra.get_absolute_url()


class TransferenciaCompra(TimeStampedModel):
    """
    Registers the date when a :class:`Compra` has been transfered
    """
    compra = models.ForeignKey(Compra)


class ItemTransferido(TimeStampedModel):
    """
    Register the items that have been transfered from :class:`Compra`
    """
    transferencia = models.ForeignKey(TransferenciaCompra)
    item = models.ForeignKey(ItemTemplate)
    cantidad = models.IntegerField(default=0)


class AnomaliaCompra(TimeStampedModel):
    """
    Registers discrepancies between the aproved :class:`Compra` and the
    actual presented :class:`Item`s
    """
    item = models.ForeignKey(ItemComprado)
    cantidad = models.IntegerField(default=0)
    detalle = models.TextField()

    def get_absolute_url(self):
        return self.item.compra.get_absolute_url()


class ItemAction(TimeStampedModel):
    """
    Crea un registro de cada movimiento efectuado por un :class:`User`
    en un :class:`Item`
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)


@python_2_unicode_compatible
class Cotizacion(TimeStampedModel):
    """
    Represents a quotation that will be made in the UI
    """
    proveedor = models.ForeignKey(Proveedor)
    creacion = models.DateTimeField(auto_now_add=True)
    vencimiento = models.DateTimeField(auto_now_add=True)
    autorizada = models.BooleanField(default=False)
    denegada = models.BooleanField(default=False)
    comprada = models.BooleanField(default=False)
    inventario = models.ForeignKey(Inventario, blank=True, null=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True,
                                related_name='cotizacion_inventario_set')

    objects = managers.CotizacionManager()

    def __str__(self):
        return _('Cotización de {0}').format(self.proveedor)

    def get_absolute_url(self):
        return reverse('cotizacion-view', args=[self.id])

    def items_requeridos(self):
        """
        Creates a :class:`QuerySet` that displays the :class:`ItemTemplate`s
        needed in the current :class:`Cotizacion`
        :return: :class:`QuerySet`
        """
        return ItemRequisicion.objects.filter(
            cantidad__gt=0,
            requisicion__denegada=False,
            requisicion__entregada=False,
        ).prefetch_related(
            'item',
            'item__items',
            'requisicion',
            'requisicion__inventario',
            'requisicion__inventario__ciudad',
        ).annotate(
            existencias=Case(
                When(
                    item__items__inventario__puede_comprar=True,
                    then=Coalesce(
                        Sum('item__items__cantidad'),
                        Decimal()
                    )
                )
            )
        ).exclude(
            existencias__isnull=True,
        ).order_by(
            'item__descripcion',
        )


class ItemCotizado(TimeStampedModel):
    """
    Represents an :class:`ItemTemplate` that will be part of a
    :class:`Cotizacion`
    """
    cotizacion = models.ForeignKey(Cotizacion)
    item = models.ForeignKey(ItemTemplate)
    cantidad = models.IntegerField(default=0)
    precio = models.DecimalField(max_digits=11, decimal_places=2, default=0)

    def get_absolute_url(self):
        return self.cotizacion.get_absolute_url()
