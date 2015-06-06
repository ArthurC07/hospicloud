# !/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2011-2014 Carlos Flores <cafg10@gmail.com>
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
import calendar
from datetime import date, timedelta, datetime
from decimal import Decimal
import operator

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Q
from django.utils import timezone

from django_extensions.db.models import TimeStampedModel
import unicodecsv

from clinique.models import Consulta, Seguimiento, Cita
from inventory.models import ItemTemplate, ItemType
from persona.models import Persona, Empleador, transfer_object_to_persona, \
    persona_consolidation_functions

server_timezone = timezone.get_current_timezone()


class Vendedor(TimeStampedModel):
    """Indica quien realizo una venta de un :clas:`Contrato`"""
    usuario = models.ForeignKey(User, related_name="vendedores")
    habilitado = models.BooleanField(default=True)

    def __unicode__(self):
        return self.usuario.get_full_name()

    def get_contratos_vendidos(self, fecha, fin):
        return Contrato.objects.filter(inicio__gte=fecha, cancelado=False,
                                       inicio__lte=fin, vendedor=self)

    def get_absolute_url(self):
        """Obtiene la url relacionada con un :class:`Vendedor`"""

        return reverse('contracts-vendedor', args=[self.id])

    def get_contratos_mes(self):
        now = date.today()
        inicio = date(now.year, now.month, 1)
        fin = date(now.year, now.month,
                   calendar.monthrange(now.year, now.month)[1])
        return self.get_contratos_vendidos(inicio, fin).count()


class Aseguradora(TimeStampedModel):
    nombre = models.CharField(max_length=255, blank=True)
    representante = models.CharField(max_length=255, blank=True, default='')
    cardex = models.ForeignKey(Persona, null=True, blank=True,
                               related_name='cardex')

    def __unicode__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('aseguradora', args=[self.id])


