# -*- coding: utf-8 -*-
from datetime import datetime
from django.contrib.auth.models import User
from django.db import models
from persona.models import Persona

class Consultorio(models.Model):
    
    doctor = models.ManyToManyField(User)
    secretaria = models.ManyToManyField(User)
    nombre = models.CharField(max_lenght=1, blank=True)

class Visitante(models.Model):
    
    ESTADOS = (
        ('E', u'Esperando'),
        ('C', u'Consulta'),
        ('A', u'Atendido'),
    )
    
    consultorio = models.ForeignKey(Consultorio)
    nombre = models.CharField(max_length=200)
    estado = models.CharField(max_lenght=1, blank=True, choices=ESTADOS)
    llegada = models.DateTimeField(default=datetime.now)
    programacion = models.DateTimeField(default=datetime.now)

class Paciente(models.Model):
    
    ESTADOS = (
        ('E', u'Esperando'),
        ('C', u'Consulta'),
        ('A', u'Atendido'),
    )
    
    persona = models.ForeignKey(Persona)
    consultorio = models.ForeignKey(Consultorio)
    nombre = models.CharField(max_length=200)
    estado = models.CharField(max_lenght=1, blank=True, choices=ESTADOS)
    llegada = models.DateTimeField(default=datetime.now)
    programacion = models.DateTimeField(default=datetime.now)

class Cuenta(models.Model):
    
    persona = models.ForeignKey(Persona)
    consultorio = models.ForeignKey(Consultorio)

class Transaccion(models.Model):
    
    TIPO = (
        (1, u'Crédito'),
        (2, u'Débito')
    )
    
    cuenta = models.ForeignKey(Cuenta)
    concepto = models.CharField(max_lenght=1, blank=True)
    tipo = models.IntegerField(choices=TIPO)
    monto = models.DecimalField()
    fecha_y_hora = models.DateTimeField(default=datetime.now)
