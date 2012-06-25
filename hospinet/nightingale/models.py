# -*- coding: utf-8 -*-
from django.db import models
from spital.models import Admision
from datetime import time
from django.utils import timezone
from django.db.models import permalink
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from actstream import action

class Turno(object):

    def get_turno(self):

        hora = timezone.localtime(self.fecha_y_hora.time())
        a_inicio = time(7, tzinfo=hora.tzinfo)
        b_inicio = time(15, tzinfo=hora.tzinfo)
        c_inicio = time(21, tzinfo=hora.tzinfo)
        print hora, a_inicio, b_inicio, c_inicio
        if hora > a_inicio and hora < b_inicio:

            return u"turno-a"

        if hora > b_inicio and hora < c_inicio:

            return u"turno-b"

        if hora > c_inicio or hora < a_inicio:

            return u"turno-c"

class SignoVital(models.Model, Turno):
    
    """Registra los signos vitales de una :class:`Persona` durante una
    :class:`Admision` en el  Hospital"""
    
    admision = models.ForeignKey(Admision, related_name='signos_vitales')
    fecha_y_hora = models.DateTimeField(default=timezone.now)
    pulso = models.IntegerField()
    temperatura = models.DecimalField(decimal_places=2, max_digits=8, null=True)
    presion_sistolica = models.DecimalField(decimal_places=2, max_digits=8, null=True)
    presion_diastolica = models.DecimalField(decimal_places=2, max_digits=8, null=True)
    respiracion = models.DecimalField(decimal_places=2, max_digits=8, null=True)
    observacion = models.TextField(blank=True, null=True)
    saturacion_de_oxigeno = models.DecimalField(decimal_places=2, max_digits=8,
                                                null=True)
    presion_arterial_media = models.CharField(max_length=200, blank=True)
    usuario = models.ForeignKey(User, blank=True, null=True,
                                   related_name='signos_vitales')
    
    @permalink
    def get_absolute_url(self):
        
        """Obtiene la URL absoluta"""
        
        return 'nightingale-view-id', [self.admision.id]
    
    def save(self, *args, **kwargs):

        """Permite guardar los datos mientras calcula algunos campos
        automaticamente"""

        self.presion_arterial_media = float(self.presion_diastolica) + float(1) / float(3) * float(self.presion_sistolica -self.presion_diastolica)

        super(SignoVital, self).save(*args, **kwargs)

Admision.temperatura_promedio = property(lambda a:
                                 sum(s.temperatura for s in a.signos_vitales.all())
                                 / a.signos_vitales.count())

Admision.pulso_promedio = property(lambda a:
                                 sum(s.pulso for s in a.signos_vitales.all())
                                 / a.signos_vitales.count())

Admision.presion_sistolica_promedio = property(lambda a:
                                 sum(s.presion_sistolica for s in a.signos_vitales.all())
                                 / a.signos_vitales.count())

Admision.presion_diastolica_promedio = property(lambda a:
                                 sum(s.presion_diastolica for s in a.signos_vitales.all())
                                 / a.signos_vitales.count())

class Evolucion(models.Model):
    
    """Registra la evolución de la :class:`Persona durante una
    :class:`Admision`"""
    
    admision = models.ForeignKey(Admision, related_name='evoluciones')
    fecha_y_hora = models.DateTimeField(default=timezone.now)
    nota = models.CharField(max_length=200, blank=True)
    usuario = models.ForeignKey(User, blank=True, null=True,
                                   related_name='evoluciones')
    
    @permalink
    def get_absolute_url(self):
        
        """Obtiene la URL absoluta"""
        
        return 'nightingale-view-id', [self.admision.id]

class Cargo(models.Model, Turno):
    
    """Indica los cargos en base a aparatos que utiliza una :class:`Persona`"""
    
    admision = models.ForeignKey(Admision, related_name='cargos')
    fecha_y_hora = models.DateTimeField(default=timezone.now)
    cargo = models.TextField(max_length=200)
    inicio = models.DateTimeField(default=timezone.now)
    fin = models.DateTimeField(default=timezone.now)
    usuario = models.ForeignKey(User, blank=True, null=True,
                                   related_name='cargos')
    
    @permalink
    def get_absolute_url(self):
        
        """Obtiene la URL absoluta"""
        
        return 'nightingale-view-id', [self.admision.id]

class OrdenMedica(models.Model):
    
    """Registra las indicaciones a seguir por el personal de enfermeria"""
    
    admision = models.ForeignKey(Admision, related_name='ordenes_medicas')
    orden = models.CharField(max_length=200, blank=True)
#    doctor = models.CharField(max_length=200, blank=True)
    fecha_y_hora = models.DateTimeField(default=timezone.now)
    usuario = models.ForeignKey(User, blank=True, null=True,
                                   related_name='ordenes_medicas')
    
    @permalink
    def get_absolute_url(self):
        
        """Obtiene la URL absoluta"""
        
        return 'nightingale-view-id', [self.admision.id]

