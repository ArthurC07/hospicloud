# -*- coding: utf-8 -*-
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

"""
Modelos básicos necesarios para recabar la información personal de una
:class:`Persona` en la aplicación, permitiendo centralizar las funciones que
se utilizarán a lo largo de todo el sistema
"""
import re
from datetime import date

from django.db import models
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save
from django_extensions.db.models import TimeStampedModel

from persona.fields import OrderedCountryField


class Persona(models.Model):
    """Representación de una :class:`Persona` en la aplicación"""

    class Meta:
        permissions = (
            ('persona', 'Permite al usuario gestionar persona'),
        )

    GENEROS = (
        ('M', u'Masculino'),
        ('F', u'Femenino'),
    )

    ESTADOS_CIVILES = (
        ('S', u'Soltero/a'),
        ('D', u'Divorciado/a'),
        ('C', u'Casado/a'),
        ('U', u'Union Libre')
    )
    TIPOS_IDENTIDAD = (
        ("T", u"Tarjeta de Identidad"),
        ("P", u"Pasaporte"),
        ("L", u"Licencia"),
        ("N", u"Ninguno"),
    )

    __expresion__ = re.compile(r'\d{4}-\d{4}-\d{5}')

    tipo_identificacion = models.CharField(max_length=1,
                                           choices=TIPOS_IDENTIDAD, blank=True)
    identificacion = models.CharField(max_length=20, blank=True, unique=False)
    nombre = models.CharField(max_length=50, blank=True)
    apellido = models.CharField(max_length=50, blank=True)
    sexo = models.CharField(max_length=1, choices=GENEROS, blank=True)
    nacimiento = models.DateField(default=date.today)
    estado_civil = models.CharField(max_length=1, choices=ESTADOS_CIVILES,
                                    blank=True)
    profesion = models.CharField(max_length=200, blank=True)
    telefono = models.CharField(max_length=200, blank=True)
    celular = models.CharField(max_length=200, blank=True)
    domicilio = models.CharField(max_length=200, blank=True)
    email = models.CharField(max_length=200, blank=True)
    fax = models.CharField(max_length=200, blank=True)
    fotografia = models.ImageField(upload_to='persona/foto//%Y/%m/%d',
                                   blank=True, null=True)
    nacionalidad = OrderedCountryField(blank=True, ordered=('HN',))
    duplicado = models.BooleanField(default=False)

    @staticmethod
    def validar_identidad(identidad):

        """Permite validar la identidad ingresada antes de asignarla a una
        :class:`Persona`
        
        :param identidad: Número de identidad a validar
        """

        return Persona.__expresion__.match(identidad)

    def __unicode__(self):

        """Muestra el nombre completo de la persona"""

        return self.nombre_completo()

    def get_absolute_url(self):

        """Obtiene la URL absoluta"""

        return reverse('persona-view-id', args=[self.id])

    def nombre_completo(self):

        """Obtiene el nombre completo de la :class:`Persona`"""

        return u'{0} {1}'.format(self.nombre, self.apellido).upper()

    def obtener_edad(self):

        """Obtiene la edad de la :class:`Persona`"""

        if self.nacimiento is None:
            return None

        today = date.today()
        born = date(self.nacimiento.year,
                    self.nacimiento.month,
                    self.nacimiento.day)
        try:
            # raised when birth date is February 29 and the current year is
            # not a leap year
            birthday = born.replace(year=today.year)
        except ValueError:
            birthday = born.replace(year=today.year, day=born.day - 1)

        if birthday > today:
            return today.year - born.year - 1
        else:
            return today.year - born.year


class Fisico(models.Model):
    """Describe el estado fisico de una :class:`Persona`"""

    TIPOS_SANGRE = (
        ('A', u'A'),
        ('B', u'B'),
        ('AB', u'AB'),
        ('O', u'O'),
    )

    FACTOR_RH = (
        ('+', u'+'),
        ('-', u'-'),
    )

    LATERALIDAD = (
        ('D', u'Derecha'),
        ('I', u'Izquierda'),
    )

    persona = models.OneToOneField(Persona, primary_key=True)
    peso = models.DecimalField(decimal_places=2, max_digits=5, null=True)
    lateralidad = models.CharField(max_length=1, choices=LATERALIDAD,
                                   blank=True)
    altura = models.DecimalField(decimal_places=2, max_digits=5, null=True)

    color_de_ojos = models.CharField(max_length=200, blank=True)
    color_de_cabello = models.CharField(max_length=200, blank=True)
    factor_rh = models.CharField(max_length=1, blank=True, choices=FACTOR_RH)
    tipo_de_sangre = models.CharField(max_length=2, blank=True,
                                      choices=TIPOS_SANGRE)

    def get_absolute_url(self):
        """Obtiene la URL absoluta"""

        return reverse('persona-view-id', args=[self.persona.id])


