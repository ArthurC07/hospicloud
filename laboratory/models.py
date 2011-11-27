# -*- coding: utf-8 -*-
from datetime import datetime
from django.db import models
from django.db.models import permalink
from library import image_to_content, dicom
from persona.models import Persona
from sorl.thumbnail import ImageField #@UnresolvedImport
import os

class Examen(models.Model):
    
    """Permite almacenar los datos de un estudio médico realizado a una
    :class:`Persona`"""
    
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE,
                                related_name="examenes")
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
    
    examen = models.ForeignKey(Examen, on_delete=models.CASCADE,
                               related_name='imagenes')
    imagen = ImageField(upload_to="examen/imagen/%Y/%m/%d")
    descripcion = models.CharField(max_length=255, blank=True)
    
    @permalink
    def get_absolute_url(self):
        
        """Obtiene la URL absoluta"""
        
        return 'examen-view-id', [self.examen.id]

class Adjunto(models.Model):
    
    """Permite agregar otro tipo de archivos adjuntos a un :class:`Examen`"""
    
    examen = models.ForeignKey(Examen, on_delete=models.CASCADE,
                               related_name='adjuntos')
    archivo = models.FileField(upload_to='examen/adjunto/%Y/%m/%d')
    descripcion = models.CharField(max_length=255, blank=True)
    
    @permalink
    def get_absolute_url(self):
        
        """Obtiene la URL absoluta"""
        
        return 'examen-view-id', [self.examen.id]

class Dicom(models.Model):
    
    """Permite agregar archivos DICOM a un :class:`Examen`, incluye funciones
    de utilidad para convertir en :class:`Imagen`
    """
    archivo = models.FileField(upload_to='examen/dicom/%Y/%m/%d')
    descripcion = models.CharField(max_length=255, blank=True)
    convertido = models.BooleanField(default=False)
    imagen = models.ImageField(upload_to='examen/dicom/imagen/%Y/%m%/%d', blank=True)
    
    def extraer_imagen(self):
        
        imagen_dicom = image_to_content(dicom.extraer_imagen(self.archivo.name))
        archivo = os.path.splitext(os.path.basename(self.archivo.name))[0]
        self.imagen.save("{0}.jpg".format(archivo), imagen_dicom)
