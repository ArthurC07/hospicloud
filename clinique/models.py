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

from collections import defaultdict
from datetime import timedelta

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import QuerySet
from django.db.models.aggregates import Sum
from django.db.models.functions import Coalesce
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel
from mail_templated import EmailMessage

from contracts.models import Contrato, MasterContract
from inventory.models import ItemTemplate, Inventario, ItemType
from persona.models import Persona, HistoriaFisica, transfer_object_to_persona, \
    persona_consolidation_functions
from users.models import Ciudad


@python_2_unicode_compatible
class Localidad(TimeStampedModel):
    nombre = models.CharField(max_length=50, blank=True, null=True)
    habilitado = models.BooleanField(default=True)
    ciudad = models.ForeignKey(Ciudad, blank=True, null=True)

    def __str__(self):
        return self.nombre


@python_2_unicode_compatible
class Afeccion(TimeStampedModel):
    codigo = models.CharField(max_length=50)
    nombre = models.CharField(max_length=255, blank=True, null=True)
    habilitado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


@python_2_unicode_compatible
class Especialidad(TimeStampedModel):
    nombre = models.CharField(max_length=50)
    habilitado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


@python_2_unicode_compatible
class TipoConsulta(models.Model):
    tipo = models.CharField(max_length=50)
    habilitado = models.BooleanField(default=True)
    facturable = models.BooleanField(default=True)

    def __str__(self):
        return self.tipo


@python_2_unicode_compatible
class Consultorio(TimeStampedModel):
    class Meta:
        permissions = (
            ('consultorio', 'Permite al usuario gestionar consultorios'),
            ('clinical_read',
             _('Permite que el usuario tenga acceso a los datos clínicos')),
            ('clinical_write',
             _('Permite que el usuario escriba a los datos clínicos')),
            ('clinical_manage',
             _('Permite que el usuario escriba a los datos clínicos')),
        )
        ordering = ["nombre", ]

    nombre = models.CharField(max_length=50, blank=True, null=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL,
                                related_name='consultorios')
    secretaria = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   related_name='secretarias')
    inventario = models.ForeignKey(Inventario, related_name='consultorios',
                                   blank=True, null=True)
    administradores = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                             blank=True,
                                             related_name='consultorios_administrados')
    localidad = models.ForeignKey(Localidad, related_name='consultorios',
                                  blank=True, null=True)
    especialidad = models.ForeignKey(Especialidad, related_name='consultorios',
                                     blank=True, null=True)
    activo = models.BooleanField(default=True)
    especialista = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        """Obtiene la URL absoluta"""

        return reverse('consultorio', args=[self.id])

    def consultas_remitidas(self):
        return Consulta.objects.filter(remitida=True, revisada=False)


class EsperaQuerySet(QuerySet):
    """
    Contains comon queries made to :class:`Espera`
    """

    def pendientes(self):
        """
        Returns all the class:`Espera`s that have not been yet attended
        """
        return self.filter(
            consulta=False,
            terminada=False,
            atendido=False,
            ausente=False,
            datos=False
        )

    def en_consulta(self):
        """
        Returns all the :class:`Espera` that are in the physician's office
        """
        return self.filter(
            consulta=True,
            terminada=False,
            ausente=False,
            atendido=False,
        )

    def espera_consulta(self):
        """
        Returns all the :class:`Espera` that are been taked physical history
        """
        return self.filter(
            consulta=False,
            terminada=False,
            ausente=False,
            atendido=False,
            datos=True
        )


