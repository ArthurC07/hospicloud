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
from collections import defaultdict

from constance import config
from django.db import models
from django.utils import timezone
from django_extensions.db.models import TimeStampedModel
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from inventory.models import ItemTemplate, Inventario, ItemType
from persona.models import Persona, transfer_object_to_persona, \
    persona_consolidation_functions


class Localidad(TimeStampedModel):
    nombre = models.CharField(max_length=50, blank=True, null=True)
    habilitado = models.BooleanField(default=True)

    def __unicode__(self):
        return self.nombre


class Afeccion(TimeStampedModel):
    codigo = nombre = models.CharField(max_length=50)
    nombre = models.CharField(max_length=50, blank=True, null=True)
    habilitado = models.BooleanField(default=True)

    def __unicode__(self):
        return self.nombre


class Especialidad(TimeStampedModel):
    nombre = models.CharField(max_length=50)
    habilitado = models.BooleanField(default=True)

    def __unicode__(self):
        return self.nombre


class TipoConsulta(models.Model):
    tipo = models.CharField(max_length=50)
    habilitado = models.BooleanField(default=True)
    facturable = models.BooleanField(default=True)

    def __unicode__(self):
        return self.tipo


class Consultorio(TimeStampedModel):
    class Meta:
        permissions = (
            ('consultorio', 'Permite al usuario gestionar consultorios'),
        )
        ordering = ["nombre", ]

    nombre = models.CharField(max_length=50, blank=True, null=True)
    usuario = models.ForeignKey(User, related_name='consultorios')
    secretaria = models.ForeignKey(User, related_name='secretarias')
    inventario = models.ForeignKey(Inventario, related_name='consultorios',
                                   blank=True, null=True)
    administradores = models.ManyToManyField(User, blank=True,
                                             related_name='consultorios_administrados')
    localidad = models.ForeignKey(Localidad, related_name='consultorios',
                                  blank=True, null=True)
    especialidad = models.ForeignKey(Especialidad, related_name='consultorios',
                                     blank=True, null=True)
    activo = models.BooleanField(default=True)

    def __unicode__(self):
        return self.nombre

    def get_absolute_url(self):
        """Obtiene la URL absoluta"""

        return reverse('consultorio', args=[self.id])


class Paciente(TimeStampedModel):
    """Relaciona a una :class:`Persona` con un :class:`Doctor` para
    ayudar a proteger la privacidad de dicha :class:`Persona` ya que se
    restringe el acceso a la información básica y a los datos ingresados por
    el :class:`User` al que pertenece el :class:`Consultorio`"""

    persona = models.ForeignKey(Persona, related_name='pacientes')
    consultorio = models.ForeignKey(Consultorio, related_name='pacientes',
                                    blank=True, null=True)

    def __unicode__(self):
        return u"Paciente {0} de {1}".format(self.persona.nombre_completo(),
                                             self.consultorio.usuario.get_full_name())

    def identificacion(self):
        return self.persona.identificacion

    def nombre(self):
        return self.persona.nombre_completo()

    def get_absolute_url(self):
        """Obtiene la url relacionada con un :class:`Paciente`"""

        return reverse('clinique-paciente', args=[self.id])


class Consulta(TimeStampedModel):
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

    def get_absolute_url(self):
        """Obtiene la URL absoluta"""

        return self.persona.get_absolute_url()

    def item(self):

        item = None
        for contrato in self.persona.contratos.filter(
                vencimiento__gte=timezone.now()).all():
            item = contrato.plan.consulta

        if item is None:
            item = ItemTemplate.objects.get(pk=config.DEFAULT_CONSULTA_ITEM)

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

            for contrato in self.persona.contratos.filter(
                    vencimiento__gte=timezone.now()).all():
                precios[cargo.item] = contrato.obtener_cobro(cargo.item)

            print precios[cargo.item]
            cargo.facturado = True
            cargo.save()

        return items, precios


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
    """Registra los análisis que se le efectua a la :class:`Persona`"""
    persona = models.ForeignKey(Persona, related_name='evaluaciones',
                                blank=True, null=True)
    usuario = models.ForeignKey(User, related_name='evaluaciones',
                                blank=True, null=True)
    consulta = models.ForeignKey(Consulta, related_name='evaluaciones',
                                 blank=True, null=True)
    orl = models.TextField()
    cardiopulmonar = models.TextField()
    gastrointestinal = models.TextField()
    extremidades = models.TextField()
    otras = models.TextField()

    def get_absolute_url(self):
        """Obtiene la url relacionada con un :class:`Paciente`"""

        return self.consulta.get_absolute_url()


