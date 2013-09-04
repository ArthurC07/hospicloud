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
from django_extensions.db.models import TimeStampedModel
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from persona.models import Persona


class TipoConsulta(models.Model):
    tipo = models.CharField(max_length=50)

    def __unicode__(self):
        return self.tipo


class Consultorio(TimeStampedModel):
    nombre = models.CharField(max_length=50, blank=True, null=True)
    usuario = models.ForeignKey(User, related_name='consultorios')
    secretaria = models.ForeignKey(User, related_name='secretarias')

    def __unicode__(self):
        return self.nombre


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
                                             self.user.get_full_name())

    def identificacion(self):
        return self.persona.identificacion

    def nombre(self):
        return self.persona.nombre_completo()

    def get_absolute_url(self):
        """Obtiene la url relacionada con un :class:`Paciente`"""

        return reverse('clinique-paciente', args=[self.id])


class Consulta(TimeStampedModel):
    paciente = models.ForeignKey(Paciente, related_name='consultas')
    tipo = models.ForeignKey(TipoConsulta, related_name='consultas')
    padecimiento = models.TextField()

    def get_absolute_url(self):
        """Obtiene la URL absoluta"""

        return reverse('clinique-paciente', args=[self.paciente.id])


class LecturaSignos(TimeStampedModel):
    paciente = models.ForeignKey(Paciente, related_name='signos_vitales')
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

        return reverse('clinique-paciente', args=[self.paciente.id])

    def save(self, *args, **kwargs):
        """Permite guardar los datos mientras calcula algunos campos
        automaticamente"""

        self.presion_arterial_media = float(self.presion_diastolica) + (
            float(1) / float(3) * float(self.presion_sistolica -
                                        self.presion_diastolica))

        super(LecturaSignos, self).save(*args, **kwargs)


class Evaluacion(TimeStampedModel):
    """Registra los análisis que se le efectua a la :class:`Persona`"""

    paciente = models.ForeignKey(Paciente, related_name='examenes_fisicos')
    orl = models.TextField()
    cardiopulmonar = models.TextField()
    gastrointestinal = models.TextField()
    extremidades = models.TextField()
    otras = models.TextField()

    def get_absolute_url(self):
        """Obtiene la url relacionada con un :class:`Paciente`"""

        return reverse('clinique-paciente', args=[self.paciente.id])


class Cita(TimeStampedModel):
    """Permite registrar las posibles :class:`Personas`s que serán atendidas
    en una fecha determinada"""

    usuario = models.ForeignKey(User, related_name='citas')
    nombre = models.CharField(max_length=200)
    fecha = models.DateField(blank=True, null=True)

    def get_absolute_url(self):
        """Obtiene la URL absoluta"""

        return reverse('clinique-citas', args=[self.usuario.id])


class Seguimiento(TimeStampedModel):
    """Representa las consultas posteriores que sirven como seguimiento a la
    dolencia original"""

    paciente = models.ForeignKey(Paciente, related_name='seguimientos')
    observaciones = models.TextField()
    usuario = models.ForeignKey(User, related_name='seguimientos')

    def get_absolute_url(self):
        """Obtiene la url relacionada con un :class:`Paciente`"""

        return reverse('clinique-paciente', args=[self.paciente.id])

class DiagnosticoClinico(TimeStampedModel):
    paciente = models.ForeignKey(Paciente, related_name='diagnosticos_clinicos')
    diagnostico = models.TextField()

    def get_absolute_url(self):
        """Obtiene la url relacionada con un :class:`Paciente`"""

        return reverse('clinique-paciente', args=[self.paciente.id])