@python_2_unicode_compatible
class Espera(TimeStampedModel):
    """
    Represents a :class:`Persona` that is waiting for a physician to consult to
    """
    consultorio = models.ForeignKey(Consultorio, related_name='espera',
                                    blank=True, null=True)
    persona = models.ForeignKey(Persona, related_name='espera')
    poliza = models.ForeignKey(MasterContract, blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)
    inicio = models.DateTimeField(default=timezone.now)
    fin = models.DateTimeField(default=timezone.now)
    terminada = models.BooleanField(default=False)
    atendido = models.BooleanField(default=False)
    ausente = models.BooleanField(default=False)
    consulta = models.BooleanField(default=False)
    datos = models.BooleanField(default=False)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
    ciudad = models.ForeignKey(Ciudad, blank=True, null=True)

    # Tracking several different moments of the waiting room experience
    tiempo_sap = models.DurationField(default=timedelta)
    tiempo_datos = models.DurationField(default=timedelta)
    tiempo_enfermeria = models.DurationField(default=timedelta)
    tiempo_consultorio = models.DurationField(default=timedelta)

    inicio_sap = models.DateTimeField(default=timezone.now)
    fin_sap = models.DateTimeField(default=timezone.now)
    inicio_datos = models.DateTimeField(default=timezone.now)
    fin_datos = models.DateTimeField(default=timezone.now)
    inicio_enfermeria = models.DateTimeField(default=timezone.now)
    fin_enfermeria = models.DateTimeField(default=timezone.now)
    inicio_doctor = models.DateTimeField(default=timezone.now)
    fin_consultorio = models.DateTimeField(default=timezone.now)

    duracion_total = models.DurationField(default=timedelta)

    objects = EsperaQuerySet.as_manager()

    class Meta:
        ordering = ['created', ]

    def __str__(self):
        if self.consultorio:
            string = _("{0} en {1}").format(self.persona.nombre_completo(),
                                            self.consultorio.nombre)
        else:
            string = self.persona.nombre_completo()
        return string

    def get_absolute_url(self):
        return reverse('consultorio-index')

    def tiempo(self):
        return timezone.now() - self.created


class HistoriaFisicaEspera(TimeStampedModel):
    """
    Relates a :class:`Espera` to a :class`HistoriaFisica` while allowing both
    classes to be completely independent
    """
    espera = models.ForeignKey(Espera)
    historia_fisica = models.ForeignKey(HistoriaFisica)

    def get_absolute_url(self):
        return self.espera.get_absolute_url()


class ConsultaQuerySet(models.QuerySet):
    """
    Creates shortcuts for many common :class:`Consulta` operations
    """

    def pendientes_encuesta(self):
        """
        Obtains all :class:`Consulta`s that have not been polled yet.
        """
        return self.filter(
            encuestada=False,
            no_desea_encuesta=False,
        )

    def atendidas(self, inicio, fin):
        """
        Obtains the :class:`Consulta`s that have been created between two dates
        """
        return self.filter(
            created__range=(inicio, fin)
        )


