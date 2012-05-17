# -*- coding: utf-8 -*-
from datetime import datetime
from django.db import models
from persona.models import Persona
from users.models import Profile
from django.contrib.auth.models import User

class Consultorio(models.Model):
    
    doctor = models.ManyToManyField(Profile, related_name='consultorios')
    nombre = models.CharField(max_length=1, blank=True)
    secretaria = models.ForeignKey(User, blank=True, null=True, related_name='consultorios')
    
    def balance(self):
        
        return sum(p.saldo() for p in self.pacientes)

class Paciente(models.Model):
    
    persona = models.ForeignKey(Persona, related_name='consultorios')
    consultorio = models.ForeignKey(Consultorio, related_name='pacientes')
    
    def saldo(self):
        
        return sum(t.monto for t in self.transacciones)

Persona.saldo = property(lambda p: sum(c.saldo() for c in p.consultorios))

class Visitante(models.Model):
    
    ESTADOS = (
        ('E', u'Esperando'),
        ('C', u'Consulta'),
        ('A', u'Atendido'),
    )
    
    consultorio = models.ForeignKey(Consultorio, related_name='visitantes')
    nombre = models.CharField(max_length=200)
    estado = models.CharField(max_length=1, blank=True, choices=ESTADOS)
    llegada = models.DateTimeField(default=datetime.now)
    programacion = models.DateTimeField(default=datetime.now)

class Transaccion(models.Model):
    
    TIPO = (
        (1, u'Crédito'),
        (2, u'Débito')
    )
    
    paciente = models.ForeignKey(Paciente, related_name='transacciones')
    concepto = models.CharField(max_length=1, blank=True)
    tipo = models.IntegerField(choices=TIPO)
    monto = models.DecimalField()
    fecha_y_hora = models.DateTimeField(default=datetime.now)

class Cita(models.Model):
    
    consultorio = models.ForeignKey(Consultorio, related_name='citas')
    persona = models.CharField(max_length=255, blank=True)
    fecha_y_hora = models.DateTimeField(default=datetime.now())
