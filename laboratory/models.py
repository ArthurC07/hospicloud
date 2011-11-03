# -*- coding: utf-8 -*-
from django.db import models
from persona.models import Persona
from datetime import datetime

class Examen(models.Model):
    
    """Permite almacenar los datos de un estudio médico realizado a una
    :class:`Persona`"""
    
    persona = models.ForeignKey(Persona)
    nombre = models.CharField(max_length=200, blank=True)
    resultado = models.CharField(max_length=200, blank=True)
    diagnostico = models.CharField(max_lenght=255, blank=True)
    fecha = models.DateTimeField(default=datetime.now)

class Imagen(models.Model):
    
    """Permite adjuntar imagenes de un estudio a un :class:`Persona`"""
    
    examen = models.ForeignKey(Examen)
    imagen = models.ImageField(upload_to="examenes")
    descripcion = models.CharField(max_lenght=255, blank=True)

class Adjuntos(models.Model):
    
    """Permite agregar otro tipo de archivos adjuntos a un :class:`Examen`"""
    
    examen = models.ForeignKey(Examen)
    archivo = models.FileField(upload_to='adjuntos')
    descripcion = models.CharField(max_lenght=255, blank=True)
