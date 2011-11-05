# -*- coding: utf-8 -*-
from django.db import models
from persona.models import Persona
from datetime import datetime
from django.db.models import permalink
from sorl.thumbnail import ImageField #@UnresolvedImport

class Examen(models.Model):
    
    """Permite almacenar los datos de un estudio médico realizado a una
    :class:`Persona`"""
    
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200, blank=True)
    resultado = models.CharField(max_length=200, blank=True)
    diagnostico = models.CharField(max_length=255, blank=True)
    fecha = models.DateTimeField(default=datetime.now)
    
    @permalink
    def get_absolute_url(self):
        
        """Obtiene la URL absoluta"""
        
        return 'examen-view-id', [self.id]

class Imagen(models.Model):
    
    """Permite adjuntar imagenes de un estudio a un :class:`Persona`"""
    
    examen = models.ForeignKey(Examen, on_delete=models.CASCADE)
    imagen = ImageField(upload_to="examen/imagen")
    descripcion = models.CharField(max_length=255, blank=True)
    
    @permalink
    def get_absolute_url(self):
        
        """Obtiene la URL absoluta"""
        
        return 'examen-view-id', [self.examen.id]

class Adjunto(models.Model):
    
    """Permite agregar otro tipo de archivos adjuntos a un :class:`Examen`"""
    
    examen = models.ForeignKey(Examen, on_delete=models.CASCADE)
    archivo = models.FileField(upload_to='examen/adjunto')
    descripcion = models.CharField(max_length=255, blank=True)
    
    @permalink
    def get_absolute_url(self):
        
        """Obtiene la URL absoluta"""
        
        return 'examen-view-id', [self.examen.id]

Persona.examenes = property(lambda p: Examen.objects.filter(persona=p))