class Cita(TimeStampedModel):
    """Permite registrar las posibles :class:`Personas`s que serán atendidas
    en una fecha determinada"""

    consultorio = models.ForeignKey(Consultorio, related_name='citas',
                                    blank=True, null=True)
    persona = models.ForeignKey(Persona, related_name='citas', blank=True,
                                null=True)
    fecha = models.DateTimeField(blank=True, null=True, default=timezone.now)
    ausente = models.BooleanField(default=False)
    atendida = models.BooleanField(default=False)

    def get_absolute_url(self):
        """Obtiene la URL absoluta"""

        return self.consultorio.get_absolute_url()

    def __unicode__(self):
        return u'{0}'.format(self.persona.nombre_completo())

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
    usuario = models.ForeignKey(User, related_name='seguimientos')

    def get_absolute_url(self):
        """Obtiene la url relacionada con un :class:`Paciente`"""

        return self.persona.get_absolute_url()


class DiagnosticoClinico(TimeStampedModel):
    persona = models.ForeignKey(Persona, related_name='diagnosticos_clinicos',
                                blank=True, null=True)
    usuario = models.ForeignKey(User, related_name='diagnosticos_clinicos',
                                blank=True, null=True)
    afeccion = models.ForeignKey(Afeccion, related_name='diagnosticos_clinicos',
                                 blank=True, null=True)
    consulta = models.ForeignKey(Consulta, related_name='diagnosticos_clinicos',
                                 blank=True, null=True)
    diagnostico = models.TextField(blank=True, null=True)

    def get_absolute_url(self):
        """Obtiene la url relacionada con un :class:`Paciente`"""

        return self.consulta.get_absolute_url()


class OrdenMedica(TimeStampedModel):
    """Registra las indicaciones dadas al paciente de parte del
    :class:`Doctor`"""

    persona = models.ForeignKey(Persona, related_name='ordenes_medicas',
                                blank=True, null=True)
    usuario = models.ForeignKey(User, related_name='ordenes_clinicas',
                                blank=True, null=True)
    consulta = models.ForeignKey(Consulta, related_name='ordenes_medicas',
                                 blank=True, null=True)
    evolucion = models.TextField(blank=True)
    orden = models.TextField(blank=True)
    medicamento = models.ForeignKey(ItemTemplate, blank=True, null=True,
                                    related_name='ordenes_medicas')
    farmacia = models.BooleanField(default=False)
    facturada = models.BooleanField(default=False)

    def get_absolute_url(self):
        """Obtiene la url relacionada con un :class:`Paciente`"""

        return self.persona.get_absolute_url()


class TipoCargo(TimeStampedModel):
    """Permite Diferenciar entre los distintos tipos de :class:`Cargo` que se
    pueden agregar a un :class:`Paciente`"""

    nombre = models.CharField(max_length=200, blank=True)
    descontable = models.BooleanField(default=True)

    def __unicode__(self):
        return self.nombre


class Cargo(TimeStampedModel):
    """Permite registrar diversos cobros durante una :class:`Consulta`"""
    consulta = models.ForeignKey(Consulta, related_name='cargos', blank=True,
                                 null=True)
    usuario = models.ForeignKey(User, related_name='cargos_clinicos',
                                blank=True,
                                null=True)
    tipo = models.ForeignKey(ItemType, related_name='cargos')
    item = models.ForeignKey(ItemTemplate, related_name='consultorio_cargos')
    cantidad = models.IntegerField(default=1)
    facturado = models.BooleanField(default=False)

    def get_absolute_url(self):
        """Obtiene la url relacionada con un :class:`Paciente`"""

        return self.consulta.persona.get_absolute_url()


