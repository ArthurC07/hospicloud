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

from collections import defaultdict
from decimal import Decimal

from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django_extensions.db.fields import UUIDField
from django_extensions.db.models import TimeStampedModel

from persona.models import Persona, transfer_object_to_persona, \
    persona_consolidation_functions
from emergency.models import Emergencia
from inventory.models import ItemTemplate, TipoVenta

dot01 = Decimal("0.01")


class CargoAdapter(object):
    def __init__(self):
        self.cantidad = 0
        self.detalles = list()
        self.precio_unitario = Decimal(0)
        self.valor = Decimal(0)
        self.descuento = Decimal(0)
        self.subtotal = Decimal(0)

    def __unicode__(self):
        return u'{0} {1}'.format(self.precio_unitario, self.valor)

    def __str__(self):
        return '{0} {1}'.format(self.precio_unitario, self.valor)


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
    item = models.ForeignKey(ItemTemplate, related_name='habitaciones',
                             blank=True, null=True)

    def __unicode__(self):
        return u'{0} {1}'.format(self.get_tipo_display(), self.numero)

    def get_absolute_url(self):
        """Obtiene la URL absoluta de la :class:`Habitacion`"""

        return reverse('habitacion-view', args=[self.id])


class Admision(models.Model):
    """Permite registrar el Ingreso y estadía de una :class:`Persona` en el
    Hospital.
    
    Durante cada :class:`Admision se registran los diversos procedmientos que
    efectuan la :class:`Persona` durante su estadía en el hospital, ya sean
    procedimientos quirúrgicos, examenes de laboratorio, controles de
    enfermería, diversos cargos y otra información adecuada
    """

    class Meta:
        permissions = (
            ('admision', 'Permite al usuario gestionar admision'),
        )

    ESTADOS = (
        ('A', 'Admitido'),
        ('B', 'Autorizado'),
        ('H', 'Hospitalizar'),
        ('I', 'Ingresado'),
        ('C', 'Alta'),
        ('Q', 'Cancelada'),
    )

    ARANCELES = (
        ('E', u"Empleado"),
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
        ("PA", "Particular"),
        ("SN", "Aseguradora Nacional"),
        ("SI", "Aseguradora Internacional"),
        ("PS", "Presupuesto"),
    )

    momento = models.DateTimeField(default=timezone.now, null=True, blank=True)
    paciente = models.ForeignKey(Persona, related_name='admisiones')
    fiadores = models.ManyToManyField(Persona, related_name='fianzas',
                                      blank=True)
    referencias = models.ManyToManyField(Persona, related_name='referencias',
                                         blank=True)

    diagnostico = models.CharField(max_length=200, blank=True)
    doctor = models.CharField(max_length=200, blank=True)

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
    admision = models.DateTimeField(default=timezone.now, null=True, blank=True)
    """Indica la fecha y hora en que la :class:`Persona` fue ingresada en
    admisiones"""
    autorizacion = models.DateTimeField(default=timezone.now, null=True,
                                        blank=True)
    hospitalizacion = models.DateTimeField(null=True, blank=True)
    """Indica la fecha y hora en que la :class:`Persona` fue internada"""
    ingreso = models.DateTimeField(null=True, blank=True)
    """Indica la fecha y hora en que la :class:`Persona` fue enviada al area
    de enfermeria"""
    fecha_pago = models.DateTimeField(default=timezone.now, null=True,
                                      blank=True)
    fecha_alta = models.DateTimeField(default=timezone.now, null=True,
                                      blank=True)
    uuid = UUIDField(version=4)
    estado = models.CharField(max_length=1, blank=True, choices=ESTADOS)
    tiempo = models.IntegerField(default=0, blank=True)
    neonato = models.NullBooleanField(blank=True, null=True)
    tipo_de_ingreso = models.CharField(max_length=200, blank=True, null=True,
                                       choices=TIPOS_INGRESOS)
    facturada = models.NullBooleanField(default=False)
    ultimo_cobro = models.DateTimeField(default=timezone.now, null=True,
                                        blank=True)
    tipo_de_venta = models.ForeignKey(TipoVenta, blank=True, null=True)

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

        if self.hospitalizacion is None or self.hospitalizacion <= self.momento:
            self.estado = 'H'
            self.save()

    def ingresar(self):

        if self.ingreso is None or self.ingreso <= self.momento:
            self.estado = 'I'
            self.save()

    def tiempo_autorizacion(self):

        """Calcula el tiempo que se tarda una :class:`Persona` para ser
        autorizar en el :class:`Hospital`"""

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

        if self.ingreso is None or self.ingreso <= self.hospitalizacion:
            return (timezone.now() - self.hospitalizacion).total_seconds() / 60

        return (self.ingreso - self.hospitalizacion).total_seconds() / 60

    def tiempo_hospitalizado(self):

        """Calcula los días que una :class:`Persona` es atendida en el
        centro hospitalario"""
        dias = 0
        fraccion_dias = 0
        if self.hospitalizacion is None:
            dias = (timezone.now() - self.momento).days
            fraccion_dias = (
                                timezone.now() - self.momento).total_seconds() / 3600 / 24
            if dias < 0:
                dias = 0
            return Decimal(dias + fraccion_dias)

        if self.fecha_alta > self.hospitalizacion:
            dias = (self.fecha_alta - self.hospitalizacion).days
            fraccion_dias = (
                                self.fecha_alta - self.hospitalizacion).seconds / 3600 / 24
            if dias < 0:
                dias = 0
            return Decimal(dias + fraccion_dias)

        if self.ingreso is None or self.ingreso <= self.hospitalizacion:
            dias = (timezone.now() - self.hospitalizacion).days
            fraccion_dias = \
                divmod((timezone.now() - self.hospitalizacion).seconds, 3600)[
                    0] / 24
            if dias < 0:
                dias = 0
            return Decimal(dias + fraccion_dias)

        if self.fecha_alta <= self.hospitalizacion:
            return \
                divmod((timezone.now() - self.hospitalizacion).seconds, 3600)[
                    0] / 24

        dias = (self.fecha_alta - self.hospitalizacion).days
        fraccion_dias = \
            divmod((self.fecha_alta - self.hospitalizacion).seconds, 3600)[
                0] / 24
        if dias < 0:
            dias = 0
        return Decimal(dias + fraccion_dias)

    def tiempo_cobro(self):

        """Permite calcular el tiempo que hace falta por facturar"""

        ahora = timezone.now()
        ultimo = self.hospitalizacion
        if ultimo is None:
            ultimo = self.admision

        if ultimo >= ahora:
            return 0

        dias = (ahora - ultimo).days
        if dias < 1:
            return 1

        if self.estado == 'C':
            return (self.fecha_alta - ultimo).days

        return (ahora - ultimo).days

    def precio_diario(self):

        precio = self.habitacion.item.precio_de_venta

        if not self.tipo_de_venta:
            return precio

        aumento = self.tipo_de_venta.incremento * precio
        return (precio + aumento).quantize(Decimal("0.01"))

    def descuento_diario(self):

        if not self.tipo_de_venta:
            return Decimal(0)
        precio = self.habitacion.item.precio_de_venta

        return self.tipo_de_venta.disminucion * precio

    def descuento_hospitalizacion(self):

        return self.descuento_diario() * self.tiempo_cobro()

    def debido(self):

        """Calcula el monto que aún se debe por conceptio de hospitalización"""

        dias = self.tiempo_cobro()

        if not self.tipo_de_venta:
            return dias * self.habitacion.item.precio_de_venta

        subtotal = (dias * self.precio_diario()).quantize(dot01)
        return subtotal

    def descontado(self):

        return self.debido() - self.descuento_hospitalizacion()

    def dar_alta(self, day):

        self.fecha_alta = day
        self.estado = 'C'
        self.fecha_alta = timezone.now()
        [m.suspender() for m in self.medicamentos.all()]
        self.save()

    def actualizar_tiempo(self):

        """Actualiza el tiempo transcurrido desde el ingreso hasta el momento
        en que se dio de alta"""

        if self.ingreso is None:
            return

        if not self.fecha_alta is None:
            self.tiempo = (self.fecha_alta - self.ingreso).total_seconds() / 60
        else:
            self.tiempo = self.tiempo_ahora()

    def save(self, *args, **kwargs):

        self.actualizar_tiempo()
        super(Admision, self).save(*args, **kwargs)

    def get_absolute_url(self):

        """Obtiene la URL absoluta"""

        return reverse('admision-view-id', args=[self.id])

    def facturar(self):

        """Permite convertir los :class:`Cargo`s de esta :class:`Admision` en
        las :class:`Venta`s de un :class:`Recibo`"""

        items = defaultdict(int)

        items[self.habitacion.item] += self.tiempo_cobro()

        for cargo in self.cargos.all():
            print(cargo)
            items[cargo.cargo] += cargo.cantidad
            cargo.facturada = True
            cargo.save()

        for oxigeno in self.oxigeno_terapias.all():
            items[oxigeno.cargo] += oxigeno.litros()
            oxigeno.facturada = True
            oxigeno.save()

        return items

    def __unicode__(self):

        return u"{0} en {1}".format(self.paciente.nombre_completo(),
            self.habitacion)

    def tiempo_ahora(self):

        """Permite mostrar el tiempo que ha transcurrido desde que se agrego
        la :class:`Admision` al sistema"""

        ahora = timezone.now()

        if self.ultimo_cobro >= ahora:
            return 0

        return (ahora - self.momento).total_seconds() / 60

    def estado_de_cuenta(self, total=False, honorarios=True):

        total = Decimal()
        total += sum(c.valor() for c in self.cargos.all())
        total += self.debido() - self.descuento_hospitalizacion()

        total += sum(h.monto for h in self.honorarios.all())
        total += sum(o.valor() for o in self.oxigeno_terapias.all())

        return total.quantize(dot01)

    def agrupar_cargos(self):

        agrupados = defaultdict(CargoAdapter)

        for cargo in self.cargos.all():
            agrupados[cargo.cargo].cantidad += cargo.cantidad
            agrupados[cargo.cargo].detalles.append(cargo)
            agrupados[cargo.cargo].precio_unitario = cargo.precio_unitario()
            agrupados[cargo.cargo].valor += cargo.valor()
            agrupados[cargo.cargo].descuento += cargo.descuento()
            agrupados[cargo.cargo].subtotal += cargo.subtotal()

        return dict(agrupados)

    def subtotal(self):

        total = Decimal(0)
        total += sum(c.subtotal() for c in self.cargos.all())
        total += self.debido()
        total += sum(h.monto for h in self.honorarios.all())
        total += sum(o.subtotal() for o in self.oxigeno_terapias.all())

        return total.quantize(dot01)

    def descuento(self):

        return sum(c.descuento() for c in
                   self.cargos.all()) + self.descuento_hospitalizacion()

    def total(self):

        return self.estado_de_cuenta(True)