class EstiloVida(models.Model):
    """Resumen del estilo de vida de una :class:`Persona`"""

    persona = models.OneToOneField(Persona, primary_key=True,
                                   related_name='estilo_vida')
    consume_tabaco = models.BooleanField(default=False, blank=True)
    inicio_consumo_tabaco = models.CharField(max_length=30, blank=True)
    tipo_de_tabaco = models.CharField(max_length=30, blank=True)
    consumo_diario_tabaco = models.IntegerField(null=True)

    # consume_alcohol = models.BooleanField(default=False, blank=True)
    vino = models.BooleanField(default=False, blank=True)
    cerveza = models.BooleanField(default=False, blank=True)
    licor = models.BooleanField(default=False, blank=True)

    cafe = models.BooleanField(default=False, blank=True)
    cantidad_cafe = models.CharField(max_length=200, blank=True)

    dieta = models.CharField(max_length=200, blank=True)
    cantidad = models.CharField(max_length=200, blank=True)
    numero_comidas = models.IntegerField(null=True)
    tipo_de_comidas = models.CharField(max_length=200, blank=True)

    consume_drogas = models.BooleanField(default=False, blank=True)
    drogas = models.CharField(max_length=200, blank=True)
    otros = models.CharField(max_length=200, blank=True)

    def get_absolute_url(self):
        """Obtiene la URL absoluta"""

        return reverse('persona-view-id', args=[self.persona.id])


class Antecedente(models.Model):
    """Describe el historial clínico de una :class:`Persona` al llegar a
    consulta por primera vez
    """

    persona = models.OneToOneField(Persona, primary_key=True)

    # complete = models.BooleanField(default=False, blank=True)
    # reaction = models.BooleanField(default=False, blank=True)

    cardiopatia = models.BooleanField(default=False, blank=True)
    hipertension = models.BooleanField(default=False, blank=True)
    diabetes = models.BooleanField(default=False, blank=True)
    hepatitis = models.BooleanField(default=False, blank=True)
    rinitis = models.BooleanField(default=False, blank=True)
    tuberculosis = models.BooleanField(default=False, blank=True)
    artritis = models.BooleanField(default=False, blank=True)
    asma = models.BooleanField(default=False, blank=True)
    colitis = models.BooleanField(default=False, blank=True)
    gastritis = models.BooleanField(default=False, blank=True)
    sinusitis = models.BooleanField(default=False, blank=True)
    hipertrigliceridemia = models.BooleanField(default=False, blank=True)
    colelitiasis = models.BooleanField(default=False, blank=True)
    migrana = models.NullBooleanField(default=False, blank=True)
    obesidad = models.NullBooleanField(default=False, blank=True)
    colesterol = models.NullBooleanField(default=False, blank=True)
    trigliceridos = models.NullBooleanField(default=False, blank=True)
    alcoholismo = models.NullBooleanField(default=False, blank=True)
    cancer = models.NullBooleanField(default=False, blank=True)
    alergias = models.CharField(max_length=200, blank=True, null=True)

    congenital = models.CharField(max_length=200, blank=True)

    general = models.CharField(max_length=200, blank=True)
    nutricional = models.CharField(max_length=200, blank=True)

    otros = models.CharField(max_length=200, blank=True)

    def get_absolute_url(self):
        """Obtiene la URL absoluta"""

        return reverse('persona-view-id', args=[self.persona.id])


