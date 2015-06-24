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
from decimal import Decimal
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Sum
from django_extensions.db.models import TimeStampedModel

from clinique.models import Consulta, OrdenMedica, Incapacidad, Espera
from emergency.models import Emergencia
from invoice.models import Recibo


class ScoreCard(TimeStampedModel):
    nombre = models.CharField(max_length=255)

    def __unicode__(self):
        return self.nombre

    def get_absolute_url(self):
        """Obtiene la URL absoluta"""

        return reverse('scorecard', args=[self.id])


class Escala(TimeStampedModel):
    score_card = models.ForeignKey(ScoreCard)
    puntaje_inicial = models.DecimalField(max_digits=11, decimal_places=2,
                                          default=0)
    puntaje_final = models.DecimalField(max_digits=11, decimal_places=2,
                                        default=0)
    comision = models.DecimalField(max_digits=11, decimal_places=2, default=0)


class Meta(TimeStampedModel):
    CONSULTA_TIME = 'CT'
    PRE_CONSULTA_TIME = 'PCT'
    PRESCRIPTION_PERCENTAGE = 'PP'
    INCAPACIDAD_PERCENTAGE = 'IP'
    CLIENT_FEEDBACK_PERCENTAGE = 'CFP'
    METAS = (
        (CONSULTA_TIME, u'Tiempo de Consulta'),
        (PRE_CONSULTA_TIME, u'Tiempo en Preconsulta'),
        (PRESCRIPTION_PERCENTAGE, u'Porcentaje de Recetas'),
        (INCAPACIDAD_PERCENTAGE, u'Porcentaje de Incapacidades'),
        (CLIENT_FEEDBACK_PERCENTAGE, u'Porcentaje de Aprobación del Cliente'),
    )
    score_card = models.ForeignKey(ScoreCard)
    tipo_meta = models.CharField(max_length=3, choices=METAS,
                                 default=CONSULTA_TIME)
    peso = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    meta = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    basado_en_tiempo = models.BooleanField(default=False)

    def logro(self, usuario, inicio, fin):

        if self.tipo_meta == self.CONSULTA_TIME:
            return self.average_consulta_time(usuario, inicio, fin)

        if self.tipo_meta == self.PRE_CONSULTA_TIME:
            return self.average_preconsulta(usuario, inicio, fin)

        if self.tipo_meta == self.PRESCRIPTION_PERCENTAGE:
            return self.average_medical_order(usuario, inicio, fin)

        if self.tipo_meta == self.CLIENT_FEEDBACK_PERCENTAGE:
            # TODO: Make this a calculation, there is no data for this
            return 1

        if self.tipo_meta == self.INCAPACIDAD_PERCENTAGE:
            return self.average_incapacidad(usuario, inicio, fin)

    def ponderacion(self, logro):
        if self.basado_en_tiempo:
            return self.meta / max(Decimal(logro), 1)
        return Decimal(logro) / max(self.meta, 1)

    def emergencias(self, usuario, inicio, fin):
        return Emergencia.objects.filter(usuario=usuario,
                                         created__range=(inicio, fin)
                                         )

    def consultas(self, usuario, inicio, fin):
        return Consulta.objects.filter(consultorio__usuario=usuario,
                                       created__range=(inicio, fin)
                                       )

    def recibos(self, usuario, inicio, fin):
        return Recibo.objects.annotate(sold=Sum('ventas__total')).filter(
            created__range=(inicio, fin), cajero=usuario
        )

    def orden_medicas(self, usuario, inicio, fin):
        return OrdenMedica.objects.filter(created__range=(inicio, fin),
                                          usuario=usuario)

    def incapacidades(self, usuario, inicio, fin):
        return Incapacidad.objects.filter(created__range=(inicio, fin),
                                          usuario=usuario)

    def esperas(self, usuario, inicio, fin):
        return Espera.objects.filter(created__range=(inicio, fin),
                                     consultorio__usuario=usuario)

    def average_consulta_time(self, usuario, inicio, fin):
        tiempos = []
        for consulta in self.consultas(usuario, inicio, fin):
            tiempos.append((consulta.final - consulta.created).total_seconds())

        return float(sum(tiempos)) / max(len(tiempos), 1)

    def average_preconsulta(self, usuario, inicio, fin):
        tiempos = []
        for espera in self.esperas(usuario, inicio, fin):
            tiempos.append((espera.final - espera.inicio).total_seconds())

        return float(sum(tiempos)) / max(len(tiempos), 1)

    def average_medical_order(self, usuario, inicio, fin):
        ordenes = self.orden_medicas(usuario, inicio, fin).count()
        consultas = self.consultas(usuario, inicio, fin).count()

        return float(ordenes) / max(consultas, 1)

    def average_incapacidad(self, usuario, inicio, fin):
        incapacidades = self.incapacidades(usuario, inicio, fin).count()
        consultas = self.consultas(usuario, inicio, fin).count()

        return float(incapacidades) / max(consultas, 1)
