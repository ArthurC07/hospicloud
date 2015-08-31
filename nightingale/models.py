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

from datetime import timedelta
from decimal import Decimal

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django_extensions.db.models import TimeStampedModel

from spital.models import Admision
from inventory.models import ItemTemplate


dot01 = Decimal('0.01')


class Precio(object):
    def precio_unitario(self):

        tipo_de_venta = self.admision.tipo_de_venta
        precio_de_venta = self.cargo.precio_de_venta

        if not tipo_de_venta:
            return precio_de_venta

        aumento = tipo_de_venta.incremento * precio_de_venta

        return (precio_de_venta + aumento).quantize(dot01)

    def descuento(self):

        tipo_de_venta = self.admision.tipo_de_venta

        if not tipo_de_venta:
            return Decimal(0)

        disminucion = tipo_de_venta.disminucion * self.cantidad

        return disminucion * self.cargo.precio_de_venta


class Turno(object):
    def get_turno(self):
        pass


class SignoVital(models.Model, Turno):
    """Registra los signos vitales de una :class:`Persona` durante una
    :class:`Admision` en el  Hospital"""

    admision = models.ForeignKey(Admision, related_name='signos_vitales')
    fecha_y_hora = models.DateTimeField(default=timezone.now)
    pulso = models.IntegerField()
    temperatura = models.DecimalField(decimal_places=2, max_digits=8,
                                      null=True)
    presion_sistolica = models.DecimalField(decimal_places=2, max_digits=8,
                                            null=True)
    presion_diastolica = models.DecimalField(decimal_places=2, max_digits=8,
                                             null=True)
    respiracion = models.DecimalField(decimal_places=2, max_digits=8, null=True)
    observacion = models.TextField(blank=True, null=True)
    saturacion_de_oxigeno = models.DecimalField(decimal_places=2, max_digits=8,
                                                null=True)
    presion_arterial_media = models.CharField(max_length=200, blank=True)
    usuario = models.ForeignKey(User, blank=True, null=True,
                                related_name='signos_vitales')

    def get_absolute_url(self):
        """Obtiene la URL absoluta"""

        return reverse('enfermeria-signos', args=[self.admision.id])

    def save(self, *args, **kwargs):
        """Permite guardar los datos mientras calcula algunos campos
        automaticamente"""

        self.presion_arterial_media = float(self.presion_diastolica) + (
            float(1) / float(3) * float(self.presion_sistolica -
                                        self.presion_diastolica))

        super(SignoVital, self).save(*args, **kwargs)


Admision.temperatura_promedio = property(lambda a:
                                         sum(s.temperatura for s
                                             in a.signos_vitales.all())
                                         / a.signos_vitales.count())

Admision.pulso_promedio = property(lambda a:
                                   sum(s.pulso for s in a.signos_vitales.all())
                                   / a.signos_vitales.count())

Admision.presion_sistolica_promedio = property(lambda a:
                                               sum(s.presion_sistolica for s
                                                   in a.signos_vitales.all())
                                               / a.signos_vitales.count())

Admision.presion_diastolica_promedio = property(lambda a:
                                                sum(s.presion_diastolica for s
                                                    in a.signos_vitales.all())
                                                / a.signos_vitales.count())


class Evolucion(models.Model):
    """Registra la evolución de la :class:`Persona durante una
    :class:`Admision`"""

    admision = models.ForeignKey(Admision, related_name='evoluciones')
    fecha_y_hora = models.DateTimeField(default=timezone.now)
    nota = models.TextField(blank=True)
    usuario = models.ForeignKey(User, blank=True, null=True,
                                related_name='evoluciones')

    def get_absolute_url(self):
        """Obtiene la URL absoluta"""

        return reverse('enfermeria-evolucion', args=[self.admision.id])