class Ingesta(models.Model, Turno):
    
    """Registra las ingestas que una :class:`Persona`"""
    
    admision = models.ForeignKey(Admision, related_name='ingestas')
    fecha_y_hora = models.DateTimeField(default=timezone.now)
    ingerido = models.CharField(max_length=200, blank=True)
    cantidad = models.IntegerField()
    liquido = models.NullBooleanField(blank=True, null=True)
    via = models.CharField(max_length=200, blank=True, null=True)
    usuario = models.ForeignKey(User, blank=True, null=True,
                                   related_name='ingestas')
    
    @permalink
    def get_absolute_url(self):
        
        """Obtiene la URL absoluta"""
        
        return 'enfermeria-ingestas-excretas', [self.admision.id]

class Excreta(models.Model, Turno):
    
    """Registra las excresiones de una :class:`Persona` durante una
    :class:`Admision`"""
    
    MEDIOS = (
        ("S", u"Succión"),
        ("O","Orina"),
        ("V","Vomito"),
    )
    
    admision = models.ForeignKey(Admision, related_name='excretas')
    fecha_y_hora = models.DateTimeField(default=timezone.now)
    medio = models.CharField(max_length=2, blank=True, choices=MEDIOS)
    cantidad = models.CharField(max_length=200, blank=True)
    descripcion = models.CharField(max_length=200, blank=True)
    otro = models.CharField(max_length=200, blank=True)
    otros = models.CharField(max_length=200, blank=True)
    usuario = models.ForeignKey(User, blank=True, null=True,
                                   related_name='excretas')
    
    @permalink
    def get_absolute_url(self):
        
        """Obtiene la URL absoluta"""
        
        return 'enfermeria-ingestas-excretas', [self.admision.id]

class NotaEnfermeria(models.Model, Turno):
    
    """Nota agregada a una :class:`Admision` por el personal de Enfermeria"""
    
    admision = models.ForeignKey(Admision, related_name='notas_enfermeria')
    fecha_y_hora = models.DateTimeField(default=timezone.now)
    nota = models.TextField(blank=True)
    usuario = models.ForeignKey(User, blank=True, null=True,
                                   related_name='notas_enfermeria')
    cerrada = models.BooleanField(default=False)
    
    @permalink
    def get_absolute_url(self):
        
        """Obtiene la URL absoluta"""
        
        return 'enfermeria-notas', [self.admision.id]

class Glicemia(models.Model, Turno):
    
    """Registra las fluctuaciones en los niveles de Glucosa en la sangre de una
    :class:`Persona` durante una :class`Admision`"""
    
    admision = models.ForeignKey(Admision, related_name='glicemias')
    fecha_y_hora = models.DateTimeField(default=timezone.now)
    control = models.CharField(max_length=200, blank=True)
    observacion = models.CharField(max_length=200, blank=True)
    usuario = models.ForeignKey(User, blank=True, null=True,
                                   related_name='glicemias')
    
    @permalink
    def get_absolute_url(self):
        
        """Obtiene la URL absoluta"""
        
        return 'nightingale-glucometria-id', [self.admision.id]

class Glucosuria(models.Model, Turno):

    """Registra la expulsión de Glucosa mediante la orina"""

    admision = models.ForeignKey(Admision, related_name='glucosurias')
    fecha_y_hora = models.DateTimeField(default=timezone.now)
    control = models.CharField(max_length=200, blank=True)
    observacion = models.TextField(blank=True)
    usuario = models.ForeignKey(User, blank=True, null=True,
                                   related_name='glucosurias')
    
    @permalink
    def get_absolute_url(self):
        
        """Obtiene la URL absoluta"""
        
        return 'nightingale-glucometria-id', [self.admision.id]

class Insulina(models.Model, Turno):

    """Registra la expulsión de Glucosa mediante la orina"""

    admision = models.ForeignKey(Admision, related_name='insulina')
    fecha_y_hora = models.DateTimeField(default=timezone.now)
    control = models.CharField(max_length=200, blank=True)
    observacion = models.CharField(max_length=200, blank=True)
    usuario = models.ForeignKey(User, blank=True, null=True,
                                   related_name='insulinas')
    
    @permalink
    def get_absolute_url(self):
        
        """Obtiene la URL absoluta"""
        
        return 'nightingale-glucometria-id', [self.admision.id]

class Sumario(models.Model):
    
    """Registra los datos de una :class:`Persona` al momento de darle de alta
    de una :class:`Admision`"""
    
    admision = models.OneToOneField(Admision)
    diagnostico = models.TextField(blank=True)
    procedimiento_efectuado = models.TextField(blank=True)
    condicion = models.TextField(blank=True)
    recomendaciones = models.TextField(blank=True)
    usuario = models.ForeignKey(User, blank=True, null=True,
                                   related_name='sumarios')
    
    @permalink
    def get_absolute_url(self):
        
        """Obtiene la URL absoluta"""
        
        return 'nightingale-view-id', [self.admision.id]

