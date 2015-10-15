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
import calendar
from datetime import date, datetime, time
from decimal import Decimal

from django.contrib.auth.models import User, user_logged_in
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.utils import timezone
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from django_extensions.db.models import TimeStampedModel

from clinique.models import Consulta, OrdenMedica, Incapacidad, Espera
from emergency.models import Emergencia
from invoice.models import Recibo
from persona.models import Persona
from users.models import UserProfile, Turno


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


@python_2_unicode_compatible
class Extra(TimeStampedModel):
    EMERGENCIA = 'ER'
    EVALUACION = 'EV'
    EXTRAS = (
        (EMERGENCIA, _(u'Emergencias Atendidas')),
        (EVALUACION, _(u'Evaluación del Estudiante'))
    )
    tipo_extra = models.CharField(max_length=3, choices=EXTRAS,
                                  default=Emergencia)
    descripcion = models.CharField(max_length=255, blank=True)
    score_card = models.ForeignKey(ScoreCard)
    inicio_de_rango = models.DecimalField(max_digits=11, decimal_places=2,
                                          default=0)
    fin_de_rango = models.DecimalField(max_digits=11, decimal_places=2,
                                       default=0)
    comision = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    es_puntuado = models.BooleanField(default=False)

    def __str__(self):

        return _(u'{0} de {1}').format(
            self.get_tipo_extra_display(),
            self.score_card.nombre
        )

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


class Puntuacion(TimeStampedModel):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL)
    extra = models.ForeignKey(Extra)
    fecha = models.DateTimeField(default=timezone.now)
    puntaje = models.DecimalField(max_digits=11, decimal_places=2, default=0)


@python_2_unicode_compatible
class Meta(TimeStampedModel):
    CONSULTA_TIME = 'CT'
    PRE_CONSULTA_TIME = 'PCT'
    PRESCRIPTION_PERCENTAGE = 'PP'
    INCAPACIDAD_PERCENTAGE = 'IP'
    CLIENT_FEEDBACK_PERCENTAGE = 'CFP'
    CONSULTA_REMITIDA = 'CR'
    COACHING = 'CO'
    PUNTUALIDAD = 'PU'
    QUEJAS = 'QJ'
    VENTAS = 'VE'
    PRESUPUESTO = 'PR'
    TURNOS = 'TU'
    TEACHING = 'TE'
    EVALUACION = 'EV'
    CAPACITACIONES = 'CA'
    METAS = (
        (CONSULTA_TIME, _(u'Tiempo de Consulta')),
        (PRE_CONSULTA_TIME, _(u'Tiempo en Preconsulta')),
        (PRESCRIPTION_PERCENTAGE, _(u'Porcentaje de Recetas')),
        (INCAPACIDAD_PERCENTAGE, _(u'Porcentaje de Incapacidades')),
        (
            CLIENT_FEEDBACK_PERCENTAGE,
            _(u'Porcentaje de Aprobación del Cliente')),
        (CONSULTA_REMITIDA, _(u'Consulta Remitida a Especialista')),
        (COACHING, _(u'Coaching')),
        (PUNTUALIDAD, _(u'Puntualidad')),
        (QUEJAS, _(u'Manejo de Quejas')),
        (VENTAS, _(u'Ventas del Mes')),
        (PRESUPUESTO, _(u'Manejo de Presupuesto')),
        (TURNOS, _(u'Manejo de Turnos')),
        (TEACHING, _(u'Horas Enseñadas')),
        (EVALUACION, _(u'Evaluación de Alumnos')),
        (CAPACITACIONES, _(u'Capacitaciones')),
    )
    score_card = models.ForeignKey(ScoreCard)
    tipo_meta = models.CharField(max_length=3, choices=METAS,
                                 default=CONSULTA_TIME)
    peso = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    meta = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    basado_en_tiempo = models.BooleanField(default=False)
    logro_menor_que_meta = models.BooleanField(default=False)
    activa = models.BooleanField(default=True)

    def __str__(self):

        return _(u'{0} de {1}').format(
            self.get_tipo_meta_display(),
            self.score_card.nombre
        )

    def logro(self, usuario, inicio, fin):
        """
        Returns the percentage value obtained by the :class:`User` during the
        specific time frame.
        """

        logins = Login.objects.filter(user=usuario,
                                      created__range=(inicio, fin)).count()

        turnos = usuario.turno_set.count()

        if logins < 5 < turnos:
            return Decimal()

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

        evaluaciones = Evaluacion.objects.filter(meta=self, usuario=usuario,
                                                 fecha__range=(inicio, fin))

        return evaluaciones.aggregate(
            total=Coalesce(Sum('puntaje'), Decimal())
        )['total']

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

        votos = Voto.objects.filter(
            opcion__isnull=False,
            created__range=(inicio, fin),
            respuesta__consulta__consultorio__usuario=usuario,
            pregunta__calificable=True
        )

        total = votos.aggregate(
            total=Coalesce(Sum('opcion__valor'), Decimal())
        )['total']

        return Decimal(total) / max(votos.count(), 1)


class Evaluacion(TimeStampedModel):
    meta = models.ForeignKey(Meta)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL)
    fecha = models.DateTimeField(default=timezone.now)
    puntaje = models.DecimalField(max_digits=11, decimal_places=2, default=0)


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
    class Meta:
        ordering = ["created"]

    encuesta = models.ForeignKey(Encuesta)
    pregunta = models.CharField(max_length=255)
    calificable = models.BooleanField(default=True)
    mostrar_sugerencia = models.BooleanField(default=False)

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
    terminada = models.BooleanField(default=False)

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
    sugerencia = models.TextField(blank=True, null=True)

    def get_absolute_url(self):
        """Obtiene la URL absoluta"""

        return reverse('respuesta', args=[self.respuesta.id])


class Holiday(TimeStampedModel):
    day = models.DateField()


class Login(TimeStampedModel):
    user = models.ForeignKey(User)
    holiday = models.BooleanField(default=False)


def register_login(sender, user, request, **kwargs):
    day = timezone.now().date()
    holidays = Holiday.objects.filter(day=day)
    logins = Login.objects.filter(created__range=(
        timezone.make_aware(datetime.combine(day, time.min),
                            timezone.get_current_timezone()),
        timezone.make_aware(datetime.combine(day, time.max),
                            timezone.get_current_timezone())
    )).count()

    if logins > 0:
        return

    login = Login(user=user)
    if holidays.count() > 0 or day.weekday() not in range(1, 6):
        login.holiday = True

    login.save()


user_logged_in.connect(register_login)

Persona.cantidad_encuestas = property(lambda p: Respuesta.objects.filter(
    consulta__persona=p).count())

Persona.ultima_encuesta = property(lambda p: Respuesta.objects.filter(
    consulta__persona=p).order_by('created').last())


def get_current_month_logins(user):
    now = timezone.now()
    fin = date(now.year, now.month,
               calendar.monthrange(now.year, now.month)[1])
    inicio = date(now.year, now.month, 1)

    fin = datetime.combine(fin, time.max)
    inicio = datetime.combine(inicio, time.min)

    fin = timezone.make_aware(fin, timezone.get_current_timezone())
    inicio = timezone.make_aware(inicio,
                                 timezone.get_current_timezone())

    query = Login.objects.filter(created__range=(inicio, fin),
                                 user=user)

    value = {
        'normal': query.filter(holiday=False).count(),
        'festivos': query.filter(holiday=True).count(),
    }

    return value


UserProfile.get_current_month_logins = property(
    lambda p: get_current_month_logins(p.user))