class Cargo(TimeStampedModel, Precio):
    """Indica los cargos en base a los diversos """

    class Meta:
        permissions = (
            ('enfermeria', 'Permite al usuario gestionar hospitalizaciones'),
            ('enfermeria_ver', 'Permite al usuario ver datos'),
        )

    admision = models.ForeignKey(Admision, related_name='cargos')
    cargo = models.ForeignKey(ItemTemplate, blank=True, null=True,
                              related_name='cargos')
    cantidad = models.DecimalField(max_digits=8, decimal_places=2, default=1)
    usuario = models.ForeignKey(User, blank=True, null=True,
                                related_name='cargos')
    facturada = models.NullBooleanField(default=False)

    def get_absolute_url(self):
        """Obtiene la URL absoluta"""

        return reverse('enfermeria-cargo-agregar', args=[self.admision.id])

    def subtotal(self):
        return (self.cantidad * self.precio_unitario()).quantize(dot01)

    def valor(self):
        return (self.subtotal() - self.descuento()).quantize(dot01)


class OrdenMedica(models.Model):
    """Registra las indicaciones a seguir por el personal de enfermeria"""

    admision = models.ForeignKey(Admision, related_name='ordenes_medicas')
    evolucion = models.TextField(blank=True)
    orden = models.TextField(blank=True)
    fecha_y_hora = models.DateTimeField(default=timezone.now)
    doctor = models.CharField(blank=True, null=True, max_length=255)
    usuario = models.ForeignKey(User, blank=True, null=True,
                                related_name='ordenes_medicas')

    def get_absolute_url(self):
        """Obtiene la URL absoluta"""

        return reverse('enfermeria-ordenes', args=[self.admision.id])


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

    def get_absolute_url(self):
        """Obtiene la URL absoluta"""

        return reverse('enfermeria-ingestas-excretas', args=[self.admision.id])