@python_2_unicode_compatible
class Consulta(TimeStampedModel):
    """
    Registra la interacción entre una :class:`Persona` y un :class:`Usuario`
    que es un médico.
    """
    persona = models.ForeignKey(Persona, related_name='consultas',
                                blank=True, null=True)
    consultorio = models.ForeignKey(Consultorio, related_name='consultas',
                                    blank=True, null=True)
    tipo = models.ForeignKey(TipoConsulta, related_name='consultas')
    motivo_de_consulta = models.TextField(default=None, null=True)
    HEA = models.TextField(default=None, null=True)
    facturada = models.BooleanField(default=False)
    activa = models.BooleanField(default=True)
    final = models.DateTimeField(blank=True, null=True)
    remitida = models.BooleanField(default=False)
    encuestada = models.BooleanField(default=False)
    no_desea_encuesta = models.BooleanField(default=False)
    revisada = models.BooleanField(default=False)
    espera = models.ForeignKey(Espera, blank=True, null=True,
                               related_name='consulta_set')
    poliza = models.ForeignKey(MasterContract, blank=True, null=True)
    contrato = models.ForeignKey(Contrato, blank=True, null=True)
    duracion = models.DurationField(default=timedelta)

    objects = ConsultaQuerySet.as_manager()

    class Meta:
        ordering = ['created', ]

    def __str__(self):

        return _('Consulta de {0}').format(self.persona.nombre_completo())

    def get_absolute_url(self):
        """Obtiene la URL absoluta"""

        return self.persona.get_absolute_url()

    def item(self):
        item = None
        if self.contrato:
            item = self.contrato.plan.consulta

        if item is None:
            item = self.consultorio.usuario.profile.honorario

        return item

    def facturar(self):
        """Permite convertir los :class:`Cargo`s de esta :class:`Admision` en
        las :class:`Venta`s de un :class:`Recibo`"""

        items = defaultdict(int)
        precios = defaultdict(int)
        item = self.item()

        items[item] += 1
        precios[item] += item.precio_de_venta

        for cargo in self.cargos.all():
            items[cargo.item] += cargo.cantidad
            precios[cargo.item] = cargo.item.precio_de_venta
            if self.contrato:
                precios[cargo.item] = self.contrato.obtener_cobro(cargo.item)

        self.cargos.update(facturado=True)

        return items, precios

    def total_incapacidad(self):

        return self.incapacidades.aggregate(total=Coalesce(Sum('dias'), 0))[
            'total']

    def total_time(self):
        """
        Calculates the total time a :class:`Persona` has spent between
        :class`Espera` start and :class:`Consulta` ending.
        """

        if self.espera:
            return (self.espera.created - self.final).seconds / 60

        else:
            return (self.created - self.final).seconds / 60

    def current_time(self):
        """
        Calculates the total time a :class:`Consulta` has spent between
        :class`Consulta` start and Now.
        """
        time = timezone.now() - self.created
        total_seconds = time.total_seconds()

        minutes = (total_seconds % 3600) // 60
        hours = total_seconds // 3600
        seconds = int(total_seconds)
        delta = {"hours": 0, "minutes": 0, "seconds": seconds}
        if total_seconds > 60:
            seconds = int(total_seconds % 60)
            minutes = int(minutes)
            delta = {"hours": 0, "minutes": minutes, "seconds": seconds}
        if total_seconds > 3600:
            hours = int(hours)
            minutes = int(minutes % 60)
            seconds = int(total_seconds % 60)
            delta = {"hours": hours, "minutes": minutes, "seconds": seconds}

        return delta

    def save(self, **kwargs):

        if self.contrato is None and self.poliza:
            contrato = self.persona.contratos.filter(
                master=self.poliza
            ).first()
            if contrato is None:
                beneficiario = self.persona.beneficiarios.filter(
                    contrato__master=self.poliza
                ).first()
                if beneficiario is not None:
                    contrato = beneficiario.contrato

            self.contrato = contrato

        super(Consulta, self).save(**kwargs)

    def titularDependiente(self):
        try:
            is_beneficiario = False
            personas = [b.persona for b in self.contrato.beneficiarios.all()]
            if self.persona in personas:
                is_beneficiario = True

            if self.contrato.persona == self.persona:
                return 'Titular'
            elif is_beneficiario:
                return 'Dependiente'
            else:
                return ''
        except:
            return ''


class LecturaSignos(TimeStampedModel):
    persona = models.ForeignKey(Persona, related_name='lecturas_signos',
                                null=True)
    pulso = models.IntegerField()
    temperatura = models.DecimalField(decimal_places=2, max_digits=8,
                                      null=True)
    presion_sistolica = models.IntegerField(null=True)
    presion_diastolica = models.IntegerField(null=True)
    respiracion = models.IntegerField(null=True)
    presion_arterial_media = models.CharField(max_length=200, blank=True)

    def get_absolute_url(self):
        """Obtiene la URL absoluta"""

        return self.persona.get_absolute_url()

    def save(self, *args, **kwargs):
        """Permite guardar los datos mientras calcula algunos campos
        automaticamente"""

        self.presion_arterial_media = float(self.presion_diastolica) + (
            float(1) / float(3) * float(self.presion_sistolica -
                                        self.presion_diastolica))

        super(LecturaSignos, self).save(*args, **kwargs)


