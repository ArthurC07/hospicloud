# -*- coding: utf-8 -*-
from django.db import models
from persona.models import Persona
from datetime import datetime

class Examen(models.Model):
    
    persona = models.ForeignKey(Persona)
    nombre = models.CharField(max_length=200, blank=True)
    resultado = models.CharField(max_length=200, blank=True)
    diagnostico = models.CharField(max_lenght=255, blank=True)
    fecha = models.DateTimeField(default=datetime.now)

class Imagen(models.Model):
    
    examen = models.ForeignKey(Examen)
    imagen = models.ImageField(upload_to="examenes")
