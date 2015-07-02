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
from django.utils.encoding import python_2_unicode_compatible
from django_extensions.db.models import TimeStampedModel

from clinique.models import Consulta, OrdenMedica, Incapacidad, Espera
from emergency.models import Emergencia
from invoice.models import Recibo

@python_2_unicode_compatible
class ScoreCard(TimeStampedModel):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        """Obtiene la URL absoluta"""

        return reverse('scorecard', args=[self.id])

    def get_escala(self, score):
        escalas = Escala.objects.filter(score_card=self,
                                        puntaje_final__lte=score,
                                        puntaje_inicial__gte=score)
        return escalas.all()

    def get_extras(self, usuario, inicio, fin):
        extras = []
        for extra in self.extra_set.all():

            if extra.cumplido(usuario, inicio, fin):
                extras.append(extra)

        return extras


class Escala(TimeStampedModel):
    score_card = models.ForeignKey(ScoreCard)
    puntaje_inicial = models.DecimalField(max_digits=11, decimal_places=2,
                                          default=0)
    puntaje_final = models.DecimalField(max_digits=11, decimal_places=2,
                                        default=0)
    comision = models.DecimalField(max_digits=11, decimal_places=2, default=0)


class Extra(TimeStampedModel):
    EMERGENCIA = 'ER'
    EXTRAS = (
        (EMERGENCIA, u'Emergencias Atendidas'),
    )
    tipo_extra = models.CharField(max_length=3, choices=EXTRAS,
                                  default=Emergencia)
    score_card = models.ForeignKey(ScoreCard)
    inicio_de_rango = models.DecimalField(max_digits=11, decimal_places=2,
                                          default=0)
    fin_de_rango = models.DecimalField(max_digits=11, decimal_places=2,
                                       default=0)
    comision = models.DecimalField(max_digits=11, decimal_places=2, default=0)

    def cumplido(self, usuario, inicio, fin):

        cantidad = self.cantidad(usuario, inicio, fin)

        if self.inicio_de_rango <= cantidad <= self.fin_de_rango:
            return True

        return False

    def cantidad(self, usuario, inicio, fin):
        if self.tipo_extra == self.EMERGENCIA:
            return self.emergencias(usuario, inicio, fin).count()

        return Decimal()

    def emergencias(self, usuario, inicio, fin):
        return Emergencia.objects.filter(usuario=usuario,
                                         created__range=(inicio, fin))