class Evaluacion(TimeStampedModel):
    """
    Registra los análisis que se le efectua a la :class:`Persona`
    """

    ASPECTO = (
        ('L', _('Lucido')),
        ('C', _('Consciente')),
        ('O', _('Orientado')),
    )

    NORMALIDAD = (
        ('N', _('Normal')),
        ('A', _('Anormal')),
    )

    SIMETRIA = (
        ('S', _('Simétrico')),
        ('A', _('Asimétrico')),
    )

    persona = models.ForeignKey(Persona, related_name='evaluaciones',
                                blank=True, null=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL,
                                related_name='evaluaciones',
                                blank=True, null=True)
    consulta = models.ForeignKey(Consulta, related_name='evaluaciones',
                                 blank=True, null=True)
    lucido = models.BooleanField(default=True)
    consciente = models.BooleanField(default=True)
    orientado = models.BooleanField(default=True)
    cabeza = models.CharField(max_length=1, choices=NORMALIDAD, default='N')
    descripcion_cabeza = models.TextField(blank=True)
    ojos = models.CharField(max_length=1, choices=NORMALIDAD, default='N')
    descripcion_ojos = models.TextField(blank=True)
    cuello = models.CharField(max_length=1, choices=NORMALIDAD, default='N')
    descripcion_cuello = models.TextField(blank=True)
    pulmones_ventilados = models.BooleanField(default=True)
    pulmones_crepitos = models.BooleanField(default=False)
    pulmones_subcrepitos = models.BooleanField(default=False)
    pulmones_roncus = models.BooleanField(default=False)
    civilancias = models.BooleanField(default=False)
    matides = models.BooleanField(default=False)
    primer_ruido_cardiaco = models.BooleanField(default=True)
    segundo_ruido_cardiaco = models.BooleanField(default=True)
    tercer_ruido_cardiaco = models.BooleanField(default=False)
    cuarto_ruido_cardiaco = models.BooleanField(default=False)
    soplo = models.BooleanField(default=False)
    arritmia = models.BooleanField(default=False)
    orl = models.CharField(max_length=1, choices=NORMALIDAD, default='N')
    descripcion_orl = models.TextField(blank=True)
    mamas_normales = models.BooleanField(default=True)
    nodulos = models.BooleanField(default=False)
    retracciones_mamarias = models.BooleanField(default=False)
    nopatias_satelites = models.BooleanField(default=False)
    abdomen_blando = models.BooleanField(default=True)
    abdomen_deprecible = models.BooleanField(default=True)
    dolor_abdominal = models.BooleanField(default=False)
    blumber = models.BooleanField(default=False)
    rovsig = models.BooleanField(default=False)
    gastrointestinal = models.TextField(blank=True)
    tacto_rectal_diferido = models.BooleanField(default=True)
    hallazgos_tacto_rectal = models.TextField(blank=True)
    genitales_normales = models.BooleanField(default=True)
    hallazgos_genitales = models.TextField(blank=True)
    extremidades_simetricas = models.BooleanField(default=True)
    hallazgos_extremidades = models.TextField(blank=True)
    piel_normal = models.BooleanField(default=True)
    hallazgos_piel = models.TextField(blank=True)
    neurologico_normal = models.BooleanField(default=True)
    focalizaciones = models.BooleanField(default=False)
    atonia = models.BooleanField(default=False)
    disminucion_de_la_fuerza = models.BooleanField(default=False)
    movimientos_involuntarios = models.BooleanField(default=False)
    otras = models.TextField(blank=True)

    def get_absolute_url(self):
        """Obtiene la url relacionada con un :class:`Paciente`"""

        return self.consulta.get_absolute_url()


@python_2_unicode_compatible
class Cita(TimeStampedModel):
    """Permite registrar las posibles :class:`Personas`s que serán atendidas
    en una fecha determinada"""

    consultorio = models.ForeignKey(Consultorio, related_name='citas',
                                    blank=True, null=True)
    persona = models.ForeignKey(Persona, related_name='citas', blank=True,
                                null=True)
    tipo = models.ForeignKey(TipoConsulta, blank=True, null=True)
    fecha = models.DateTimeField(blank=True, null=True, default=timezone.now)
    ausente = models.BooleanField(default=False)
    atendida = models.BooleanField(default=False)

    def get_absolute_url(self):
        """Obtiene la URL absoluta"""

        return self.consultorio.get_absolute_url()

    def __str__(self):
        return '{0}'.format(self.persona.nombre_completo())

    def to_espera(self):
        espera = Espera()
        espera.consultorio = self.consultorio
        espera.persona = self.persona
        self.atendida = True
        self.save()

        return espera


class Seguimiento(TimeStampedModel):
    """Representa las consultas posteriores que sirven como seguimiento a la
    dolencia original"""

    persona = models.ForeignKey(Persona, related_name='seguimientos',
                                blank=True, null=True)
    consultorio = models.ForeignKey(Consultorio, related_name='seguimientos',
                                    blank=True, null=True)
    observaciones = models.TextField()
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL,
                                related_name='seguimientos')

    def get_absolute_url(self):
        """Obtiene la url relacionada con un :class:`Paciente`"""

        return self.persona.get_absolute_url()