class Plan(TimeStampedModel):
    """Indica los limites que presenta cada :class:`Contrato`"""

    nombre = models.CharField(max_length=255, null=True, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    edad_maxima = models.IntegerField()
    consulta = models.ForeignKey(ItemTemplate, null=True, blank=True,
                                 related_name='plan')
    item = models.ForeignKey(ItemTemplate, null=True, blank=True,
                             related_name='planes_precio')

    def __unicode__(self):
        return self.nombre

    def get_absolute_url(self):
        """Obtiene la url relacionada con un :class:`Plan`"""

        return reverse('contracts-plan', args=[self.id])


class Beneficio(TimeStampedModel):
    """Permite listar los posibles cobros a efectuar dentro de un :class`Plan`
    de :class:`contrato`"""

    class Meta:
        ordering = ["nombre"]

    plan = models.ForeignKey(Plan, related_name='beneficios')
    nombre = models.CharField(max_length=255, null=True, blank=True)
    descuento = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    observacion = models.CharField(max_length=255, null=True, blank=True)
    activo = models.BooleanField(default=True)
    tipo_items = models.ForeignKey(ItemType, related_name='beneficios',
                                   null=True, blank=True)
    limite = models.IntegerField(default=0, verbose_name=u'Límite de Eventos')
    descuento_post_limite = models.DecimalField(max_digits=10, decimal_places=2,
                                                default=0)
    aplicar_a_suspendidos = models.BooleanField(default=False)

    def __unicode__(self):
        return u"{0} de plan {1}".format(self.nombre, self.plan.nombre)

    def get_absolute_url(self):
        return self.plan.get_absolute_url()


class PCD(TimeStampedModel):
    persona = models.ForeignKey(Persona, related_name="pcds")
    numero = models.CharField(max_length=255, unique=True)
    pc = models.IntegerField(default=0)

    def __unicode__(self):
        return u'{0} {1}'.format(self.persona.nombre_completo(), self.numero)

    def get_absolute_url(self):
        return self.persona.get_absolute_url()


def check_line(line, vencimiento):
    file_pcd = line[0]
    file_certificado = int(line[2])
    poliza_f = line[1]
    apellido_f, nombre_f = line[4].split(",")
    nacimiento_f = server_timezone.localize(
        datetime.strptime(line[6], "%m/%d/%Y"))
    sexo_f = line[5]
    identificacion = line[9]
    vencimiento_r = vencimiento

    activo = line[7].upper()

    master = MasterContract.objects.get(poliza=poliza_f)

    if line[8]:
        venc = server_timezone.localize(datetime.strptime(line[8], '%m/%d/%Y'))
        if venc <= vencimiento_r:
            vencimiento_r = venc

    try:
        pcd = PCD.objects.get(numero=file_pcd)

        persona = pcd.persona
        persona.apellido = apellido_f
        persona.nombre = nombre_f
        persona.save()

        contratos = Contrato.objects.filter(persona=persona,
                                            certificado=file_certificado)

        for contrato in contratos.all():
            contrato.vencimiento = vencimiento_r
            contrato.plan = master.plan
            contrato.master = master
            contrato.exclusion = line[10]
            if activo == 'S':
                contrato.suspendido = True
            else:
                contrato.suspendido = False

            contrato.save()

        for beneficiario in Beneficiario.objects.filter(
                persona=persona).all():
            beneficiario.contrato.vencimiento = vencimiento_r
            beneficiario.exclusion = line[10]
            beneficiario.contrato.save()

    except ObjectDoesNotExist:

        persona = Persona(nombre=nombre_f, apellido=apellido_f,
                          sexo=sexo_f, nacimiento=nacimiento_f,
                          identificacion=identificacion)
        persona.save()
        pcd = PCD(persona=persona, numero=file_pcd)
        pcd.save()

        dependiente = int(line[3])

        if dependiente == 0:

            contract = master.create_contract(persona, vencimiento_r,
                                              file_certificado, file_pcd)
            if activo == 'S':
                contract.suspendido = True
            else:
                contract.suspendido = False
            contract.exclusion = line[10]
            contract.save()
        else:
            contract = Contrato.objects.filter(poliza=poliza_f,
                                               certificado=file_certificado).first()

            if contract:
                beneficiario = Beneficiario(persona=persona, contrato=contract)
                beneficiario.exclusion = line[10]
                beneficiario.save()

    except MultipleObjectsReturned:
        pass


class ImportFile(TimeStampedModel):
    archivo = models.FileField(upload_to='contracts/import/%Y/%m/%d')
    processed = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('contracts-archivo', args=[self.id])

    def assign_contracts(self):
        """Creates :class:`Contract`s for existing :class:`Persona`"""
        # if self.processed:
        # return

        archivo = open(self.archivo.path, 'rU')
        data = unicodecsv.reader(archivo)
        vencimiento = self.created + timedelta(days=8)

        # Create a :class:`Contract` for each identificacion on the file
        for line in data:
            check_line(line, vencimiento)

        self.processed = True
        self.save()


class MasterContract(TimeStampedModel):
    vendedor = models.ForeignKey(Vendedor, related_name='master_contracts')
    plan = models.ForeignKey(Plan, related_name='master_contracts')
    aseguradora = models.ForeignKey(Aseguradora,
                                    related_name='master_contracts')
    inicio = models.DateField(default=timezone.now)
    vencimiento = models.DateField(default=timezone.now)
    contratante = models.ForeignKey(Empleador, blank=True, null=True,
                                    related_name='master_contracts')
    poliza = models.CharField(max_length=255, null=True, blank=True)
    adicionales = models.IntegerField(default=0)
    comision = models.IntegerField(default=0)

    processed = models.BooleanField(default=False)
    item = models.ForeignKey(ItemTemplate, null=True, blank=True)

    def __unicode__(self):
        nombre = self.plan.nombre
        if self.contratante:
            nombre += ' ' + self.contratante.nombre
        if self.aseguradora:
            nombre += ' ' + self.aseguradora.nombre
        return nombre

    def get_absolute_url(self):
        """Obtiene la url relacionada con un :class:`MasterContract`"""

        return reverse('contract-master', args=[self.id])

    def create_contract(self, persona, vencimiento, certificiado, numero):

        contract = Contrato(persona=persona, poliza=self.poliza, plan=self.plan,
                            inicio=timezone.now(), vencimiento=vencimiento,
                            certificado=certificiado, numero=numero,
                            vendedor=self.vendedor, empresa=self.contratante,
                            master=self)

        return contract

    def active_contracts(self):

        return Contrato.objects.filter(master=self,
                                       vencimiento__gte=timezone.now().date())

    def active_contracts_count(self):

        return self.active_contracts().count()


class Contrato(TimeStampedModel):
    """Almacena el estado de cada contrato que se ha celebrado"""

    class Meta:
        permissions = (
            ('contrato', 'Permite al usuario gestionar contratos'),
        )

    persona = models.ForeignKey(Persona, related_name='contratos')
    numero = models.CharField(max_length=255, default='', blank=True)
    vendedor = models.ForeignKey(Vendedor, related_name='contratos')
    plan = models.ForeignKey(Plan, related_name='contratos')
    inicio = models.DateField()
    vencimiento = models.DateField()
    ultimo_pago = models.DateTimeField(default=timezone.now)
    administradores = models.ManyToManyField(User, related_name='contratos',
                                             blank=True)
    renovacion = models.DateField(null=True, blank=True)
    cancelado = models.BooleanField(default=False)
    empresa = models.ForeignKey(Empleador, blank=True, null=True,
                                related_name='contratos')
    poliza = models.CharField(max_length=255, default='', blank=True)
    certificado = models.IntegerField(default=0)
    titular = models.IntegerField(default=0)
    master = models.ForeignKey(MasterContract, related_name='contratos',
                               blank=True, null=True, verbose_name="Contrato")
    suspendido = models.BooleanField(default=False)
    exclusion = models.TextField(blank=True)

    def get_absolute_url(self):
        """Obtiene la url relacionada con un :class:`Contrato`"""

        return reverse('contrato', args=[self.id])

    def __unicode__(self):
        return u"Contrato {0} de {1}".format(self.numero,
                                             self.persona.nombre_completo())

    def total_consultas(self):
        """"Obtiene el total de :class:`Consulta` que los usuarios del contrato
        han efectuado"""
        if self.renovacion is None:
            self.renovacion = self.inicio
            self.save()

        consultas = Consulta.objects.filter(persona=self.persona,
                                            created__gte=self.renovacion).count()
        seguimientos = Seguimiento.objects.filter(persona=self.persona,
                                                  created__gte=self.renovacion).count()
        total = seguimientos + consultas

        predicates = [Q(persona=beneficiario.persona) for beneficiario
                      in self.beneficiarios.all()]

        query = reduce(operator.or_, predicates, Q())

        seguimientos = Seguimiento.objects.filter(
            created__gte=self.renovacion).filter(query).count()
        consultas = Consulta.objects.filter(
            created__gte=self.renovacion).filter(query).count()

        return total + seguimientos + consultas

    def total_citas(self):
        """Obtiene el total de :class:`Cita`s de un periodo"""
        total = self.persona.citas.count()

        predicates = [Q(persona=beneficiario.persona) for beneficiario
                      in self.beneficiarios.all()]

        total += Cita.objects.filter(created__gte=self.renovacion).filter(
            reduce(operator.or_, predicates, Q())).count()

        return total

    def total_hospitalizaciones(self):
        total = self.persona.admisiones.filter(ingresado__isnull=False).count()
        total += sum(
            b.persona.admisiones.filter(ingresado__isnull=False).count()
            for b in self.beneficiarios.all())
        return total

    def dias_mora(self):
        """Dias extra que pasaron desde el ultimo pago"""
        pagos = self.pagos.filter(precio=self.plan.precio, ciclo=True).count()
        ahora = timezone.now().date()
        cobertura = self.inicio + timedelta(pagos * 30)
        delta = ahora - cobertura
        dias = delta.days
        if dias < 0:
            dias = 0

        return dias

    def obtener_cobro(self, item):
        for beneficio in self.plan.beneficios.all():
            for type in item.item_type.all():
                if beneficio.tipo_items == type:
                    venta = item.precio_de_venta
                    return venta - venta * beneficio.descuento / Decimal(100)

        return item.precio_de_venta

    def mora(self):
        """Obtiene la cantidad moentaria debida en este :class:`Contrato`"""
        dias = self.dias_mora()
        mora = 0

        if dias >= 1:
            mora = 1

        while dias > 30:
            mora += 1
            dias -= 30

        return mora * self.plan.precio

    def comision(self):

        return self.plan.precio * self.plan.comision

    def activo(self):

        if self.vencimiento <= timezone.now().date():
            return False

        else:
            return True

    def beneficios(self):

        if self.suspendido:
            return Beneficio.objects.filter(plan=self.plan,
                                            aplicar_a_suspendidos=True).all()

        return Beneficio.objects.filter(plan=self.plan).all()


class Beneficiario(TimeStampedModel):
    persona = models.ForeignKey(Persona, related_name='beneficiarios')
    contrato = models.ForeignKey(Contrato, related_name='beneficiarios')
    inscripcion = models.DateTimeField(default=timezone.now)
    activo = models.BooleanField(default=True)
    dependiente = models.IntegerField(default=0)
    exclusion = models.TextField(blank=True)

    def __unicode__(self):
        return self.persona.nombre_completo()

    def get_absolute_url(self):
        """Obtiene la url relacionada con un :class:`Beneficiario`"""

        return reverse('contrato', args=[self.contrato.id])


class TipoPago(TimeStampedModel):
    item = models.ForeignKey(ItemTemplate, related_name='tipos_pago')

    def __unicode__(self):
        return self.item.descripcion


class Pago(TimeStampedModel):
    """Registra los montos y las fechas en las que se efectuaron los pagos
    de un :class:`Contrato`"""
    contrato = models.ForeignKey(Contrato, related_name='pagos')
    tipo_de_pago = models.ForeignKey(TipoPago, related_name='pagos', null=True)
    fecha = models.DateTimeField(default=timezone.now)
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    descripcion = models.TextField(null=True, blank=True)
    facturar = models.BooleanField(default=False)
    ciclo = models.BooleanField(default=False)

    def get_absolute_url(self):
        """Obtiene la url relacionada con un :class:`Pago`"""

        return reverse('contrato', args=[self.contrato.id])


class TipoEvento(TimeStampedModel):
    nombre = models.CharField(max_length=255, null=True, blank=True)
    tipo_items = models.ForeignKey(ItemType, related_name='tipo_eventos',
                                   null=True, blank=True)

    def __unicode__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('contrato-index')


class LimiteEvento(TimeStampedModel):
    """Especifica la cantidad máxima de :class:`Evento` por cada
    :class:`TipoEvento` que son cubiertos por un :class:`Plan`"""
    plan = models.ForeignKey(Plan, related_name='limites')
    tipo_evento = models.ForeignKey(TipoEvento, related_name='limites')
    cantidad = models.IntegerField(default=0)

    def get_absolute_url(self):
        return self.plan.get_absolute_url()

    def __unicode__(self):
        return u"Límite {0} de {1} en plan {2}".format(self.tipo_evento,
                                                       self.cantidad,
                                                       self.plan.nombre)


class Evento(TimeStampedModel):
    """Registra el uso de los beneficios del :class:`Evento`"""
    contrato = models.ForeignKey(Contrato, related_name='eventos')
    tipo = models.ForeignKey(TipoEvento, related_name='eventos')
    fecha = models.DateTimeField(default=timezone.now)
    descripcion = models.TextField(blank=True, null=True)
    adjunto = models.FileField(upload_to='evento/%Y/%m/%d', blank=True,
                               null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def get_absolute_url(self):
        """Obtiene la url relacionada con un :class:`Evento`"""

        return reverse('contrato', args=[self.contrato.id])

    def __unicode__(self):
        return u"Evento {0} de {1} de {2}".format(self.tipo,
                                                  self.contrato.numero,
                                                  self.contrato.persona.nombre_completo())


class Meta(TimeStampedModel):
    fecha = models.DateField(default=timezone.now)
    contratos = models.IntegerField()

    def get_absolute_url(self):
        """Obtiene la url relacionada con una :class:`Meta`"""

        return reverse('contracts-meta', args=[self.id])


class Cancelacion(TimeStampedModel):
    """Registra las condiciones en las cuales se termina un :class:`Contrato`"""
    contrato = models.ForeignKey(Contrato, related_name='cancelaciones')
    fecha = models.DateField(default=timezone.now)
    motivo = models.TextField()
    pago = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def get_absolute_url(self):
        return self.contrato.get_absolute_url()


class MetodoPago(TimeStampedModel):
    nombre = models.CharField(max_length=255)

    def __unicode__(self):
        return self.nombre


class Precontrato(TimeStampedModel):
    persona = models.ForeignKey(Persona, related_name='precontratos')
    metodo_de_pago = models.ForeignKey(MetodoPago, related_name='precontratos',
                                       blank=True, null=True)
    completado = models.BooleanField(default=False)
    de_acuerdo = models.BooleanField(default=True)
    plan = models.ForeignKey(Plan, related_name='precontratos',
                             blank=True, null=True)

    def __unicode__(self):
        return u'Precontrato de {0}'.format(self.persona.nombre_completo())

    def get_absolute_url(self):
        return reverse('precontrato', args=[self.id])


class Prebeneficiario(TimeStampedModel):
    precontrato = models.ForeignKey(Precontrato,
                                    related_name='prebeneficiarios')
    persona = models.ForeignKey(Persona, related_name='prebeneficiarios')

    def get_absolute_url(self):
        return self.precontrato.get_absolute_url()


class Autorizacion(TimeStampedModel):
    imagen = models.FileField(upload_to='contracts/autorizaciones/%Y/%m/%d')
    descripcion = models.TextField(blank=True, null=True)
    vigente = models.BooleanField(default=True)

    def __unicode__(self):
        return self.imagen.name


def consolidate_contracts(persona, clone):
    [transfer_object_to_persona(contrato, persona) for contrato in
     clone.contratos.all()]

    [transfer_object_to_persona(beneficiario, persona) for beneficiario in
     clone.beneficiarios.all()]

    [transfer_object_to_persona(pcd, persona) for pcd in clone.pcds.all()]


persona_consolidation_functions.append(consolidate_contracts)
