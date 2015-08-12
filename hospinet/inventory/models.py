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
import calendar
from datetime import date, time, datetime
from decimal import Decimal

from django.core.urlresolvers import reverse
from django.db.models import Sum
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.db import models
from django_extensions.db.models import TimeStampedModel
from django.contrib.auth.models import User


@python_2_unicode_compatible
class Inventario(models.Model):
    class Meta:
        permissions = (
            ('inventario', 'Permite al usuario gestionar inventario'),
        )

    lugar = models.CharField(max_length=255, default='Bodega')
    puede_comprar = models.NullBooleanField(default=False, blank=True,
                                            null=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return u"Inventario de {0}".format(self.lugar)

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
                                   verbose_name='Aparece en Cargos de Consulta')

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('inventario-index')


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
    name = models.CharField(verbose_name=_(u"descripción"), max_length=255)
    rtn = models.CharField(max_length=255, blank=True)
    direccion = models.CharField(max_length=255, blank=True)
    contacto = models.CharField(max_length=255, blank=True)
    telefono = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name


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
        total = Transaccion.objects.filter(
            created__range=(inicio, fin),
            item=self
        ).aggregate(total=Sum('cantidad'))['total']

        if total:
            return total

        return 0

    def movimiento_mes(self):
        now = timezone.now()
        fin = date(now.year, now.month,
                   calendar.monthrange(now.year, now.month)[1])
        inicio = date(now.year, now.month, 1)

        fin = datetime.combine(fin, time.max)
        inicio = datetime.combine(inicio, time.min)

        fin = timezone.make_aware(fin, timezone.get_current_timezone())
        inicio = timezone.make_aware(inicio,
                                     timezone.get_current_timezone())

        return self.movimiento(inicio, fin)

    def get_absolute_url(self):
        """Obtiene la URL absoluta"""

        return reverse('inventario', args=[self.inventario.id])

    def __str__(self):
        return u'{0} en {1}'.format(self.plantilla.descripcion,
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
        return u'Requisición Número {1} de {0}'.format(self.inventario.lugar,
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
        return u'Transferencia desde {0} hacia {1}'.format(origen, destino)

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
        return u'Transferir {1} {0}'.format(self.item.descripcion,
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

    def __str__(self):
        return u"Compra efectuada el {0}".format(self.created)

    def get_absolute_url(self):
        """Obtiene la URL absoluta"""

        return reverse('compra', args=[self.id])

    def transferir(self):
        for comprado in self.items.all():
            self.inventario.cargar(comprado.item, comprado.cantidad)


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


@python_2_unicode_compatible
class TipoVenta(TimeStampedModel):
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    incremento = models.DecimalField(max_digits=10, decimal_places=2,
                                     default=0)
    disminucion = models.DecimalField(max_digits=10, decimal_places=2,
                                      default=0)

    def __str__(self):
        return self.descripcion


@python_2_unicode_compatible
class Historial(TimeStampedModel):
    inventario = models.ForeignKey(Inventario, related_name='historiales')

    def __str__(self):
        return u'{0} el {1}'.format(self.inventario.lugar,
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
        return u'{0} {1} el {2}'.format(self.item.descripcion,
                                        self.historial.inventario.lugar,
                                        self.historial.created.strftime(
                                            '%d/%m/Y'))


class Transaccion(TimeStampedModel):
    item = models.ForeignKey(Item)
    cantidad = models.IntegerField(default=0)
    user = models.ForeignKey(User, blank=True, null=True)


@python_2_unicode_compatible
class Cotizacion(TimeStampedModel):
    proveedor = models.ForeignKey(Proveedor)
    vencimiento = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return u'Cotización de {0}'.format(self.proveedor)

    def get_absolute_url(self):

        return reverse('cotizacion-view', args=[self.id])


class ItemCotizado(TimeStampedModel):
    cotizacion = models.ForeignKey(Cotizacion)
    item = models.ForeignKey(ItemTemplate)
    cantidad = models.IntegerField(default=0)
    precio = models.DecimalField(max_digits=11, decimal_places=2, default=0)

    def get_absolute_url(self):

        return self.cotizacion.get_absolute_url()
