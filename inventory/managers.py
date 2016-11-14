# -*- coding: utf-8 -*-
#
# Copyright (C) 2016 Carlos Flores <cafg10@gmail.com>
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

from django.db import models
from django.db.models import F, Sum, Count
from django.db.models.functions import Coalesce


class InventarioManager(models.Manager):
    """
    Builds a default :class:`QuerySet` for the :class:`Inventario`s
    """

    def get_queryset(self):
        return super(InventarioManager, self).get_queryset().annotate(
            valor=Coalesce(
                Sum(F('item__cantidad') * F('item__plantilla__precio_de_venta'),
                    output_field=models.DecimalField()),
                Decimal()
            ),
            costo=Coalesce(
                Sum(F('item__cantidad') * F('item__plantilla__costo'),
                    output_field=models.DecimalField()),
                Decimal()
            ),
            total_items=Count('item__id'),
            total_inventory=Coalesce(Sum('item__cantidad'), Decimal()),
        ).prefetch_related(
            'item_set',
            'item_set__plantilla',
        ).prefetch_related(
            'ciudad',
        )


class ItemTemplateManager(models.Manager):
    def get_queryset(self):
        return super(ItemTemplateManager, self).get_queryset().select_related(
            'item_type',
        )


class ItemManager(models.Manager):
    def get_queryset(self):
        return super(ItemManager, self).get_queryset().select_related(
            'plantilla',
        )


class ItemRequisicionManager(models.Manager):
    def get_queryset(self):
        return super(ItemRequisicionManager,
                     self).get_queryset().select_related(
            'item',
        )


class RequisicionManager(models.Manager):
    def get_queryset(self):
        return super(RequisicionManager, self).get_queryset().prefetch_related(
            'items',
            'transferencias',
        ).select_related(
            'usuario',
            'inventario',
        )


class TransferenciaManager(models.Manager):
    def get_queryset(self):
        return super(TransferenciaManager,
                     self).get_queryset().prefetch_related(
            'transferidos',
        ).select_related(
            'usuario',
            'destino',
            'destino__ciudad',
            'origen',
            'origen__ciudad',
        )


class HistorialManager(models.Manager):
    def get_queryset(self):
        return super(HistorialManager, self).get_queryset().prefetch_related(
            'items',
        ).select_related(
            'inventario',
        )


class ItemHistorialManager(models.Manager):
    def get_queryset(self):
        return super(ItemHistorialManager,
                     self).get_queryset().prefetch_related(
            'item',
        )


class CotizacionQuerySet(models.QuerySet):
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


class CotizacionManager(models.Manager):
    """
    Provides a manager for :class:`Cotizacion` that uses
    :class:`CotizacionQuerySet` as its default :class:`QuerySets
    """

    def get_queryset(self):
        return CotizacionQuerySet(self.model, using=self._db).select_related(
            'proveedor',
            'usuario',
            'inventario',
            'inventario__ciudad',
        ).prefetch_related(
            'itemcotizado_set',
            'itemcotizado_set__item',
        ).annotate(
            total=Coalesce(
                Sum(F('itemcotizado__precio') * F('itemcotizado__cantidad'),
                    output_field=models.DecimalField()),
                Decimal()
            )
        )

    def pendientes(self):
        """
        Filters the :class:`Cotizacion` only handling those pending
        """
        return self.get_queryset().pendientes()

    def autorizadas(self):
        return self.get_queryset().autorizadas()

    def compradas(self):
        return self.get_queryset().compradas()