class PreAdmision(TimeStampedModel):
    """Permite ingresar :class:`Personas` desde una :class:`Emergencia` que se
    haya atendido"""

    emergencia = models.ForeignKey(Emergencia, related_name="preadmisiones")
    completada = models.BooleanField(default=False)
    transferir_cobros = models.BooleanField(default=False)

    def get_absolute_url(self):
        """Obtiene la URL absoluta"""

        return reverse('admision-index')

    def __unicode__(self):
        return u"Preadmision de {0} {1}".format(
            self.emergencia.persona.nombre_completo(), self.completada)


class Doctor(TimeStampedModel):
    nombre = models.CharField(max_length=50)


class Laboratorio(TimeStampedModel):
    nombre = models.CharField(max_length=50)

    def __unicode__(self):
        return self.nombre


class Deposito(TimeStampedModel):
    admision = models.ForeignKey(Admision, related_name='depositos')
    monto = models.DecimalField(blank=True, null=True, max_digits=7,
                                decimal_places=2)
    fecha = models.DateTimeField(default=timezone.now, null=True, blank=True)
    recibo = models.IntegerField(null=True, blank=True)

    def get_absolute_url(self):
        """Obtiene la URL absoluta"""

        return reverse('admision-view-id', args=[self.admision.id])


def consolidate_spital(persona, clone):
    [move_admision(persona, admision) for admision in clone.admisiones.all()]


def move_admision(persona, admision):
    admision.paciente = persona
    admision.save()


persona_consolidation_functions.append(consolidate_spital)
