# -*- coding: utf-8 -*-
from datetime import datetime, date
from django.db import models
from django.db.models import permalink
from django_extensions.db.fields import UUIDField
from django.contrib.auth.models import User
from library import image_to_content, dicom
from persona.models import Persona
from private_files.models.fields import PrivateFileField #@UnresolvedImport
from sorl.thumbnail import ImageField #@UnresolvedImport
from south.modelsinspector import add_introspection_rules
import os

class TipoExamen(models.Model):

    """Representa los diferentes examenes que se pueden efectuar en
    la institución"""

    nombre = models.CharField(max_length=200)

class EstudioProgramado(models.Model):

    """Permite que se planifique un :class:`Examen` antes de
    efectuarlo"""

    usuario = models.ForeignKey(User, blank=True, null=True,
                                   related_name='estudios_programados')
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE,
                                related_name="estudios_progamados")
    tipo_de_examen = models.ForeignKey(TipoExamen, on_delete=models.CASCADE,
                                related_name="estudios_progamados")
    fecha = models.DateField(default=date.today)
    remitio = models.CharField(max_length=200)
    efectuado = models.NullBooleanField(default=False)

    @permalink
    def get_absolute_url(self):
        
        """Obtiene la URL absoluta"""

        return 'tipo-examen-view-id', [self.id]

    def efectuar(self):

        """Marca el :class:`EstudioProgramado` y crea un :class:`Examen` basandose
        en los datos del primero"""

        examen = Examen()
        examen.tipo_de_examen = self.tipo_de_examen
        examen.persona = self.persona
        examen.usuario = self.usuario
        self.efectuado = True
        self.save()
        return examen

class Examen(models.Model):
    
    """Permite almacenar los datos de un estudio médico realizado a una
    :class:`Persona`"""
    
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE,
                                related_name="examenes")
    tipo_de_examen = models.ForeignKey(TipoExamen, on_delete=models.CASCADE,
                                related_name="examenes")
    nombre = models.CharField(max_length=200, blank=True)
    fecha = models.DateTimeField(default=datetime.now)
    uuid = UUIDField(version=4)
    usuario = models.ForeignKey(User, blank=True, null=True,
                                   related_name='estudios_realizados')
    
    @permalink
    def get_absolute_url(self):
        
        """Obtiene la URL absoluta"""
        
        return 'examen-view-id', [self.uuid]

class Imagen(models.Model):
    
    """Permite adjuntar imagenes de un estudio a un :class:`Persona`"""
    
    examen = models.ForeignKey(Examen, on_delete=models.CASCADE,
                               related_name='imagenes')
    imagen = ImageField(upload_to="examen/imagen/%Y/%m/%d")
    descripcion = models.CharField(max_length=255, blank=True)
    
    @permalink
    def get_absolute_url(self):
        
        """Obtiene la URL absoluta"""
        
        return 'examen-view-id', [self.examen.uuid]

class Adjunto(models.Model):
    
    """Permite agregar otro tipo de archivos adjuntos a un :class:`Examen`"""
    
    examen = models.ForeignKey(Examen, on_delete=models.CASCADE,
                               related_name='adjuntos')
    archivo = models.FileField(upload_to='examen/adjunto/%Y/%m/%d')
    descripcion = models.CharField(max_length=255, blank=True)
    
    @permalink
    def get_absolute_url(self):
        
        """Obtiene la URL absoluta"""
        
        return 'examen-view-id', [self.examen.uuid]

class Dicom(models.Model):
    
    """Permite agregar archivos DICOM a un :class:`Examen`, incluye funciones
    de utilidad para extraer :class:`Imagen` a partir de los datos incrustados
    dentro del archivo
    """

    examen = models.ForeignKey(Examen, on_delete=models.CASCADE,
                               related_name='dicoms')
    archivo = PrivateFileField(upload_to='examen/dicom/%Y/%m/%d',
                               attachment=False)
    descripcion = models.CharField(max_length=255, blank=True)
    convertido = models.BooleanField(default=False)
    imagen = PrivateFileField(upload_to='examen/dicom/imagen/%Y/%m/%d',
                              blank=True, attachment=False)
    uuid = UUIDField(version=4)
    
    def extraer_imagen(self):
        
        """Permite extraer una :class:`Imagen` que se encuentra incrustada en
        los datos del archivo :class:`Dicom` adjunto.
        """
        try:
            absolute = os.path.abspath(self.archivo.file.name)
            datos = dicom.extraer_imagen(str(absolute))
        except IOError as error:
            print(error.message)
        
        imagen_dicom = image_to_content(datos)
        archivo = os.path.splitext(os.path.basename(self.archivo.name))[0]
        self.convertido = True
        self.imagen.save("{0}.jpg".format(archivo), imagen_dicom)
        self.save()
    
    @permalink
    def get_absolute_url(self):
        
        """Obtiene la URL absoluta"""
        
        return 'examen-view-id', [self.examen.uuid]

add_introspection_rules([
    (
        [PrivateFileField], # Class(es) these apply to
        [],         # Positional arguments (not used)
        {           # Keyword argument
            #"ordered": ["ordered", {}],
            #"sort": ["sort", {}],
        },
    ),
], ["^private_files\.models\.fields\.PrivateFileField"])
