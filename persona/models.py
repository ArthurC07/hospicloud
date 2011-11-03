# -*- coding: utf-8 -*-
"""
Modelos básicos necesarios para recabar la información personal de una
:class:`Persona` en la aplicación, permitiendo centralizar las funciones que
se utilizarán a lo largo de todo el sistema
"""
from datetime import date
from django.db import models
from django.db.models import permalink
import re

class Pais(models.Model):
    
    """Representa los varios paises dentro de la aplicación"""
    
    nombre = models.CharField(max_length=200)
    order = models.IntegerField()
    
    def __unicode__(self):
        
        return self.nombre

class Persona(models.Model):
    
    """Representación de una :class:`Persona` en la aplicación"""
    
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
                                           choices=TIPOS_IDENTIDAD)
    identificacion = models.CharField(max_length=20, blank=True, unique=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    sexo = models.CharField(max_length=1, choices=GENEROS)
    nacimiento = models.DateField(default=date.today)
    nacionalidad = models.ForeignKey('Pais')
    estado_civil = models.CharField(max_length=1, choices=ESTADOS_CIVILES)
    profesion = models.CharField(max_length=200, blank=True)
    telefono = models.CharField(max_length=200, blank=True)
    ci = models.CharField(max_length=200, blank=True)
    celular = models.CharField(max_length=200, blank=True)
    domicilio = models.CharField(max_length=200, blank=True)
    tel_trabajo = models.CharField(max_length=200, blank=True)
    centro_trabajo = models.CharField(max_length=200, blank=True)
    direccion_trabajo = models.CharField(max_length=200, blank=True)
    email = models.CharField(max_length=200, blank=True)
    antiguedad = models.CharField(max_length=200, blank=True)
    cargo = models.CharField(max_length=200, blank=True)
    fax = models.CharField(max_length=200, blank=True)
    fotografia = models.ImageField(upload_to='persona/foto', blank=True)
    
    @staticmethod
    def validar_identidad(identidad):
        
        """Permite validar la identidad ingresada antes de asignarla a una
        :class:`Persona`
        
        :param identidad: Número de identidad a validar
        """
        
        return Persona.__expresion__.match(identidad)
    
    @permalink
    def get_absolute_url(self):
        
        """Obtiene la URL absoluta"""
        
        return 'persona-view-id', [self.id]
    
    def nombre_completo(self):
        
        """Obtiene el nombre completo de la :class:`Persona`"""
        
        return u'{0} {1}'.format(self.nombre, self.apellido)
    
    def obtener_edad(self):
        
        """Obtiene la edad de la :class:`Persona`"""
        
        if self.nacimiento == None:
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
    
    persona = models.OneToOneField(Persona, primary_key=True)
    peso = models.DecimalField(decimal_places=2, max_digits=4, null=True)
    altura = models.DecimalField(decimal_places=2, max_digits=4, null=True)
    color_de_ojos = models.CharField(max_length=200, blank=True)
    color_de_cabello = models.CharField(max_length=200, blank=True)
    factor_rh = models.CharField(max_length=1, blank=True)
    tipo_de_sangre = models.CharField(max_length=2, blank=True)
    
    @permalink
    def get_absolute_url(self):
        
        """Obtiene la URL absoluta"""
        
        return self.persona.get_absolute_url()

class EstiloVida(models.Model):
    
    """Resumen del estilo de vida de una :class:`Persona`"""
    
    persona = models.OneToOneField(Persona, primary_key=True,
                                   related_name='estilo_vida')
    consume_tabaco = models.NullBooleanField(null=True, blank=True)
    inicio_consumo_tabaco = models.CharField(max_length=30, blank=True)
    consumo_diario_tabaco = models.IntegerField(null=True)
    
    consume_alcohol = models.NullBooleanField(null=True)
    vino = models.NullBooleanField(null=True)
    cerveza = models.NullBooleanField(null=True)
    licor = models.NullBooleanField(null=True)
    
    cafe = models.NullBooleanField(null=True)
    cantidad_cafe = models.CharField(max_length=200, blank=True)
    
    dieta = models.CharField(max_length=200, blank=True)
    cantidad = models.CharField(max_length=200, blank=True)
    numero_comidas = models.IntegerField(null=True)
    tipo_de_comidas = models.CharField(max_length=200, blank=True)
    
    consume_drogas = models.NullBooleanField(null=True)
    drogas = models.CharField(max_length=200, blank=True)
    otros = models.CharField(max_length=200, blank=True)
    
    @permalink
    def get_absolute_url(self):
        
        """Obtiene la URL absoluta"""
        
        return self.persona.get_absolute_url()

class Antecedente(models.Model):
    
    """Describe la situación of a :class:`Paciente` when he/she first arrives at
    the clinic
    """
    
    persona = models.OneToOneField(Persona)
    
    complete = models.NullBooleanField(null=True, blank=True)
    reaction = models.NullBooleanField(null=True, blank=True)
    
    cardiopatia = models.NullBooleanField(null=True, blank=True)
    hipertension = models.NullBooleanField(null=True, blank=True)
    diabetes = models.NullBooleanField(null=True, blank=True)
    hepatitis = models.NullBooleanField(null=True, blank=True)
    rinitis = models.NullBooleanField(null=True, blank=True)
    tuberculosis = models.NullBooleanField(null=True, blank=True)
    artritis = models.NullBooleanField(null=True, blank=True)
    asma = models.NullBooleanField(null=True, blank=True)
    colitis = models.NullBooleanField(null=True, blank=True)
    gastritis = models.NullBooleanField(null=True, blank=True)
    sinusitis = models.NullBooleanField(null=True, blank=True)
    hipertrigliceridemia = models.NullBooleanField(null=True, blank=True)
    colelitiasis = models.NullBooleanField(null=True, blank=True)
    migrana = models.NullBooleanField(null=True, blank=True)
    alergias = models.CharField(max_length=200)
    
    congenital = models.CharField(max_length=200, blank=True)
    
    general = models.CharField(max_length=200, blank=True)
    nutricional = models.CharField(max_length=200, blank=True)
    
    otros = models.CharField(max_length=200, blank=True)
    
    @permalink
    def get_absolute_url(self):
        
        """Obtiene la URL absoluta"""
        
        return self.persona.get_absolute_url()

class AntecedenteFamiliar(models.Model):
    
    """Registra los antecedentes familiares de una :class:`Persona`"""
    
    persona = models.OneToOneField(Persona)
    
    carcinogenico = models.NullBooleanField(null=True, blank=True)
    cardiovascular = models.NullBooleanField(null=True, blank=True)
    endocrinologico = models.NullBooleanField(null=True, blank=True)
    respiratorio = models.NullBooleanField(null=True, blank=True)
    otros = models.CharField(max_length=200, blank=True)
    
    @permalink
    def get_absolute_url(self):
        
        """Obtiene la URL absoluta"""
        
        return self.persona.get_absolute_url()

class AntecedenteObstetrico(models.Model):
    
    """Registra los antecedentes obstetricos de una :class:`Persona`"""
    
    persona = models.OneToOneField(Persona)
    
    menarca = models.DateField(default=date.today)
    ultimo_periodo = models.DateField(null=True, blank=True)
    displasia = models.NullBooleanField(null=True, blank=True)
    # what the hell does these means?
    g = models.CharField(max_length=200, blank=True)
    p = models.CharField(max_length=200, blank=True)
    a = models.CharField(max_length=200, blank=True)
    c = models.CharField(max_length=200, blank=True)
    otros = models.CharField(max_length=200, blank=True)
    
    @permalink
    def get_absolute_url(self):
        
        """Obtiene la URL absoluta"""
        
        return self.persona.get_absolute_url()

class AntecedenteQuirurgico(models.Model):
    
    """Registra los antecendentes quirurgicos de una :class:`Persona`"""
    
    persona = models.ForeignKey(Persona)
    procedimiento = models.CharField(max_length=200, blank=True)
    fecha = models.CharField(max_length=200, blank=True)
    
    @permalink
    def get_absolute_url(self):
        
        """Obtiene la URL absoluta"""
        
        return self.persona.get_absolute_url()