class Meta(TimeStampedModel):
    CONSULTA_TIME = 'CT'
    PRE_CONSULTA_TIME = 'PCT'
    PRESCRIPTION_PERCENTAGE = 'PP'
    INCAPACIDAD_PERCENTAGE = 'IP'
    CLIENT_FEEDBACK_PERCENTAGE = 'CFP'
    CONSULTA_REMITIDA = 'CR'
    METAS = (
        (CONSULTA_TIME, u'Tiempo de Consulta'),
        (PRE_CONSULTA_TIME, u'Tiempo en Preconsulta'),
        (PRESCRIPTION_PERCENTAGE, u'Porcentaje de Recetas'),
        (INCAPACIDAD_PERCENTAGE, u'Porcentaje de Incapacidades'),
        (CLIENT_FEEDBACK_PERCENTAGE, u'Porcentaje de Aprobación del Cliente'),
        (CONSULTA_REMITIDA, u'Consulta Remitida a Especialista'),
    )
    score_card = models.ForeignKey(ScoreCard)
    tipo_meta = models.CharField(max_length=3, choices=METAS,
                                 default=CONSULTA_TIME)
    peso = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    meta = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    basado_en_tiempo = models.BooleanField(default=False)
    logro_menor_que_meta = models.BooleanField(default=False)

    def logro(self, usuario, inicio, fin):

        if self.tipo_meta == self.CONSULTA_TIME:
            return self.average_consulta_time(usuario, inicio, fin)

        if self.tipo_meta == self.PRE_CONSULTA_TIME:
            return self.average_preconsulta(usuario, inicio, fin)

        if self.tipo_meta == self.PRESCRIPTION_PERCENTAGE:
            return self.average_medical_order(usuario, inicio, fin)

        if self.tipo_meta == self.CLIENT_FEEDBACK_PERCENTAGE:
            return self.poll_average(usuario, inicio, fin)

        if self.tipo_meta == self.CONSULTA_REMITIDA:
            return self.consulta_remitida(usuario, inicio, fin)

        if self.tipo_meta == self.INCAPACIDAD_PERCENTAGE:
            return self.average_incapacidad(usuario, inicio, fin)

        return Decimal()

    def ponderacion(self, logro):
        if self.basado_en_tiempo or self.logro_menor_que_meta:
            return self.meta / max(Decimal(logro), 1)
        return Decimal(logro) / max(self.meta, 1)

    def logro_ponderado(self, ponderacion):
        return min(self.peso, ponderacion * self.peso)

    def emergencias(self, usuario, inicio, fin):
        return Emergencia.objects.filter(usuario=usuario,
                                         created__range=(inicio, fin)
                                         )

    def consultas(self, usuario, inicio, fin):
        return Consulta.objects.filter(consultorio__usuario=usuario,
                                       created__range=(inicio, fin),
                                       activa=False
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
            if consulta.final is None:
                continue
            segundos = (consulta.final - consulta.created).total_seconds()
            minutos = Decimal(segundos) / 60
            tiempos.append(minutos)

        return Decimal(sum(tiempos)) / max(len(tiempos), 1)

    def average_preconsulta(self, usuario, inicio, fin):
        tiempos = []
        for espera in self.esperas(usuario, inicio, fin):
            segundos = (espera.inicio - espera.fecha).total_seconds()
            minutos = Decimal(segundos) / 60
            tiempos.append(minutos)
            tiempos.append(minutos)

        return Decimal(sum(tiempos)) / max(len(tiempos), 1)

    def average_medical_order(self, usuario, inicio, fin):
        ordenes = self.orden_medicas(usuario, inicio, fin).count()
        consultas = self.consultas(usuario, inicio, fin).count()

        return Decimal(ordenes) / max(consultas, 1) * 100

    def average_incapacidad(self, usuario, inicio, fin):
        incapacidades = self.incapacidades(usuario, inicio, fin).count()
        consultas = self.consultas(usuario, inicio, fin).count()

        return (Decimal(incapacidades) / max(consultas, 1)) * 100

    def consulta_remitida(self, usuario, inicio, fin):

        remitidas = self.consultas(usuario, inicio, fin).filter(
            remitida=True
        ).count()

        consultas = self.consultas(usuario, inicio, fin).count()
        return Decimal(remitidas) / max(consultas, 1) * 100

    def poll_average(self, usuario, inicio, fin):

        votos = Voto.objects.filter(opcion__isnull=False,
                                    created__range=(inicio, fin),
                                    respuesta__consulta__consultorio__usuario=usuario,
                                    pregunta__calificable=True)

        total = votos.aggregate(total=Sum('opcion__valor'))['total']
        if total is None:
            total = Decimal()
            
        return Decimal(total) / max(votos.count(), 1)

@python_2_unicode_compatible
class Encuesta(TimeStampedModel):
    nombre = models.CharField(max_length=255)

    def get_absolute_url(self):
        """Obtiene la URL absoluta"""

        return reverse('encuesta', args=[self.id])

    def __str__(self):
        return self.nombre

@python_2_unicode_compatible
class Pregunta(TimeStampedModel):
    encuesta = models.ForeignKey(Encuesta)
    pregunta = models.CharField(max_length=255)
    calificable = models.BooleanField(default=True)

    def __str__(self):
        return self.pregunta

    def get_absolute_url(self):
        """Obtiene la URL absoluta"""

        return reverse('pregunta', args=[self.id])


@python_2_unicode_compatible
class Opcion(TimeStampedModel):
    pregunta = models.ForeignKey(Pregunta)
    respuesta = models.CharField(max_length=255)
    valor = models.IntegerField(default=0)

    def __str__(self):

        return self.respuesta


@python_2_unicode_compatible
class Respuesta(TimeStampedModel):
    encuesta = models.ForeignKey(Encuesta)
    consulta = models.ForeignKey(Consulta)

    def get_absolute_url(self):
        """Obtiene la URL absoluta"""

        return reverse('respuesta', args=[self.id])

    def __str__(self):

        return u'Respuesta a {0}'.format(self.encuesta.nombre)

    def puntuacion(self):
        votos = Voto.objects.filter(opcion__isnull=False, respuesta=self)

        total = votos.aggregate(total=Sum('opcion__valor'))['total']
        if total is None:
            total = Decimal()

        return Decimal(total) / max(votos.count(), 1)


class Voto(TimeStampedModel):
    respuesta = models.ForeignKey(Respuesta)
    pregunta = models.ForeignKey(Pregunta)
    opcion = models.ForeignKey(Opcion, blank=True, null=True)

    def get_absolute_url(self):
        """Obtiene la URL absoluta"""

        return reverse('respuesta', args=[self.respuesta.id])
