# -*- coding: utf-8 -*-
#
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

from datetime import datetime, date
from django.db import models
from django.db.models import permalink
from django_extensions.db.fields import UUIDField
from django.contrib.auth.models import User
from persona.models import Persona
from sorl.thumbnail import ImageField
import os
import subprocess
from inventory.models import ItemTemplate

class TipoExamen(models.Model):
    
    """Representa los diferentes examenes que se pueden efectuar en
    la institución"""
    
    nombre = models.CharField(max_length=200)
    item = models.ForeignKey(ItemTemplate, blank=True, null=True)
    
    def __unicode__(self):
        
        """Devuelve una representación en texto del objeto"""
        
        return self.nombre

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
    radiologo = models.CharField(max_length=200, blank=True, null=True)
    efectuado = models.NullBooleanField(default=False)
    
    @permalink
    def get_absolute_url(self):
        
        """Obtiene la URL absoluta"""
        
        return 'estudio-detail-view', [self.id]
    
    def efectuar(self):

        """Marca el :class:`EstudioProgramado` y crea un :class:`Examen` basandose
        en los datos del primero"""

        examen = Examen()
        examen.tipo_de_examen = self.tipo_de_examen
        examen.persona = self.persona
        examen.usuario = self.usuario
        examen.remitio = self.remitio
        examen.radiologo = self.radiologo
        self.efectuado = True
        self.save()
        return examen
    
    def __unicode__(self):

        """Devuelve una representación en texto del objeto"""
        
        return u"{0} de {1}, {2}".format(self.tipo_de_examen, self.persona, self.fecha)

class Examen(models.Model):
    
    """Permite almacenar los datos de un estudio médico realizado a una
    :class:`Persona`"""
    
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE,
                                related_name="examenes")
    tipo_de_examen = models.ForeignKey(TipoExamen, on_delete=models.CASCADE,
                                related_name="examenes")
    fecha = models.DateTimeField(default=datetime.now)
    uuid = UUIDField(version=4)
    usuario = models.ForeignKey(User, blank=True, null=True,
                                   related_name='estudios_realizados')
    remitio = models.CharField(max_length=200, null=True)
    facturado = models.NullBooleanField(default=False)
    radiologo = models.CharField(max_length=200, blank=True, null=True)
    
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
    archivo = models.FileField(upload_to='examen/dicom/%Y/%m/%d')
    descripcion = models.CharField(max_length=255, blank=True)
    convertido = models.BooleanField(default=False)
    imagen = ImageField(upload_to='examen/dicom/imagen/%Y/%m/%d',
                              blank=True)
    uuid = UUIDField(version=4)
    
    def extraer_imagen(self):
        
        """Permite extraer una :class:`Imagen` que se encuentra incrustada en
        los datos del archivo :class:`Dicom` adjunto.
        """
       
        absolute = os.path.abspath(self.archivo.file.name)
        archivo = os.path.splitext(os.path.basename(self.archivo.name))[0]
        self.convertido = True
        subprocess.call(['dcmj2pnm', '--write-png', absolute, absolute + '.png'])
        
        self.imagen = self.archivo.name  + '.png'
        self.save()
    
    @permalink
    def get_absolute_url(self):
        
        """Obtiene la URL absoluta"""
        
        return 'examen-view-id', [self.examen.uuid]
