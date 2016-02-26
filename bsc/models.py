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
from __future__ import unicode_literals

from datetime import timedelta
from decimal import Decimal

import unicodecsv
from django.conf import settings
from django.contrib.auth.models import User, user_logged_in
from django.core.files.storage import default_storage as storage
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel

from budget.models import Presupuesto
from clinique.models import Consulta, OrdenMedica, Incapacidad, Espera
from contracts.models import MasterContract
from emergency.models import Emergencia
from hospinet.utils import get_current_month_range
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
        (EMERGENCIA, _('Emergencias Atendidas')),
        (EVALUACION, _('Evaluación del Estudiante'))
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

        return _('{0} de {1}').format(
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
    class Meta:
        ordering = ('tipo_meta',)

    CONSULTA_TIME = 'CT'
    PRE_CONSULTA_TIME = 'PCT'
    PRESCRIPTION_PERCENTAGE = 'PP'
    INCAPACIDAD_PERCENTAGE = 'IP'
    CLIENT_FEEDBACK_PERCENTAGE = 'CFP'
    CONSULTA_REMITIDA = 'CR'
    COACHING = 'CO'
    PUNTUALIDAD = 'P'
    QUEJAS = 'QJ'
    VENTAS = 'VE'
    PRESUPUESTO = 'PR'
    TURNOS = 'T'
    TEACHING = 'TE'
    EVALUACION = 'EV'
    CAPACITACIONES = 'CA'
    METAS = (
        (CONSULTA_TIME, _('Tiempo de Consulta')),
        (PRE_CONSULTA_TIME, _('Tiempo en Preconsulta')),
        (PRESCRIPTION_PERCENTAGE, _('Porcentaje de Recetas')),
        (INCAPACIDAD_PERCENTAGE, _('Porcentaje de Incapacidades')),
        (
            CLIENT_FEEDBACK_PERCENTAGE,
            _('Porcentaje de Aprobación del Cliente')),
        (CONSULTA_REMITIDA, _('Consulta Remitida a Especialista')),
        (COACHING, _('Coaching')),
        (PUNTUALIDAD, _('Puntualidad')),
        (QUEJAS, _('Manejo de Quejas')),
        (VENTAS, _('Ventas del Mes')),
        (PRESUPUESTO, _('Manejo de Presupuesto')),
        (TURNOS, _('Manejo de Turnos')),
        (TEACHING, _('Horas Enseñadas')),
        (EVALUACION, _('Evaluación de Alumnos')),
        (CAPACITACIONES, _('Capacitaciones')),
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

        return _('{0} de {1}').format(
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

        turnos = usuario.turno_set.filter(
            inicio__range=(inicio, timezone.now()),
            contabilizable=True
        )

        if logins < 5 and turnos.count() < 5:
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

        if self.tipo_meta == self.QUEJAS:
            return self.quejas(usuario, inicio, fin)

        if self.tipo_meta == self.PUNTUALIDAD:
            return self.puntualidad(usuario, turnos)

        if self.tipo_meta == self.VENTAS:
            return self.ventas(usuario, inicio, fin)

        if self.tipo_meta == self.TURNOS:
            return self.turnos(usuario, inicio, fin)

        if self.tipo_meta == self.PRESUPUESTO:
            return self.presupuesto(usuario)

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
        tiempos = 0
        consultas = self.consultas(usuario, inicio, fin)
        for consulta in consultas:
            if consulta.final is None:
                continue
            segundos = (consulta.final - consulta.created).total_seconds()
            minutos = Decimal(segundos) / 60
            tiempos += minutos

        return Decimal(tiempos) / max(consultas.count(), 1)

    def average_preconsulta(self, usuario, inicio, fin):
        tiempos = 0
        esperas = self.esperas(usuario, inicio, fin)
        for espera in esperas:
            segundos = (espera.inicio - espera.fecha).total_seconds()
            minutos = Decimal(segundos) / 60
            tiempos += minutos

        return Decimal(tiempos) / max(esperas.count(), 1)

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

    def ventas(self, usuario, inicio, fin):

        ventas = MasterContract.objects.filter(
            vendedor__usuario=usuario,
            created__range=(inicio, fin),
        ).count()

        return ventas

    def puntualidad(self, usuario, turnos):

        logins = 0
        for turno in turnos:
            logins += get_login(turno, usuario).count()

        return Decimal(logins) / max(turnos.count(), 1) * 100

    def quejas(self, usuario, inicio, fin):

        quejas = Queja.objects.select_related(
            'respuesta__consulta__consultorio__usuario__profile__ciudad'
        ).filter(
            created__range=(inicio, fin),
            respuesta__consulta__consultorio__usuario__profile__ciudad=usuario.profile.ciudad,
        )

        incompletas = quejas.filter(resuelta=False)

        return incompletas.count() / max(quejas.count(), 1)

    def presupuesto(self, usuario):

        presupuesto = Presupuesto.objects.filter(
            ciudad=usuario.profile.ciudad,
            activo=True
        ).first()

        if presupuesto is None:
            return Decimal()

        return presupuesto.porcentaje_ejecutado_mes_actual()

    def turnos(self, usuario, inicio, fin):

        turnos = Turno.objects.filter(
            created__range=(inicio, fin),
            ciudad=usuario.profile.ciudad,
        )

        return turnos.count() / max(turnos.count(), 1)


@python_2_unicode_compatible
class Evaluacion(TimeStampedModel):
    meta = models.ForeignKey(Meta)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL)
    fecha = models.DateTimeField(default=timezone.now)
    puntaje = models.DecimalField(max_digits=11, decimal_places=2, default=0)

    def __str__(self):
        return self.meta.get_tipo_meta_display()


@python_2_unicode_compatible
class ArchivoNotas(TimeStampedModel):
    meta = models.ForeignKey(Meta)
    fecha = models.DateTimeField(default=timezone.now)
    columna_de_usuarios = models.IntegerField()
    columna_de_puntaje = models.IntegerField()

    def __str__(self):
        return self.meta.get_tipo_meta_display()

    def get_absolute_url(self):
        return reverse('archivoNotas', args=[self.id])

    def procesar(self):
        archivo = storage.open(self.archivo.name, 'r')
        data = unicodecsv.reader(archivo)
        [procesar_notas(
            linea,
            self.fecha,
            self.meta,
            self.columna_de_usuarios - 1,
            self.columna_de_puntaje - 1
        ) for linea in data]


def procesar_notas(linea, fecha, meta, usuario, puntaje):
    evaluacion = Evaluacion()
    evaluacion.puntaje = linea[puntaje]
    evaluacion.usuario = linea[usuario]
    evaluacion.fecha = fecha
    evaluacion.meta = meta
    evaluacion.save()


@python_2_unicode_compatible
class Encuesta(TimeStampedModel):
    nombre = models.CharField(max_length=255)

    def get_absolute_url(self):
        """Obtiene la URL absoluta"""

        return reverse('encuesta', args=[self.id])

    def __str__(self):
        return self.nombre

    def consultas(self):
        """
        Obtains the :class:`Consulta`s that will be interviewed
        """
        a_month_ago = timezone.now() - timedelta(days=30)
        consultas = Consulta.objects.select_related(
            'persona',
            'poliza',
            'poliza__aseguradora',
            'persona__ciudad',
        ).prefetch_related(
            'persona__respuesta_set',
            'persona__contratos',
            'poliza__contratos',
            'persona__beneficiarios',
            'persona__beneficiarios__contrato'
        ).filter(
            facturada=True,
            encuestada=False,
        ).exclude(
            persona__respuesta__created__gte=a_month_ago,
        )

        return consultas


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
    persona = models.ForeignKey(Persona, blank=True, null=True)
    terminada = models.BooleanField(default=False)

    class Meta:
        ordering = ['created', ]
        get_latest_by = 'created'

    def get_absolute_url(self):
        """Obtiene la URL absoluta"""

        return reverse('respuesta', args=[self.id])

    def __str__(self):
        return 'Respuesta a {0}'.format(self.encuesta.nombre)

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


@python_2_unicode_compatible
class Queja(TimeStampedModel):
    respuesta = models.ForeignKey(Respuesta)
    queja = models.TextField()
    resuelta = models.BooleanField(default=False)

    def __str__(self):
        return self.queja

    def get_absolute_url(self):
        """Obtiene la URL absoluta"""

        return reverse('queja', args=[self.id])


class Solucion(TimeStampedModel):
    queja = models.ForeignKey(Queja)
    solucion = models.TextField()
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL)

    def get_absolute_url(self):
        return reverse('queja', args=[self.queja.id])


class Holiday(TimeStampedModel):
    day = models.DateField()


class Login(TimeStampedModel):
    user = models.ForeignKey(User)
    holiday = models.BooleanField(default=False)


def register_login(sender, user, request, **kwargs):
    day = timezone.now().date()
    holidays = Holiday.objects.filter(day=day)

    login = Login(user=user)
    if holidays.count() > 0 or day.weekday() not in range(1, 6):
        login.holiday = True

    login.save()


user_logged_in.connect(register_login)

Persona.cantidad_encuestas = property(lambda p: p.respuesta_set.count())

Persona.ultima_encuesta = property(lambda p: p.respuesta_set[-1])


def get_login(turno, usuario):
    inicio = turno.login_inicio()
    fin = turno.login_fin()

    return Login.objects.filter(user=usuario, created__range=(inicio, fin))


def get_current_month_logins_list(user):
    fin, inicio = get_current_month_range()
    return Login.objects.filter(created__range=(inicio, fin), user=user)


def get_current_month_logins(user):
    fin, inicio = get_current_month_range()
    query = Login.objects.filter(created__range=(inicio, fin), user=user)

    value = {
        'normal': query.filter(holiday=False).count(),
        'festivos': query.filter(holiday=True).count(),
    }

    return value


UserProfile.get_current_month_logins = property(
    lambda p: get_current_month_logins(p.user))

UserProfile.get_current_month_logins_list = property(
    lambda p: get_current_month_logins_list(p.user))
