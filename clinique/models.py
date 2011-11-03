# -*- coding: utf-8 -*-
from django.db import models
from datetime import datetime
from persona.models import Persona

class Visitante(models.Model):
    
    ESTADOS = (
        ('E', u'Esperando'),
        ('C', u'Consulta'),
        ('A', u'Atendido'),
    )
    
    nombre = models.CharField(max_length=200)
    estado = models.CharField(max_lenght=255, blank=True, choices=ESTADOS)
    llegada = models.DateTimeField(default=datetime.now)
    programacion = models.DateTimeField(default=datetime.now)

class Cuenta(models.Model):
    
    persona = models.ForeignKey(Persona)