class DiagnosticoClinico(TimeStampedModel):
    persona = models.ForeignKey(Persona, related_name='diagnosticos_clinicos',
                                blank=True, null=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL,
                                related_name='diagnosticos_clinicos',
                                blank=True, null=True)
    afeccion = models.ForeignKey(Afeccion, related_name='diagnosticos_clinicos',
                                 blank=True, null=True)
    consulta = models.ForeignKey(Consulta, related_name='diagnosticos_clinicos',
                                 blank=True, null=True)
    diagnostico = models.TextField(blank=True, null=True)

    def get_absolute_url(self):
        """Obtiene la url relacionada con un :class:`Paciente`"""

        return self.consulta.get_absolute_url()


@python_2_unicode_compatible
class OrdenMedica(TimeStampedModel):
    """Registra las indicaciones dadas al paciente de parte del
    :class:`Doctor`"""
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL,
                                related_name='ordenes_clinicas',
                                blank=True, null=True)
    consulta = models.ForeignKey(Consulta, related_name='ordenes_medicas',
                                 blank=True, null=True)
    orden = models.TextField(blank=True)
    farmacia = models.BooleanField(default=False)
    facturada = models.BooleanField(default=False)

    def __str__(self):
        if self.consulta is None:
            return self.orden

        return self.consulta.persona.nombre_completo()

    def get_absolute_url(self):
        """Obtiene la url relacionada con un :class:`Paciente`"""

        return self.consulta.get_absolute_url()


@python_2_unicode_compatible
class TipoCargo(TimeStampedModel):
    """Permite Diferenciar entre los distintos tipos de :class:`Cargo` que se
    pueden agregar a un :class:`Paciente`"""

    nombre = models.CharField(max_length=200, blank=True)
    descontable = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class Cargo(TimeStampedModel):
    """Permite registrar diversos cobros durante una :class:`Consulta`"""
    consulta = models.ForeignKey(Consulta, related_name='cargos', blank=True,
                                 null=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL,
                                related_name='cargos_clinicos',
                                blank=True,
                                null=True)
    tipo = models.ForeignKey(ItemType, related_name='cargos')
    item = models.ForeignKey(ItemTemplate, related_name='consultorio_cargos')
    cantidad = models.IntegerField(default=1)
    facturado = models.BooleanField(default=False)

    def get_absolute_url(self):
        """Obtiene la url relacionada con un :class:`Paciente`"""

        return reverse('consultorio-cargo-agregar', args=[self.consulta.id])


class NotaEnfermeria(TimeStampedModel):
    """Nota agregada a una :class:`Admision` por el personal de Enfermeria"""

    persona = models.ForeignKey(Persona, related_name='notas_enfermeria',
                                blank=True, null=True)
    nota = models.TextField(blank=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True,
                                related_name='consultorio_notas_enfermeria')

    def get_absolute_url(self):
        """Obtiene la url relacionada con un :class:`Paciente`"""

        return self.persona.get_absolute_url()


class Examen(TimeStampedModel):
    """Nota agregada a una :class:`Admision` por el personal de Enfermeria"""
    persona = models.ForeignKey(Persona, related_name='clinique_examenes',
                                null=True, blank=True)
    descripcion = models.TextField(blank=True)
    adjunto = models.FileField(upload_to="clinique/examen/%Y/%m/%d")

    def get_absolute_url(self):
        """Obtiene la url relacionada con un :class:`Paciente`"""

        return self.paciente.get_absolute_url()


@python_2_unicode_compatible
class Prescripcion(TimeStampedModel):
    orden = models.ForeignKey(OrdenMedica, blank=True, null=True)
    medicamento = models.ForeignKey(ItemTemplate, related_name='prescripciones',
                                    blank=True, null=True)
    dosis = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.orden.consulta.persona.nombre_completo()

    def get_absolute_url(self):
        return self.orden.get_absolute_url()


