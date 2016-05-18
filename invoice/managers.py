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


class ReciboManager(models.Manager):
    """
    Builds a default :class:`QuerySet` for the :class:`Inventario`s
    """

    def get_queryset(self):
        return super(ReciboManager, self).get_queryset().annotate(
            valor=Coalesce(
                Sum('ventas__monto'),
                Decimal()
            ),
        ).select_related(
            'ciudad',
            'legal_data',
            'cliente',
            'cajero',
        ).prefetch_related(
            'ventas',
            'pagos',
            'pagos__aseguradora',
            'pagos__tipo',
        )


class VentaManager(models.Manager):
    """
    Implements many shortcuts related to venta
    """

    def get_queryset(self):
        return super(VentaManager, self).get_queryset().select_related(
            'recibo',
            'recibo__legal_data',
        )

    def periodo(self, inicio, fin):
        """
        Returns all :class:`Venta` corresponding to :class:`Recibo` created in
        the specified date range
        """
        return self.filter(recibo__created__range=(inicio, fin))

    def total(self):
        """
        Obtains the total money from sales
        """

        return self.aggregate(
            total=Coalesce(Sum('monto'), Decimal())
        )['total']