class AntecedenteFamiliar(models.Model):
    """Registra los antecedentes familiares de una :class:`Persona`"""

    persona = models.OneToOneField(Persona, primary_key=True,
                                   related_name='antecedente_familiar')
    sindrome_coronario_agudo = models.BooleanField(default=False, blank=True)
    hipertension = models.BooleanField(default=False, blank=True)
    tabaquismo = models.BooleanField(default=False, blank=True)
    epoc = models.NullBooleanField(default=False, blank=True)
    diabetes = models.BooleanField(default=False, blank=True)
    tuberculosis = models.BooleanField(default=False, blank=True)
    asma = models.BooleanField(default=False, blank=True)
    colitis = models.BooleanField(default=False, blank=True)
    sinusitis = models.BooleanField(default=False, blank=True)
    colelitiasis = models.BooleanField(default=False, blank=True)
    migrana = models.BooleanField(default=False, blank=True)
    obesidad = models.BooleanField(default=False, blank=True)
    dislipidemias = models.BooleanField(default=False, blank=True)
    alcoholismo = models.BooleanField(default=False, blank=True)
    cancer = models.BooleanField(default=False, blank=True)
    alergias = models.CharField(max_length=200, blank=True, null=True)

    congenital = models.CharField(max_length=200, blank=True)

    general = models.CharField(max_length=200, blank=True)
    nutricional = models.CharField(max_length=200, blank=True)
    otros = models.CharField(max_length=200, blank=True)

    def get_absolute_url(self):
        """Obtiene la URL absoluta"""

        return reverse('persona-view-id', args=[self.persona.id])


class AntecedenteObstetrico(models.Model):
    """Registra los antecedentes obstetricos de una :class:`Persona`"""

    persona = models.OneToOneField(Persona, primary_key=True,
                                related_name='antecedente_obstetrico')

    menarca = models.DateField(default=date.today)
    ultimo_periodo = models.DateField(null=True, blank=True)
    displasia = models.BooleanField(default=False, blank=True)
    gestas = models.CharField(max_length=200, blank=True)
    partos = models.CharField(max_length=200, blank=True)
    anticoncepcion = models.CharField(max_length=200, blank=True)
    cesareas = models.CharField(max_length=200, blank=True)
    otros = models.CharField(max_length=200, blank=True)

    def get_absolute_url(self):
        """Obtiene la URL absoluta"""

        return reverse('persona-view-id', args=[self.persona.id])


class Empleador(TimeStampedModel):
    nombre = models.CharField(max_length=200, blank=True)
    direccion = models.TextField()

    def __unicode__(self):

        return self.nombre

    def get_absolute_url(self):

        return reverse('empresa', args=[self.id])


class Sede(TimeStampedModel):
    empleador = models.ForeignKey(Empleador, null=True, blank=True,
                                  related_name='sedes')
    lugar = models.CharField(max_length=200, blank=True)
    direccion = models.TextField()

    def __unicode__(self):

        return u'{0} de {1}'.format(self.lugar, self.empleador.nombre)


class Empleo(TimeStampedModel):
    empleador = models.ForeignKey(Empleador, null=True, blank=True,
                                  related_name='empleos')
    sede = models.ForeignKey(Sede, related_name='empleos', null=True,
                             blank=True)
    persona = models.ForeignKey(Persona, related_name='empleos')
    numero_empleado = models.CharField(max_length=200, blank=True, null=True)

    def get_absolute_url(self):
        return self.persona.get_absolute_url()


class AntecedenteQuirurgico(models.Model):
    """Registra los antecendentes quirurgicos de una :class:`Persona`"""

    persona = models.ForeignKey(Persona, primary_key=True,
                                related_name="antecedentes_quirurgicos")
    procedimiento = models.CharField(max_length=200, blank=True)
    fecha = models.CharField(max_length=200, blank=True)

    def get_absolute_url(self):
        """Obtiene la URL absoluta"""

        return reverse('persona-view-id', args=[self.persona.id])


def create_persona(sender, instance, created, **kwargs):
    if created:
        fisico = Fisico(persona=instance)
        fisico.save()
        estilo_vida = EstiloVida(persona=instance)
        estilo_vida.save()
        antecedente = Antecedente(persona=instance)
        antecedente.save()
        antecedente_familiar = AntecedenteFamiliar(persona=instance)
        antecedente_familiar.save()

        if instance.sexo == 'F':
            antecedente_obstetrico = AntecedenteObstetrico(persona=instance)
            antecedente_obstetrico.save()


post_save.connect(create_persona, sender=Persona)
