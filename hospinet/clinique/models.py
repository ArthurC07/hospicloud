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
from django.db import models
from persona.models import Persona
from django_extensions.db.fields import UUIDField
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

class Consultorio(models.Model):
    
    """Permite que un :class:`User` pueda llevar un control privado de la
    atención privada que le ha facilitado a una :class:`Persona`"""
    
    nombre = models.CharField(max_length=255, blank=True)
    secretaria = models.ForeignKey(User, blank=True, null=True,
                                   related_name='secretariados')
    doctor = models.ForeignKey(User, blank=True, null=True,
                                   related_name='consultorios')
    uuid = UUIDField(version=4)
    
    def balance(self):
        
        """Obtiene el total de las cuentas por cobrar de un
        :class:`Consultorio`"""
        
        return sum(p.saldo() for p in self.pacientes)
    
    def get_absolute_url(self):
        
        """Obtiene la URL absoluta"""
        
        return reverse('consultorio-view', args=[self.uuid])

User.balance = property(lambda u: sum(c.balance() for c in u.consultorios))

class Paciente(models.Model):
    
    """Relaciona a una :class:`Persona` con un :class:`Consultorio` para
    ayudar a proteger la privacidad de dicha :class:`Persona` ya que se
    restringe el acceso a la información básica y a los datos ingresados por
    el :class:`User` al que pertenece el :class:`Consultorio`"""
    
    persona = models.ForeignKey(Persona, related_name='consultorios')
    consultorio = models.ForeignKey(Consultorio, related_name='pacientes')
    uuid = UUIDField(version=4)
    primera_visita = models.DateTimeField(default=timezone.now)

    def identificacion():

        return self.persona.identificacion

    def nombre(self):

        return self.persona.nombre_completo()
    
    def saldo(self):
        
        """Obtiene el valor total de las :class:`Transacciones` efectuadas
        entre el :class:`User` y la :class:`Persona`"""

        creditos =  sum(t.monto for t in self.transacciones if t.tipo == 1)
        debitos =  sum(t.monto for t in self.transacciones if t.tipo == 2)
        
        return creditos - debitos
    
    def get_absolute_url(self):
        
        """Obtiene la url relacionada con un :class:`Paciente`"""
        
        return reverse('consultorio-paciente', args=[self.uuid])

Persona.saldo = property(lambda p: sum(c.saldo() for c in p.consultorios))

class Transaccion(models.Model):
    
    """Permite registrar los cargos y pagos que se efectuan entre un
    :class:`Paciente` y un :class:`Consultorio`"""
    
    TIPO = (
        (1, u'Crédito'),
        (2, u'Débito')
    )
    
    paciente = models.ForeignKey(Paciente, related_name='transacciones')
    concepto = models.CharField(max_length=1, blank=True)
    tipo = models.IntegerField(choices=TIPO)
    monto = models.DecimalField(decimal_places=2, max_digits=12)
    fecha_y_hora = models.DateTimeField(default=timezone.now)

class Cita(models.Model):
    
    """Permite registrar las posibles :class:`Personas`s que serán atendidas
    en una fecha determinada""" 
    
    consultorio = models.ForeignKey(Consultorio, related_name='citas')
    nombre = models.CharField(max_length=200)
    fecha_y_hora = models.DateTimeField(default=timezone.now)

class Esperador(models.Model):
    
    """Permite agregar una :class:`Persona` a la lista de :class:`Paciente`s en
    la sala de espera"""
    
    consultorio = models.ForeignKey(Consultorio, related_name='esperadores')
    paciente = models.ForeignKey(Paciente, related_name='esperas')
    atendido = models.BooleanField(default=False)

class Consulta(models.Model):

    """"Permite al doctor especificar las razones de la visita de un
    :class:`Paciente`"""

    paciente = models.ForeignKey(Paciente, related_name='consultas')
    razon_de_la_visita = models.TextField(blank=True)
    fecha_y_hora = models.DateTimeField(default=timezone.now)
    agudeza_visual_ojo_derecho = models.IntegerField(default=0)
    agudeza_visual_ojo_izquierdo = models.IntegerField(default=0)
    
    def get_absolute_url(self):
        
        return 'consultorio-paciente', [self.paciente.uuid]

class Receta(models.Model):

    """Describe los medicamentos que un paciente recomienda a un :class:`Paciente`
    luego de una :class:`Consulta`"""

    paciente = models.ForeignKey(Paciente, related_name='recetas')
    medicamentos = models.TextField(blank=True, null=True)
    notas_adicionales = models.TextField(blank=True, null=True)
    fecha_y_hora = models.DateTimeField(default=timezone.now)
    
    def get_absolute_url(self):
        
        return reverse('consultorio-receta-view', args=[self.id])

class HistoriaClinica(models.Model):

    """Permite ingresar entradas a la Historia Clinica de un
    :class:`Paciente`"""

    paciente = models.ForeignKey(Paciente, related_name='historias_clinicas', null=True)
    nota = models.TextField(blank=True)
    fecha_y_hora = models.DateTimeField(default=timezone.now)
    agudeza_visual_ojo_derecho = models.IntegerField(default=0)
    agudeza_visual_ojo_izquierdo = models.IntegerField(default=0)
    
    def get_absolute_url(self):
        
        return reverse('consultorio-paciente', args=[self.paciente.uuid])

class Optometria(models.Model):

    """Representa los resultados de un examen visual efectuado a un
    :class:`Paciente`"""

    paciente = models.ForeignKey(Paciente, related_name='optometrias')
    fecha_y_hora = models.DateTimeField(default=timezone.now)
    esfera_ojo_derecho = models.DecimalField(default=0, max_digits=5, decimal_places=2) 
    esfera_ojo_izquierdo = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    cilindro_ojo_derecho = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    cilindro_ojo_izquierdo = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    eje_ojo_derecho = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    eje_ojo_izquierdo = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    prisma_ojo_derecho = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    prisma_ojo_izquierdo = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    adicion_ojo_derecho = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    adicion_ojo_izquierdo = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    d_p_ojo_derecho = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    d_p_ojo_izquierdo = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    altura_ojo_derecho = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    altura_ojo_izquierdo = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    notas = models.TextField(blank=True, null=True)
    
    def get_absolute_url(self):
        
        return reverse('consultorio-optometria-view', args=[self.id])
        
        return 'consultorio-optometria-view', [self.id]

class Pago(models.Model):

    """Registra los cobros que se han efectuado a los :class:`Paciente`
    luego de una consulta"""
    
    FORMAS_DE_PAGO = (
        ('E', u'Efectivo'),
        ('T', u'Tarjeta de Crédito'),
        ('C', u'Cheque'),
    )

    paciente = models.ForeignKey(Paciente, related_name='pagos')
    fecha_y_hora = models.DateTimeField(default=timezone.now)
    monto = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    forma_de_pago = models.CharField(max_length=1, choices=FORMAS_DE_PAGO,
                                     blank=True)
    concepto = models.CharField(max_length=255, blank=True)
    
    def get_absolute_url(self):
        
        return reverse('consultorio-view',
                       args=[self.paciente.consultorio.uuid])