class Incapacidad(TimeStampedModel):
    persona = models.ForeignKey(Persona, related_name='incapacidades',
                                blank=True, null=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL,
                                related_name='incapacidades',
                                blank=True, null=True)
    consulta = models.ForeignKey(Consulta, related_name='incapacidades',
                                 blank=True, null=True)
    descripcion = models.TextField()
    dias = models.IntegerField(default=0)

    def get_absolute_url(self):
        return self.consulta.get_absolute_url()


class Reporte(TimeStampedModel):
    consultorio = models.ForeignKey(Consultorio, related_name='reportes',
                                    blank=True, null=True)
    archivo = models.FileField(upload_to='consultorio/reports/%Y/%m/%d')
    fecha = models.DateTimeField(default=timezone.now, null=True, blank=True)

    def get_absolute_url(self):
        return self.consultorio.get_absolute_url()


class TipoRemision(TimeStampedModel):
    nombre = models.CharField(max_length=50)


class Remision(TimeStampedModel):
    tipo = models.ForeignKey(TipoRemision, related_name='remisiones')
    persona = models.ForeignKey(Persona, related_name='remisiones')
    especialidad = models.ForeignKey(Especialidad, related_name='remisiones',
                                     blank=True, null=True)
    consultorio = models.ForeignKey(Consultorio, related_name='remisiones')
    motivo = models.TextField()


class NotaMedica(TimeStampedModel):
    """
    Allows a medic to add some notes about :class:`Persona` behavior
    """
    consulta = models.ForeignKey(Consulta)
    observacion = models.TextField()

    def get_absolute_url(self):
        return self.consulta.get_absolute_url()


@python_2_unicode_compatible
class OrdenLaboratorio(TimeStampedModel):
    """
    Contains a set of exams that the medic indicates to a :class:`Persona`
    """
    consulta = models.ForeignKey(Consulta)
    enviado = models.BooleanField(default=False)

    def __str__(self):
        return self.consulta.persona.nombre_completo()

    def get_absolute_url(self):
        return reverse('clinique-orden-laboratorio', args=[self.id])

    def enviar(self):
        ciudad = self.consulta.consultorio.localidad.ciudad

        correos = [ciudad.company.laboratorios, ]

        correos.extend(ciudad.correo_laboratorio.split())

        message = EmailMessage(
            str('clinique/laboratorio_email.tpl'),
            {
                'examenes': self.ordenlaboratorioitem_set.all(),
                'fecha': timezone.now().date(),
                'persona': self.consulta.persona,
                'doctor': self.consulta.consultorio.usuario.get_full_name(),
            },
            to=correos,
            from_email=settings.EMAIL_HOST_USER
        )
        message.send()

        self.enviado = True
        self.save()


@python_2_unicode_compatible
class OrdenLaboratorioItem(TimeStampedModel):
    """
    Represents an exam a :class:`Persona` was sent to make.
    """
    orden = models.ForeignKey(OrdenLaboratorio)
    item = models.ForeignKey(ItemTemplate)

    def __str__(self):
        return self.item.descripcion

    def get_absolute_url(self):
        return self.orden.get_absolute_url()


def consolidate_clinique(persona, clone):
    [transfer_object_to_persona(consulta, persona) for consulta in
     clone.consultas.all()]

    [transfer_object_to_persona(incapacidad, persona) for incapacidad in
     clone.incapacidades.all()]

    [transfer_object_to_persona(diagnostico, persona) for diagnostico in
     clone.diagnosticos_clinicos.all()]

    [transfer_object_to_persona(evaluacion, persona) for evaluacion in
     clone.evaluaciones.all()]

    [transfer_object_to_persona(espera, persona) for espera in
     clone.espera.all()]

    [transfer_object_to_persona(signos, persona) for signos in
     clone.lecturas_signos.all()]

    [transfer_object_to_persona(cita, persona) for cita in
     clone.citas.all()]

    [transfer_object_to_persona(remision, persona) for remision in
     clone.remisiones.all()]


persona_consolidation_functions.append(consolidate_clinique)

Persona.consultas_activas = property(
    lambda p: Consulta.objects.filter(persona=p, activa=True))

Persona.ultima_consulta = property(
    lambda p: Consulta.objects.filter(persona=p).last())
