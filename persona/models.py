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
from __future__ import unicode_literals

import re
from datetime import date
from decimal import Decimal

from annoying.fields import AutoOneToOneField
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel

from persona.fields import OrderedCountryField


@python_2_unicode_compatible
class Persona(TimeStampedModel):
    """
    Representación de una :class:`Persona` en la aplicación

    Contiene los datos básicos que se utilizan para registar los datos de
    personas reales que se ingresan a la aplicación y de esta manera poder
    relacionarlos con el resto de las actividades que se realizan en la misma.
    """

    class Meta:
        permissions = (
            ('persona', 'Permite al usuario gestionar persona'),
        )
        ordering = ('created',)

    GENEROS = (
        ('M', _('Masculino')),
        ('F', _('Femenino')),
    )

    ESTADOS_CIVILES = (
        ('S', _('Soltero/a')),
        ('D', _('Divorciado/a')),
        ('C', _('Casado/a')),
        ('U', _('Union Libre')),
        ('', _('---------'))
    )
    TIPOS_IDENTIDAD = (
        ("R", _("Carnet de Residencia")),
        ("L", _("Licencia")),
        ("P", _("Pasaporte")),
        ("T", _("Tarjeta de Identidad")),
        ("N", _("Ninguno")),
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
    cargo = models.CharField(max_length=50, blank=True)
    telefono = models.CharField(max_length=200, blank=True)
    celular = models.CharField(max_length=200, blank=True)
    domicilio = models.CharField(max_length=200, blank=True)
    email = models.CharField(max_length=200, blank=True)
    fax = models.CharField(max_length=200, blank=True)
    fotografia = models.ImageField(upload_to='persona/foto//%Y/%m/%d',
                                   blank=True, null=True,
                                   help_text="El archivo debe estar en "
                                             "formato jpg o png y no pesar "
                                             "mas de 120kb")
    nacionalidad = OrderedCountryField(blank=True, ordered=('HN',))
    duplicado = models.BooleanField(default=False)
    rtn = models.CharField(max_length=200, blank=True, null=True)
    mostrar_en_cardex = models.BooleanField(
        default=False,
        verbose_name=_("Es representante legal")
    )
    ciudad = models.ForeignKey("users.Ciudad", blank=True, null=True)

    @staticmethod
    def validar_identidad(identidad):
        """Permite validar la identidad ingresada antes de asignarla a una
        :class:`Persona`
        
        :param identidad: Número de identidad a validar
        """

        return Persona.__expresion__.match(identidad)

    def __str__(self):
        """Muestra el nombre completo de la persona"""

        return self.nombre_completo()

    def get_absolute_url(self):
        """Obtiene la URL absoluta"""

        return reverse('persona-view-id', args=[self.id])

    def nombre_completo(self):
        """Obtiene el nombre completo de la :class:`Persona`"""

        return _('{0} {1}').format(self.nombre, self.apellido).upper()

    def obtener_edad(self):
        """Obtiene la edad de la :class:`Persona`"""

        if self.nacimiento is None:
            return None

        today = date.today()
        born = self.nacimiento
        return today.year - born.year - (
            (today.month, today.day) < (born.month, born.day))


class Fisico(TimeStampedModel):
    """Describe el estado fisico de una :class:`Persona`"""

    TIPOS_SANGRE = (
        ('A', 'A'),
        ('B', 'B'),
        ('AB', 'AB'),
        ('O', 'O'),
    )

    FACTOR_RH = (
        ('+', '+'),
        ('-', '-'),
    )

    LATERALIDAD = (
        ('D', _('Derecha')),
        ('I', _('Izquierda')),
    )

    persona = AutoOneToOneField(Persona, primary_key=True)
    peso = models.DecimalField(decimal_places=2, max_digits=5, default=Decimal)
    lateralidad = models.CharField(max_length=1, choices=LATERALIDAD,
                                   blank=True)
    color_de_ojos = models.CharField(max_length=200, blank=True)
    color_de_cabello = models.CharField(max_length=200, blank=True)
    factor_rh = models.CharField(max_length=1, blank=True, choices=FACTOR_RH)
    tipo_de_sangre = models.CharField(max_length=2, blank=True,
                                      choices=TIPOS_SANGRE)

    def get_absolute_url(self):
        """Obtiene la URL absoluta"""

        return reverse('persona-view-id', args=[self.persona.id])


class HistoriaFisica(TimeStampedModel):
    MEDIDA_PESO = (
        ('Lb', _('Libras')),
        ('Kg', _('Kilogramos'))
    )

    persona = models.ForeignKey(Persona)
    fecha = models.DateTimeField(default=timezone.now)
    peso = models.DecimalField(decimal_places=2, max_digits=5, null=True)
    medida_de_peso = models.CharField(max_length=2, blank=True,
                                      choices=MEDIDA_PESO, default='Lb')
    altura = models.DecimalField(decimal_places=2, max_digits=5, null=True)

    pulso = models.IntegerField(null=True)
    temperatura = models.DecimalField(decimal_places=2, max_digits=8, null=True)
    presion_sistolica = models.IntegerField(null=True)
    presion_diastolica = models.IntegerField(null=True)
    respiracion = models.IntegerField(null=True)

    presion_arterial_media = models.CharField(max_length=200, blank=True)
    bmi = models.DecimalField(decimal_places=2, max_digits=11, null=True)
    bmr = models.DecimalField(decimal_places=2, max_digits=11, null=True)

    def get_absolute_url(self):
        """Obtiene la URL absoluta"""

        return reverse('persona-view-id', args=[self.persona.id])

    def get_weight(self):
        """
        Calculates body weight in Kg
        :return: Body weight in Kilograms
        """
        peso = 0
        if self.peso is not None:
            peso = self.peso

        if self.medida_de_peso == 'Lb':
            return peso / Decimal(2.22)
        else:
            return peso

    def body_mass_index(self):

        return self.get_weight() / max(self.altura, Decimal(0.01))

    def basal_energetic_expense(self):
        if self.persona.sexo == 'M':
            return Decimal(66.5) + Decimal(13.75) * self.get_weight() + \
                   Decimal(5) * self.altura * 100 + \
                   Decimal(6.78) * self.persona.obtener_edad()
        else:
            return Decimal(655.1) + Decimal(9.56) * self.get_weight() + \
                   Decimal(1.85) * self.altura * 100 + \
                   Decimal(4.68) * self.persona.obtener_edad()

    def save(self, **kwargs):
        self.bmr = self.basal_energetic_expense()
        self.bmi = self.body_mass_index()

        self.presion_arterial_media = float(self.presion_diastolica) + (
            float(1) / float(3) * float(self.presion_sistolica -
                                        self.presion_diastolica))
        super(HistoriaFisica, self).save(**kwargs)


class EstiloVida(TimeStampedModel):
    """Resumen del estilo de vida de una :class:`Persona`"""

    persona = AutoOneToOneField(Persona, primary_key=True,
                                related_name='estilo_vida')
    consume_tabaco = models.BooleanField(default=False, blank=True)
    inicio_consumo_tabaco = models.CharField(max_length=30, blank=True)
    tipo_de_tabaco = models.CharField(max_length=30, blank=True)
    consumo_diario_tabaco = models.IntegerField(default=0)

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


class Antecedente(TimeStampedModel):
    """Describe el historial clínico de una :class:`Persona` al llegar a
    consulta por primera vez
    """

    persona = AutoOneToOneField(Persona, primary_key=True)

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
    migrana = models.BooleanField(default=False, blank=True,
                                  verbose_name=_('Migraña'))
    obesidad = models.BooleanField(default=False, blank=True)
    colesterol = models.BooleanField(default=False, blank=True)
    trigliceridos = models.BooleanField(default=False, blank=True)
    alcoholismo = models.BooleanField(default=False, blank=True)
    cancer = models.BooleanField(default=False, blank=True)
    tiroides = models.BooleanField(default=False, blank=True)
    alergias = models.CharField(max_length=200, blank=True, null=True)

    congenital = models.CharField(max_length=200, blank=True,
                                  verbose_name=_('Congenitas'))

    general = models.CharField(max_length=200, blank=True)
    nutricional = models.CharField(max_length=200, blank=True)

    otros = models.CharField(max_length=200, blank=True)

    def get_absolute_url(self):
        """Obtiene la URL absoluta"""

        return reverse('persona-view-id', args=[self.persona.id])


class AntecedenteFamiliar(TimeStampedModel):
    """Registra los antecedentes familiares de una :class:`Persona`"""

    persona = AutoOneToOneField(Persona, primary_key=True,
                                related_name='antecedente_familiar')
    sindrome_coronario_agudo = models.BooleanField(
        default=False, blank=True,
        verbose_name=_('cardiopatia')
    )
    hipertension = models.BooleanField(default=False, blank=True,
                                       verbose_name=_('Hipertensión Arterial'))
    tabaquismo = models.BooleanField(default=False, blank=True)
    epoc = models.BooleanField(default=False, blank=True)
    diabetes = models.BooleanField(default=False, blank=True,
                                   verbose_name=_('Diabetes Mellitus'))
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
    tiroides = models.BooleanField(default=False, blank=True)
    alergias = models.CharField(max_length=200, blank=True, null=True)

    congenital = models.CharField(max_length=200, blank=True)

    general = models.CharField(max_length=200, blank=True)
    nutricional = models.CharField(max_length=200, blank=True)
    otros = models.CharField(max_length=200, blank=True)

    def get_absolute_url(self):
        """Obtiene la URL absoluta"""

        return reverse('persona-view-id', args=[self.persona.id])


class AntecedenteObstetrico(TimeStampedModel):
    """Registra los antecedentes obstetricos de una :class:`Persona`"""

    persona = AutoOneToOneField(Persona, primary_key=True,
                                related_name='antecedente_obstetrico')

    menarca = models.DateField(default=date.today)
    ultimo_periodo = models.DateField(null=True, blank=True)
    gestas = models.IntegerField(default=0)
    partos = models.IntegerField(default=0)
    cesareas = models.IntegerField(default=0)
    otros = models.CharField(max_length=200, blank=True)
    displasia = models.BooleanField(default=False, blank=True)
    anticoncepcion = models.BooleanField(default=False, blank=True)

    def get_absolute_url(self):
        """Obtiene la URL absoluta"""

        return reverse('persona-view-id', args=[self.persona.id])


@python_2_unicode_compatible
class Empleador(TimeStampedModel):
    nombre = models.CharField(max_length=200, blank=True)
    direccion = models.TextField()

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('empresa', args=[self.id])


@python_2_unicode_compatible
class Sede(TimeStampedModel):
    empleador = models.ForeignKey(Empleador, null=True, blank=True,
                                  related_name='sedes')
    lugar = models.CharField(max_length=200, blank=True)
    direccion = models.TextField()

    def __str__(self):
        return _('{0} de {1}').format(self.lugar, self.empleador.nombre)


class Empleo(TimeStampedModel):
    empleador = models.ForeignKey(Empleador, null=True, blank=True,
                                  related_name='empleos')
    sede = models.ForeignKey(Sede, related_name='empleos', null=True,
                             blank=True)
    persona = models.ForeignKey(Persona, related_name='empleos')
    numero_empleado = models.CharField(max_length=200, blank=True, null=True)

    def get_absolute_url(self):
        return self.persona.get_absolute_url()


class AntecedenteQuirurgico(TimeStampedModel):
    """Registra los antecendentes quirurgicos de una :class:`Persona`"""

    persona = models.ForeignKey(Persona,
                                related_name="antecedentes_quirurgicos")
    procedimiento = models.CharField(max_length=200, blank=True)
    fecha = models.CharField(max_length=200, blank=True)

    def get_absolute_url(self):
        """Obtiene la URL absoluta"""

        return self.persona.get_absolute_url()


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

persona_consolidation_functions = []


def remove_duplicates():
    count = Persona.objects.filter(duplicado=True).count()
    persona = Persona.objects.filter(duplicado=True).first()
    cantidad = 0
    if count == 1:
        persona.duplicado = False
        persona.save()

    while persona and count > 1:
        print(persona)
        cantidad += 1
        consolidate_into_persona(persona)
        persona = Persona.objects.filter(duplicado=True).first()
        count = Persona.objects.filter(duplicado=True).count()

    return cantidad


def consolidate_into_persona(persona):
    clones = Persona.objects.filter(
        nombre__iexact=persona.nombre,
        duplicado=True,
        apellido__iexact=persona.apellido
    ).exclude(pk=persona.pk)

    print(clones.count())
    for clone in clones.all():
        print(clone)

    [move_persona(persona, clone) for clone in clones.all()]
    persona.duplicado = False
    persona.save()


def move_persona(persona, clone):
    [function(persona, clone) for function in persona_consolidation_functions]
    print(_("Eliminando Persona"))
    clone.delete()


def transfer_object_to_persona(entity, persona):
    entity.persona = persona
    entity.save()