Admision.sumario = property(lambda a: Sumario.objects.get_or_create(admision=a)[0])

class FrecuenciaLectura(models.Model):
    
    """Indica cada cuanto se debe tomar una :class:`Glucometria` y una lectura
    de :class:`SignosVitales`"""
    
    admision = models.OneToOneField(Admision)
    glucometria = models.IntegerField(default=0,blank=True)
    signos_vitales = models.IntegerField(default=0,blank=True)
    
    @permalink
    def get_absolute_url(self):
        
        """Obtiene la URL absoluta"""
        
        return 'nightingale-view-id', [self.admision.id]

Admision.frecuencia_lectura = property(lambda a: FrecuenciaLectura.objects.get_or_create(admision=a)[0])

class Medicamento(models.Model):
    
    """Permite A un :class:`User` recetar una droga que debera ser administrada
    a una :class:`Persona` durante una :class:`Admision`.
    
    Esta droga puede administrarse a intervalos determinados por el doctor,
    dichos intervalos son medidos en horas.
    """

    INTERVALOS = (
        (1, u"Una vez al día"),
        (2, u"Dos veces al día"),
        (3, u"Tres veces al día"),
        (4, u"Cuatro veces al día"),
        (6, u"Seis veces al día"),
    )

    ESTADOS = (
        (1, u"Activo"),
        (2, u"Suspendido"),
        (3, u"Terminado"),
    )

    admision = models.ForeignKey(Admision, related_name='medicamentos')
    nombre = models.CharField(max_length=200, blank=True, null=True)
    fecha_y_hora = models.DateTimeField(default=timezone.now)
    inicio = models.DateTimeField(default=timezone.now)
    intervalo = models.IntegerField(blank=True, null=True, choices=INTERVALOS)
    dias = models.IntegerField(blank=True, null=True)
    control = models.CharField(max_length=200, blank=True, null=True)
    usuario = models.ForeignKey(User, blank=True, null=True,
                                   related_name='medicamentos')
    estado = models.IntegerField(blank=True, null=True, choices=ESTADOS, default=1)
    
    @permalink
    def get_absolute_url(self):
        
        """Obtiene la URL absoluta"""
        
        return 'enfermeria-medicamentos', [self.admision.id]

class Dosis(models.Model, Turno):

    """Permite llevar un control sobre los momentos en los que se debe
    administrar un :class:`Medicamento` y saber quien los ha administrado a la
    :class:`Persona`"""

    ESTADOS = (
        (1, u"Pendiente"),
        (2, u"Rechazada"),
        (3, u"Administrada"),
    )

    medicamento = models.ForeignKey(Medicamento, related_name='dosis',
                                   on_delete=models.CASCADE)
    fecha_y_hora = models.DateTimeField(default=timezone.now)
    estado = models.IntegerField(blank=True, null=True, choices=ESTADOS, default=1)
    recomendacion = models.CharField(max_length=200, blank=True, null=True)
    usuario = models.ForeignKey(User, blank=True, null=True, related_name='dosis')
    administrador = models.ForeignKey(User, blank=True, null=True,
                                      related_name='dosis_administradas',
                                      on_delete=models.CASCADE)
    
    @permalink
    def get_absolute_url(self):
        
        """Obtiene la URL absoluta"""
        
        return 'enfermeria-medicamentos', [self.admision.id]

class Devolucion(models.Model, Turno):

    """Representa todos aquellos materiales que han sido devueltos"""

    admision = models.ForeignKey(Admision, related_name='devoluciones')
    descripcion = models.TextField(max_length=200, blank=True, null=True)
    fecha_y_hora = models.DateTimeField(default=timezone.now)
    usuario = models.ForeignKey(User, blank=True, null=True,
                                   related_name='devoluciones')

def action_register_handler(sender, instance, created, **kwargs):
    action.send(instance, verb='fue guardado')

post_save.connect(action_register_handler, sender=SignoVital)
post_save.connect(action_register_handler, sender=Evolucion)
post_save.connect(action_register_handler, sender=Cargo)
post_save.connect(action_register_handler, sender=NotaEnfermeria)
post_save.connect(action_register_handler, sender=Ingesta)
post_save.connect(action_register_handler, sender=Excreta)
post_save.connect(action_register_handler, sender=OrdenMedica)
post_save.connect(action_register_handler, sender=Glicemia)
post_save.connect(action_register_handler, sender=Glucosuria)
post_save.connect(action_register_handler, sender=Insulina)
post_save.connect(action_register_handler, sender=Sumario)
post_save.connect(action_register_handler, sender=Medicamento)
post_save.connect(action_register_handler, sender=Dosis)
