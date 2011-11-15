# -*- coding: utf-8 -*-
from django.db import models
from spital.models import Admision
from datetime import datetime
# Create your models here.

class SignoVital(models.Model):
    
    """Registra los signos vitales de una :class:`Persona` durante una
    :class:`Admision` en el  Hospital"""
    
    admision = models.ForeignKey(Admision, related_name='signos_vitales')
    fecha_y_hora = models.DateTimeField(default=datetime.now)
    pulso = models.IntegerField()
    temperatura = models.DecimalField(decimal_places=2, max_digits=4, null=True)
    presion = models.DecimalField(decimal_places=2, max_digits=4, null=True)
    respiracion = models.DecimalField(decimal_places=2, max_digits=4, null=True)
    observacion = models.DecimalField(decimal_places=2, max_digits=4, null=True)
    saturacion_de_oxigeno = models.DecimalField(decimal_places=2, max_digits=4,
                                                null=True)
    presion_arterial_media = models.CharField(max_length=200, blank=True)

class Evolucion(models.Model):
    
    """Registra la evolución de la :class:`Persona durante una
    :class:`Admision`"""
    
    admision = models.ForeignKey(Admision, related_name='evolucion')
    fecha_y_hora = models.DateTimeField(default=datetime.now)
    nota = models.CharField(max_length=200, blank=True)

class Cargo(models.Model):
    
    """Indica los cargos en base a aparatos que utiliza una :class:`Persona`"""
    
    admision = models.ForeignKey(Admision, related_name='cargos')
    fecha_y_hora = models.DateTimeField(default=datetime.now)
    cargo = models.CharField(max_length=200)
    inicio = models.DateTimeField(default=datetime.now)
    fin = models.DateTimeField(default=datetime.now)

class OrdenMedica(models.Model):
    
    """Registra las indicaciones a seguir por el personal de enfermeria"""
    
    admision = models.ForeignKey(Admision, related_name='ordenes_medicas')
    orden = models.CharField(max_length=200, blank=True)
    doctor = models.CharField(max_length=200, blank=True)
    fecha_y_hora = models.DateTimeField(default=datetime.now)

class Ingesta(models.Model):
    
    """Registra las ingestas que una :class:`Persona`"""
    
    admision = models.ForeignKey(Admision, related_name='ingestas')
    fecha_y_hora = models.DateTimeField(default=datetime.now)
    ingerido = models.CharField(max_length=200, blank=True)
    cantidad = models.IntegerField()
    liquido = models.NullBooleanField(blank=True, null=True)

class Excreta(models.Model):
    
    """Registra las excresiones de una :class:`Persona` durante una
    :class:`Admision`"""
    
    admision = models.ForeignKey(Admision, related_name='excretas')
    fecha_y_hora = models.DateTimeField(default=datetime.now)
    medio = models.CharField(max_length=200, blank=True)
    cantidad = models.CharField(max_length=200, blank=True)
    descripcion = models.CharField(max_length=200, blank=True)
    otro = models.CharField(max_length=200, blank=True)
    otros = models.CharField(max_length=200, blank=True)

class NotaEnfermeria(models.Model):
    
    """Nota agregada a una :class:`Admision` por el personal de Enfermeria"""
    
    admision = models.ForeignKey(Admision, related_name='notas_enfermeria')
    fecha_y_hora = models.DateTimeField(default=datetime.now)
    nota = models.CharField(max_length=200, blank=True)

class Glucometria(models.Model):
    
    """Registra las fluctuaciones en los niveles de Glucosa en la sangre de una
    :class:`Persona` durante una :class`Admision`"""
    
    admision = models.ForeignKey(Admision, related_name='glucometrias')
    fecha_y_hora = models.DateTimeField(default=datetime.now)
    control = models.CharField(max_length=200, blank=True)
    tipo = models.CharField(max_length=200, blank=True)
    observacion = models.CharField(max_length=200, blank=True)

class Sumario(models.Model):
    
    """Registra los datos de una :class:`Persona` al momento de darle de alta
    de una :class:`Admision`"""
    
    admision = models.OneToOneField(Admision)
    diagnostico = models.CharField(max_length=200, blank=True)
    procedimiento_efectuado = models.CharField(max_length=200, blank=True)
    condicion = models.CharField(max_length=200, blank=True)
    recomendaciones = models.CharField(max_length=200, blank=True)

Admision.sumario = property(lambda a: Sumario.objects.get_or_create(admision=a)[0])

class FrecuenciaLectura(models.Model):
    
    """Indica cada cuanto se debe tomar una :class:`Glucometria` y una lectura
    de :class:`SignosVitales`"""
    
    admision = models.OneToOneField(Admision)
    glucometria = models.IntegerField(default=0,blank=True)
    signos_vitales = models.IntegerField(default=0,blank=True)

Admision.frecuencia_lectura = property(lambda a: FrecuenciaLectura.objects.get_or_create(admision=a)[0])
