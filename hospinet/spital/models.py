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

from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models
from django.db.models import permalink
from django_extensions.db.fields import UUIDField
from library import image_to_content
from persona.models import Persona
from sorl.thumbnail import ImageField

class Habitacion(models.Model):
    
    """Permite llevar control acerca de las :class:`Habitacion`es que se
    encuentran en el hospital para asignar adecuadamente las mismas a cada
    :class:`Admision`"""

    TIPOS = (
        ('N', 'Normal'),
        ('S', 'Suite'),
        ('U', 'U.C.I.'),
    )

    ESTADOS = (
        ('D', 'Disponible'),
        ('O', 'Ocupada'),
        ('M', 'Mantenimiento'),
    )

    numero = models.IntegerField()
    tipo = models.CharField(max_length=1, blank=True, choices=TIPOS)
    estado = models.CharField(max_length=1, blank=True, choices=ESTADOS)
    
    def __unicode__(self):

        return u'{0} {1}'.format(self.get_tipo_display(), self.numero)

    @permalink
    def get_absolute_url(self):
        
        """Obtiene la URL absoluta de la :class:`Habitacion`"""
        
        return 'habitacion-view', [self.id]

class Admision(models.Model):
    
    """Permite registrar el Ingreso y estadía de una :class:`Persona` en el
    Hospital.

    Durante cada :class:`Admision se registran los diversos procedmientos que
    efectuan la :class:`Persona` durante su estadía en el hospital, ya sean
    procedimientos quirúrgicos, examenes de laboratorio, controles de
    enfermería, diversos cargos y otra información adecuada
    """
    
    ESTADOS = (
        ('A', 'Admitido'),
        ('B', 'Autorizado'),
        ('H', 'Hospitalizar'),
        ('I', 'Ingresado'),
        ('C', 'Alta'),
    )
    
    ARANCELES = (
               ('C', u"CEMESA"),
               ('E', u"Empleado"),
               ('M', u"Mediprocesos"),
               ('J', u"Ejecutivo"),
               ('X', u"Extranjero"),
    )
    
    PAGOS = (
             ('EF', u"Efectivo"),
             ('CK', u"Cheque"),
             ('CO', u"Empresa"),
             ("OC", u"Orden de Compra"),
             ('TC', u"Tarjeta Crédito"),
             ('TB', u"Transferencia Bancaria"),
    )
    
    TIPOS_INGRESOS = (
             ("PA","Particular"),
             ("SN", "Aseguradora Nacional"),
             ("SI", "Aseguradora Internacional"),
             ("PS", "Presupuesto"),
    )
    
    momento = models.DateTimeField(default=timezone.now, null=True, blank=True)
    paciente = models.ForeignKey(Persona, related_name='admisiones')
    fiadores = models.ManyToManyField(Persona, related_name='fianzas',
                                      null=True, blank=True)
    referencias = models.ManyToManyField(Persona, related_name='referencias',
                                         null=True, blank=True)
    
    diagnostico = models.CharField(max_length=200, blank=True)
    doctor = models.CharField(max_length=200, blank=True)
    
    tipo_de_habitacion = models.CharField(max_length=200, blank=True)
    habitacion = models.ForeignKey(Habitacion, related_name='admisiones',
                                   null=True, blank=True)
    arancel = models.CharField(max_length=200, blank=True, choices=ARANCELES)
    
    pago = models.CharField(max_length=200, blank=True, choices=PAGOS)
    
    poliza = models.CharField(max_length=200, blank=True)
    certificado = models.CharField(max_length=200, blank=True)
    aseguradora = models.CharField(max_length=200, blank=True)
    deposito = models.CharField(max_length=200, blank=True)
    
    observaciones = models.CharField(max_length=200, blank=True)
    admitio = models.ForeignKey(User)
    admision = models.DateTimeField(default=timezone.now,null=True, blank=True)
    """Indica la fecha y hora en que la :class:`Persona` fue ingresada en
    admisiones"""
    autorizacion = models.DateTimeField(default=timezone.now,null=True, blank=True)
    hospitalizacion = models.DateTimeField(null=True, blank=True)
    """Indica la fecha y hora en que la :class:`Persona` fue internada"""
    ingreso = models.DateTimeField(null=True, blank=True)
    """Indica la fecha y hora en que la :class:`Persona` fue enviada al area
    de enfermeria"""
    fecha_pago = models.DateTimeField(default=timezone.now,null=True, blank=True)
    fecha_alta = models.DateTimeField(default=timezone.now,null=True, blank=True)
    uuid = UUIDField(version=4)
    estado = models.CharField(max_length=1, blank=True, choices=ESTADOS)
    tiempo = models.IntegerField(default=0, blank=True)
    neonato = models.NullBooleanField(blank=True, null=True)
    tipo_de_ingreso = models.CharField(max_length=200, blank=True, null=True, choices=TIPOS_INGRESOS)
    
    def autorizar(self):
        
        if self.autorizacion <= self.momento:
            self.autorizacion = timezone.now()
            self.estado = 'B'
            self.save()
    
    def pagar(self):

        """Registra el momento en el que se efectua el pago de una
        :class:`Admision`"""
        
        if self.fecha_pago <= self.momento:
            self.fecha_pago = timezone.now()
            self.save()
    
    def hospitalizar(self):

        """Permite que registrar el momento en que una :class:`Admision` ha
        sido enviada a enfermeria para ingresar al hospital"""
        
        if self.hospitalizacion == None or self.hospitalizacion <= self.momento:
            self.hospitalizacion = timezone.now()
            self.estado = 'H'
            self.save()
            
    def ingresar(self):
        
        if self.ingreso == None or self.ingreso <= self.momento:
            self.ingreso = timezone.now()
            self.estado = 'I'
            self.save()
    
    def tiempo_autorizacion(self):
        
        """Calcula el tiempo que se tarda una :class:`Persona` para ser
        admitida en el :class:`Hospital`"""
        
        if self.autorizacion <= self.momento:
            
            return 0
        
        return (self.autorizacion - self.momento).seconds / 60
    
    def tiempo_admisiones(self):
        
        """Calcula el tiempo que se tarda una :class:`Persona` para ser
        admitida en el :class:`Hospital`"""
        
        if self.admision <= self.momento:
            
            return 0
        
        return (self.admision - self.momento).seconds / 60
    
    def tiempo_hospitalizacion(self):
        
        """Calcula el tiempo que se tarda una :class:`Persona` para ser
        ingresada en el :class:`Hospital`"""
        
        if self.ingreso == None or self.ingreso <= self.hospitalizacion:
            
            return (timezone.now() - self.hospitalizacion).total_seconds() / 60
        
        return (self.ingreso - self.hospitalizacion).total_seconds() / 60
    
    def tiempo_ahora(self):
        
        """Permite mostrar el tiempo que ha transcurrido desde que se agrego
        la :class:`Admision` al sistema"""

        ahora = timezone.now()
        if self.momento >= ahora:
            
            return 0
        
        return (ahora - self.momento).total_seconds() / 60
    
    def actualizar_tiempo(self):

        """Actualiza el tiempo transcurrido desde el ingreso hasta el momento
        en que se dio de alta"""

        if self.ingreso == None:
            return

        if not self.fecha_alta == None:
            self.tiempo = (self.fecha_alta - self.ingreso).total_seconds() / 60
        else:
            self.tiempo = self.tiempo_ahora()
    
    def save(self, *args, **kwargs):
        self.actualizar_tiempo()
        super(Admision, self).save(*args, **kwargs)
    
    @permalink
    def get_absolute_url(self):
        
        """Obtiene la URL absoluta"""
        
        return 'admision-view-id', [self.id]
    
    def __unicode__(self):

        return u"{0} en {1}".format(self.paciente.nombre_completo(), self.habitacion)