class NotaEnfermeria(TimeStampedModel):
    """Nota agregada a una :class:`Admision` por el personal de Enfermeria"""

    persona = models.ForeignKey(Persona, related_name='notas_enfermeria',
                                blank=True, null=True)
    nota = models.TextField(blank=True)
    usuario = models.ForeignKey(User, blank=True, null=True,
                                related_name='consultorio_notas_enfermeria')

    def get_absolute_url(self):
        """Obtiene la url relacionada con un :class:`Paciente`"""

        return self.persona.get_absolute_url()


class Examen(TimeStampedModel):
    """Nota agregada a una :class:`Admision` por el personal de Enfermeria"""

    paciente = models.ForeignKey(Paciente, related_name='consultorio_examenes')
    descripcion = models.TextField(blank=True)
    adjunto = models.FileField(upload_to="clinique/examen/%Y/%m/%d")

    def get_absolute_url(self):
        """Obtiene la url relacionada con un :class:`Paciente`"""

        return self.paciente.get_absolute_url()


class Espera(TimeStampedModel):
    consultorio = models.ForeignKey(Consultorio, related_name='espera',
                                    blank=True, null=True)
    persona = models.ForeignKey(Persona, related_name='espera')
    fecha = models.DateTimeField(auto_now_add=True)
    atendido = models.BooleanField(default=False)
    ausente = models.BooleanField(default=False)
    consulta = models.BooleanField(default=False)
    inicio = models.DateTimeField(auto_now_add=True)
    terminada = models.BooleanField(default=False)
    fin = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u"{0} en {1}".format(self.persona.nombre_completo(),
                                    self.consultorio.nombre)

    def get_absolute_url(self):
        return self.consultorio.get_absolute_url()

    def tiempo(self):
        delta = timezone.now() - self.created

        return delta.seconds / 60


class Prescripcion(TimeStampedModel):
    persona = models.ForeignKey(Persona, related_name='prescripciones',
                                blank=True, null=True)
    usuario = models.ForeignKey(User, related_name='prescripciones',
                                blank=True, null=True)
    consulta = models.ForeignKey(Consulta, related_name='prescripciones',
                                 blank=True, null=True)
    medicamento = models.ForeignKey(ItemTemplate, related_name='prescripciones',
                                    blank=True, null=True)
    nota = models.TextField(blank=True, verbose_name=u'Otros MEdicamentos')

    def __unicode__(self):
        return self.persona.nombre_completo()

    def get_absolute_url(self):
        return self.consulta.get_absolute_url()


class Incapacidad(TimeStampedModel):
    persona = models.ForeignKey(Persona, related_name='incapacidades',
                                blank=True, null=True)
    usuario = models.ForeignKey(User, related_name='incapacidades',
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


def consolidate_clinique(persona, clone):
    [transfer_object_to_persona(consulta, persona) for consulta in
     clone.consultas.all()]

    [transfer_object_to_persona(incapacidad, persona) for incapacidad in
     clone.incapacidades.all()]

    [transfer_object_to_persona(diagnostico, persona) for diagnostico in
     clone.diagnosticos_clinicos.all()]

    [transfer_object_to_persona(evaluacion, persona) for evaluacion in
     clone.evaluaciones.all()]

    [transfer_object_to_persona(orden, persona) for orden in
     clone.ordenes_medicas.all()]

    [transfer_object_to_persona(espera, persona) for espera in
     clone.espera.all()]

    [transfer_object_to_persona(signos, persona) for signos in
     clone.lecturas_signos.all()]

    [transfer_object_to_persona(cita, persona) for cita in
     clone.citas.all()]

    [transfer_object_to_persona(remision, persona) for remision in
     clone.remisiones.all()]


persona_consolidation_functions.append(consolidate_clinique)

User.consultorios_activos = property(
    lambda u: Consultorio.objects.filter(usuario=u, activo=True))

Persona.consultas_activas = property(
    lambda p: Consulta.objects.filter(persona=p, activa=True))

Persona.ultima_consulta = property(
    lambda p: Consulta.objects.filter(persona=p).last())
