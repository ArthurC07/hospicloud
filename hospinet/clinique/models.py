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

from django.db import models
from django.utils import timezone
from django_extensions.db.models import TimeStampedModel
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from inventory.models import ItemTemplate, Inventario
from persona.models import Persona


class TipoConsulta(models.Model):
    tipo = models.CharField(max_length=50)

    def __unicode__(self):
        return self.tipo


class Consultorio(TimeStampedModel):
    class Meta:
        permissions = (
            ('consultorio', 'Permite al usuario gestionar consultorios'),
        )

    nombre = models.CharField(max_length=50, blank=True, null=True)
    usuario = models.ForeignKey(User, related_name='consultorios')
    secretaria = models.ForeignKey(User, related_name='secretarias')
    inventario = models.ForeignKey(Inventario, related_name='consultorios',
                                   blank=True, null=True)
    administradores = models.ManyToManyField(User, blank=True, null=True,
                                             related_name='consultorios_administrados')

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

        return reverse('clinique-paciente-resume', args=[self.id])


class Consulta(TimeStampedModel):
    paciente = models.ForeignKey(Paciente, related_name='consultas')
    tipo = models.ForeignKey(TipoConsulta, related_name='consultas')

    def get_absolute_url(self):
        """Obtiene la URL absoluta"""

        return reverse('clinique-paciente', args=[self.paciente.id])


class LecturaSignos(TimeStampedModel):
    persona = models.ForeignKey(Persona, related_name='lecturas_signos',
                                null=True)
    pulso = models.IntegerField()
    temperatura = models.DecimalField(decimal_places=2, max_digits=8,
                                      null=True)
    presion_sistolica = models.DecimalField(decimal_places=2, max_digits=8,
                                            null=True)
    presion_diastolica = models.DecimalField(decimal_places=2, max_digits=8,
                                             null=True)
    respiracion = models.DecimalField(decimal_places=2, max_digits=8, null=True)
    presion_arterial_media = models.CharField(max_length=200, blank=True)

    def get_absolute_url(self):
        """Obtiene la URL absoluta"""

        return reverse('persona-view-id', args=[self.persona.id])

    def save(self, *args, **kwargs):
        """Permite guardar los datos mientras calcula algunos campos
        automaticamente"""

        self.presion_arterial_media = float(self.presion_diastolica) + (
            float(1) / float(3) * float(self.presion_sistolica -
                                        self.presion_diastolica))

        super(LecturaSignos, self).save(*args, **kwargs)


class Evaluacion(TimeStampedModel):
    """Registra los análisis que se le efectua a la :class:`Persona`"""

    paciente = models.ForeignKey(Paciente, related_name='evaluaciones')
    orl = models.TextField()
    cardiopulmonar = models.TextField()
    gastrointestinal = models.TextField()
    extremidades = models.TextField()
    otras = models.TextField()

    def get_absolute_url(self):
        """Obtiene la url relacionada con un :class:`Paciente`"""

        return self.paciente.get_absolute_url()


class Cita(TimeStampedModel):
    """Permite registrar las posibles :class:`Personas`s que serán atendidas
    en una fecha determinada"""

    consultorio = models.ForeignKey(Consultorio, related_name='citas',
                                    blank=True, null=True)
    persona = models.ForeignKey(Persona, related_name='citas', blank=True,
                                null=True)
    fecha = models.DateTimeField(blank=True, null=True, default=timezone.now)
    ausente = models.BooleanField(default=False)

    def get_absolute_url(self):
        """Obtiene la URL absoluta"""

        return reverse('consultorio-cita-list', args=[self.consultorio.id])


class Seguimiento(TimeStampedModel):
    """Representa las consultas posteriores que sirven como seguimiento a la
    dolencia original"""

    paciente = models.ForeignKey(Paciente, related_name='seguimientos')
    observaciones = models.TextField()
    usuario = models.ForeignKey(User, related_name='seguimientos')

    def get_absolute_url(self):
        """Obtiene la url relacionada con un :class:`Paciente`"""

        return self.paciente.get_absolute_url()


class DiagnosticoClinico(TimeStampedModel):
    paciente = models.ForeignKey(Paciente, related_name='diagnosticos_clinicos')
    diagnostico = models.TextField()

    def get_absolute_url(self):
        """Obtiene la url relacionada con un :class:`Paciente`"""

        return reverse('clinique-paciente', args=[self.paciente.id])


class OrdenMedica(TimeStampedModel):
    """Registra las indicaciones dadas al paciente de parte del
    :class:`Doctor`"""

    paciente = models.ForeignKey(Paciente, related_name='ordenes_medicas')
    evolucion = models.TextField(blank=True)
    orden = models.TextField(blank=True)

    def get_absolute_url(self):
        """Obtiene la url relacionada con un :class:`Paciente`"""

        return self.paciente.get_absolute_url()


class TipoCargo(TimeStampedModel):
    """Permite Diferenciar entre los distintos tipos de :class:`Cargo` que se
    pueden agregar a un :class:`Paciente`"""

    nombre = models.CharField(max_length=200, blank=True)
    descontable = models.BooleanField(default=True)

    def __unicode__(self):
        return self.nombre


class Cargo(TimeStampedModel):
    """Permite registrar diversos cobros a un :class:`Paciente`"""

    paciente = models.ForeignKey(Paciente, related_name='cargos')
    tipo = models.ForeignKey(TipoCargo, related_name='cargos')
    item = models.ForeignKey(ItemTemplate, related_name='consultorio_cargos')
    cantidad = models.IntegerField(default=1)

    def get_absolute_url(self):
        """Obtiene la url relacionada con un :class:`Paciente`"""

        return self.paciente.get_absolute_url()


class NotaEnfermeria(TimeStampedModel):
    """Nota agregada a una :class:`Admision` por el personal de Enfermeria"""

    paciente = models.ForeignKey(Paciente, related_name='notas_enfermeria')
    nota = models.TextField(blank=True)
    usuario = models.ForeignKey(User, blank=True, null=True,
                                related_name='consultorio_notas_enfermeria')

    def get_absolute_url(self):
        """Obtiene la url relacionada con un :class:`Paciente`"""

        return self.paciente.get_absolute_url()


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
    fecha = models.DateTimeField(default=timezone.now)
    atendido = models.BooleanField(default=False)
    ausente = models.BooleanField(default=False)

    def get_absolute_url(self):

        return self.consultorio.get_absolute_url()

    def tiempo(self):

        delta = timezone.now() - self.created

        return delta.seconds


class Prescripcion(TimeStampedModel):
    paciente = models.ForeignKey(Paciente, related_name='prescripciones')
    nota = models.TextField(blank=True)

    def __unicode__(self):

        return self.paciente.persona.nombre_completo()

    def get_absolute_url(self):

        return self.paciente.get_absolute_url()
