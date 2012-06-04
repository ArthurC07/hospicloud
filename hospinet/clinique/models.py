# -*- coding: utf-8 -*-
from datetime import datetime
from django.db import models
from persona.models import Persona
from users.models import Profile
from django.db.models import permalink
from django_extensions.db.fields import UUIDField

class Consultorio(models.Model):
    
    """Permite que un :class:`User` pueda llevar un control privado de la
    atención privada que le ha facilitado a una :class:`Persona`"""
    
    nombre = models.CharField(max_length=255, blank=True)
    secretaria = models.ForeignKey(Profile, blank=True, null=True,
                                   related_name='secretariados')
    doctor = models.ForeignKey(Profile, blank=True, null=True,
                                   related_name='consultorios')
    uuid = UUIDField(version=4)
    
    def balance(self):
        
        """Obtiene el total de las cuentas por cobrar de un
        :class:`Consultorio`"""
        
        return sum(p.saldo() for p in self.pacientes)
    
    @permalink
    def get_absolute_url(self):
        
        """Obtiene la URL absoluta"""
        
        return 'consultorio-view', [self.uuid]

Profile.balance = property(lambda u: sum(c.balance() for c in u.consultorios))

class Paciente(models.Model):
    
    """Relaciona a una :class:`Persona` con un :class:`Consultorio` para
    ayudar a proteger la privacidad de dicha :class:`Persona` ya que se
    restringe el acceso a la información básica y a los datos ingresados por
    el :class:`User` al que pertenece el :class:`Consultorio`"""
    
    persona = models.ForeignKey(Persona, related_name='consultorios')
    consultorio = models.ForeignKey(Consultorio, related_name='pacientes')
    uuid = UUIDField(version=4)
    
    def saldo(self):
        
        """Obtiene el valor total de las :class:`Transacciones` efectuadas
        entre el :class:`User` y la :class:`Persona`"""

        creditos =  sum(t.monto for t in self.transacciones if t.tipo == 1)
        debitos =  sum(t.monto for t in self.transacciones if t.tipo == 2)
        
        return creditos - debitos
    
    @permalink
    def get_absolute_url(self):
        
        """Obtiene la url relacionada con un :class:`Paciente`"""
        
        return 'consultorio-paciente', [self.uuid]

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
    fecha_y_hora = models.DateTimeField(default=datetime.now)

class Cita(models.Model):
    
    """Permite registrar las posibles :class:`Personas`s que serán atendidas
    en una fecha determinada""" 
    
    consultorio = models.ForeignKey(Consultorio, related_name='citas')
    nombre = models.CharField(max_length=200)
    fecha_y_hora = models.DateTimeField(default=datetime.now())

class Esperador(models.Model):
    
    """Permite agregar una :class:`Persona` a la lista de :class:`Paciente`s en
    la sala de espera"""
    
    consultorio = models.ForeignKey(Consultorio, related_name='esperadores')
    paciente = models.ForeignKey(Paciente, related_name='esperas')
    atendido = models.BooleanField(default=False)