class Excreta(models.Model, Turno):
    """Registra las excresiones de una :class:`Persona` durante una
    :class:`Admision`"""

    MEDIOS = (
        ("S", u"Succión"),
        ("O", "Orina"),
        ("V", "Vomito"),
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

    def get_absolute_url(self):
        """Obtiene la URL absoluta"""

        return reverse('enfermeria-ingestas-excretas', args=[self.admision.id])


class NotaEnfermeria(models.Model, Turno):
    """Nota agregada a una :class:`Admision` por el personal de Enfermeria"""

    admision = models.ForeignKey(Admision, related_name='notas_enfermeria')
    fecha_y_hora = models.DateTimeField(default=timezone.now)
    nota = models.TextField(blank=True)
    usuario = models.ForeignKey(User, blank=True, null=True,
                                related_name='notas_enfermeria')
    autor = models.CharField(max_length=200, blank=True)
    cerrada = models.BooleanField(default=False)

    def get_absolute_url(self):
        """Obtiene la URL absoluta"""

        return reverse('enfermeria-notas', args=[self.admision.id])


class Glicemia(models.Model, Turno):
    """Registra las fluctuaciones en los niveles de Glucosa en la sangre de una
    :class:`Persona` durante una :class`Admision`"""

    admision = models.ForeignKey(Admision, related_name='glicemias')
    fecha_y_hora = models.DateTimeField(default=timezone.now)
    control = models.CharField(max_length=200, blank=True)
    observacion = models.CharField(max_length=200, blank=True)
    usuario = models.ForeignKey(User, blank=True, null=True,
                                related_name='glicemias')

    def get_absolute_url(self):
        """Obtiene la URL absoluta"""

        return reverse('enfermeria-glucometria', args=[self.admision.id])


class Glucosuria(models.Model, Turno):
    """Registra la expulsión de Glucosa mediante la orina"""

    admision = models.ForeignKey(Admision, related_name='glucosurias')
    fecha_y_hora = models.DateTimeField(default=timezone.now)
    control = models.CharField(max_length=200, blank=True)
    observacion = models.TextField(blank=True)
    usuario = models.ForeignKey(User, blank=True, null=True,
                                related_name='glucosurias')

    def get_absolute_url(self):
        """Obtiene la URL absoluta"""

        return reverse('enfermeria-glucometria', args=[self.admision.id])


class Insulina(models.Model, Turno):
    """Registra la expulsión de Glucosa mediante la orina"""

    admision = models.ForeignKey(Admision, related_name='insulina')
    fecha_y_hora = models.DateTimeField(default=timezone.now)
    control = models.CharField(max_length=200, blank=True)
    observacion = models.CharField(max_length=200, blank=True)
    usuario = models.ForeignKey(User, blank=True, null=True,
                                related_name='insulinas')

    def get_absolute_url(self):
        """Obtiene la URL absoluta"""

        return reverse('enfermeria-glucometria', args=[self.admision.id])


class Sumario(TimeStampedModel):
    """Registra los datos de una :class:`Persona` al momento de darle de alta
    de una :class:`Admision`"""

    admision = models.OneToOneField(Admision)
    diagnostico = models.TextField(blank=True)
    procedimiento_efectuado = models.TextField(blank=True)
    condicion = models.TextField(blank=True)
    recomendaciones = models.TextField(blank=True)
    usuario = models.ForeignKey(User, blank=True, null=True,
                                related_name='sumarios')
    fecha = models.DateTimeField(blank=True, null=True)

    def get_absolute_url(self):
        """Obtiene la URL absoluta"""

        return reverse('nightingale-view-id', args=[self.admision.id])

    def save(self, **kwargs):
        self.admision.dar_alta(self.fecha)
        super(Sumario, self).save(**kwargs)


Admision.sumario = property(
    lambda a: Sumario.objects.get_or_create(admision=a)[0])


class FrecuenciaLectura(models.Model):
    """Indica cada cuanto se debe tomar una :class:`Glucometria` y una lectura
    de :class:`SignosVitales`"""

    admision = models.OneToOneField(Admision)
    glucometria = models.IntegerField(default=0, blank=True)
    signos_vitales = models.IntegerField(default=0, blank=True)

    def get_absolute_url(self):
        """Obtiene la URL absoluta"""

        return reverse('nightingale-view-id', args=[self.admision.id])


Admision.frecuencia_lectura = property(
    lambda a: FrecuenciaLectura.objects.get_or_create(admision=a)[0]
)


class Medicamento(TimeStampedModel):
    """Permite A un :class:`User` recetar una droga que debera ser administrada
    a una :class:`Persona` durante una :class:`Admision`.
    
    Esta droga puede administrarse a intervalos determinados por el doctor,
    dichos intervalos son medidos en horas.
    """

    INTERVALOS = (
        (24, u"Cada 24 Horas"),
        (12, u"Cada 12 Horas"),
        (8, u"Cada 8 Horas"),
        (6, u"Cada 6 Horas"),
        (4, u"Cada 4 Horas"),
    )

    ESTADOS = (
        (1, u"Activo"),
        (2, u"Suspendido"),
        (3, u"Terminado"),
    )

    admision = models.ForeignKey(Admision, related_name='medicamentos')
    cargo = models.ForeignKey(ItemTemplate, blank=True, null=True,
                              related_name='medicamentos')
    inicio = models.DateTimeField(default=timezone.now)
    intervalo = models.IntegerField(blank=True, null=True, choices=INTERVALOS)
    unidades = models.CharField(max_length=200, blank=True)
    repeticiones = models.IntegerField(blank=True, null=True)
    usuario = models.ForeignKey(User, blank=True, null=True,
                                related_name='medicamentos')
    estado = models.IntegerField(blank=True, null=True, choices=ESTADOS,
                                 default=1)
    ultima_dosis = models.DateTimeField(default=timezone.now)
    proxima_dosis = models.DateTimeField(default=timezone.now)
    suministrado = models.IntegerField(default=0)

    def get_absolute_url(self):

        """Obtiene la URL absoluta"""

        return reverse('enfermeria-cargos', args=[self.admision.id])

    def suministrar(self, hora, usuario):

        """Crea un :class:`Cargo` basado en una Dosis del Medicamento"""

        if self.suministrado >= self.repeticiones:
            return

        cargo = Cargo()
        cargo.admision = self.admision
        cargo.created = hora
        cargo.cargo = self.cargo
        cargo.usuario = usuario
        cargo.save()

        self.ultima_dosis = timezone.now()
        print(timedelta(hours=self.intervalo))
        self.proxima_dosis = self.ultima_dosis + timedelta(hours=self.intervalo)

        self.suministrado += 1
        if self.suministrado == self.repeticiones:
            self.estado = 3

        self.save()

    def suspender(self):

        self.estado = 2
        self.save()

    def save(self, *args, **kwargs):

        if self.suministrado < self.repeticiones:
            self.estado = 1

        return super(Medicamento, self).save(*args, **kwargs)


class Dosis(TimeStampedModel, Turno):
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
    estado = models.IntegerField(blank=True, null=True, choices=ESTADOS,
                                 default=1)
    recomendacion = models.CharField(max_length=200, blank=True, null=True)
    usuario = models.ForeignKey(User, blank=True, null=True,
                                related_name='dosis')

    def get_absolute_url(self):
        """Obtiene la URL absoluta"""

        return reverse('enfermeria-medicamentos',
                       args=[self.medicamento.admision.id])


class Devolucion(TimeStampedModel, Turno):
    """Representa todos aquellos materiales que han sido devueltos"""

    admision = models.ForeignKey(Admision, related_name='devoluciones')
    cargo = models.ForeignKey(ItemTemplate, blank=True, null=True,
                              related_name='devoluciones')
    descripcion = models.TextField(max_length=200, blank=True, null=True)
    usuario = models.ForeignKey(User, blank=True, null=True,
                                related_name='devoluciones')

    def get_absolute_url(self):
        """Obtiene la URL absoluta"""

        return reverse('enfermeria-medicamentos',
                       args=[self.medicamento.admision.id])


class OxigenoTerapia(TimeStampedModel, Precio):
    """Registra los tiempos en los cuales el paciente ha utilizado oxigeno"""

    admision = models.ForeignKey(Admision, related_name='oxigeno_terapias')
    cargo = models.ForeignKey(ItemTemplate, blank=True, null=True,
                              related_name='oxigeno_terapias')
    terminada = models.BooleanField(default=False)
    inicio = models.DateTimeField(null=True, blank=True)
    fin = models.DateTimeField(null=True, blank=True)
    facturada = models.NullBooleanField(default=False)

    def get_absolute_url(self):
        """Obtiene la URL absoluta"""

        return reverse('enfermeria-oxigeno', args=[self.admision.id])

    def tiempo(self):
        """Calcula el tiempo que la :class:`Persona` ha utilizado Oxigeno"""

        if self.fin is None or self.inicio is None:
            return 0

        delta = self.fin - self.inicio
        return delta.days * 24 + (delta.seconds / 3600)

    def litros(self):
        """Calcula el volumen de Oxigeno utilizado"""

        return self.tiempo() * 180

    def subtotal(self):

        return (self.litros() * self.precio_unitario()).quantize(dot01)

    def descuento(self):

        if not self.admision.tipo_de_venta:
            return Decimal(0)

        disminucion = self.admision.tipo_de_venta.disminucion * self.litros()

        return disminucion * self.precio_unitario()

    def valor(self):
        return self.subtotal() - self.descuento()

    def final(self):
        if self.created >= self.modified:
            return timezone.now()

        return self.fin


class Honorario(TimeStampedModel):
    """Permite agregar un cargo que no utiliza los precios predefinidos"""

    admision = models.ForeignKey(Admision, related_name='honorarios')
    item = models.ForeignKey(ItemTemplate, blank=True, null=True,
                             related_name='honorarios')
    monto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    medico = models.CharField(max_length=200, blank=True)
    facturada = models.NullBooleanField(default=False)
    usuario = models.ForeignKey(User, blank=True, null=True,
                                related_name='honorarios')

    def get_absolute_url(self):
        """Obtiene la URL absoluta"""

        return reverse('enfermeria-honorarios', args=[self.admision.id])
