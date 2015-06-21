# -*- coding: utf-8 -*-
#
# Copyright (C) 2015 Carlos Flores <cafg10@gmail.com>
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
from django.contrib.auth.models import User

from django.db import models
from django.db.models import Sum
from django_extensions.db.models import TimeStampedModel

from clinique.models import Consulta
from emergency.models import Emergencia
from invoice.models import Recibo


class Meta(TimeStampedModel):
    EMERGENCY = 'ER'
    CLINIQUE = 'MD'
    INVOICE = 'IN'
    METAS = (
        (INVOICE, u'Cajero'),
        (CLINIQUE, u'Consulta'),
        (EMERGENCY, u'Emergencia')
    )
    usuario = models.ForeignKey(User)
    tipo = models.CharField(max_length=2, choices=METAS, default=EMERGENCY)
    inicio = models.DateTimeField(auto_now_add=True)
    fin = models.DateTimeField(auto_now_add=True)
    base = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    meta = models.DecimalField(max_digits=11, decimal_places=2, default=0)

    def emergency(self):
        return Emergencia.objects.filter(usuario=self.usuario,
                                         created__range=(self.inicio, self.fin)
                                         ).count()

    def clinique(self):
        return Consulta.objects.filter(consultorio___usuario=self.usuario,
                                       created__range=(self.inicio, self.fin)
                                       ).count()

    def invoice(self):
        return Recibo.objects.annotate(sold=Sum('ventas__total')).filter(
            created__range=(self.inicio, self.fin), cajero=self.usuario
        ).aggregate(total=Sum('sold'))['total']
