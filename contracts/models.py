# -*- coding: utf-8 -*-
#
# Copyright (C) 2011-2016 Carlos Flores <cafg10@gmail.com>
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
from __future__ import unicode_literals

from datetime import timedelta, datetime, time
from decimal import Decimal

import unicodecsv
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.files.storage import default_storage as storage
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import F, Max
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible, smart_text
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel

from hospinet.utils import make_end_day
from hospinet.utils.date import get_current_month_range
from inventory.models import ItemTemplate, ItemType
from persona.models import Persona, Empleador, transfer_object_to_persona, \
    persona_consolidation_functions

server_timezone = timezone.get_current_timezone()


@python_2_unicode_compatible
class Vendedor(TimeStampedModel):
    """Indica quien realizo una venta de un :clas:`Contrato`"""
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL,
                                related_name="vendedores")
    habilitado = models.BooleanField(default=True)

    def __str__(self):
        return self.usuario.get_full_name()

    def get_contratos_vendidos(self, fecha, fin):
        return Contrato.objects.filter(inicio__gte=fecha, cancelado=False,
                                       inicio__lte=fin, vendedor=self)

    def get_absolute_url(self):
        """Obtiene la url relacionada con un :class:`Vendedor`"""

        return reverse('contracts-vendedor', args=[self.id])

    def get_contratos_mes(self):
        fin, inicio = get_current_month_range()
        return self.get_contratos_vendidos(inicio, fin).count()


@python_2_unicode_compatible
class Aseguradora(TimeStampedModel):
    """
    Contains the data for each insurance company the organization has
    :class:`Contrato` with
    """
    nombre = models.CharField(max_length=255, blank=True)
    cardex = models.ForeignKey(Persona, null=True, blank=True,
                               related_name='cardex',
                               verbose_name=_('Representante'))

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('aseguradora', args=[self.id])

    def master_contracts(self):
        return self.mastercontract_set.order_by('contratante__nombre')


@python_2_unicode_compatible
class Plan(TimeStampedModel):
    """Indica los limites que presenta cada :class:`Contrato`"""

    nombre = models.CharField(max_length=255, null=True, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    edad_maxima = models.IntegerField()
    consulta = models.ForeignKey(ItemTemplate, null=True, blank=True,
                                 related_name='plan')
    item = models.ForeignKey(ItemTemplate, null=True, blank=True,
                             related_name='planes_precio')

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        """Obtiene la url relacionada con un :class:`Plan`"""

        return reverse('contracts-plan', args=[self.id])


@python_2_unicode_compatible
class Beneficio(TimeStampedModel):
    """
    Permite listar los posibles cobros a efectuar dentro de un :class`Plan`
    de :class:`Contrato`
    """

    class Meta:
        ordering = ["nombre"]

    plan = models.ForeignKey(Plan, related_name='beneficios')
    nombre = models.CharField(max_length=255, null=True, blank=True)
    descuento = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    observacion = models.CharField(max_length=255, null=True, blank=True)
    activo = models.BooleanField(default=True)
    tipo_items = models.ForeignKey(ItemType, related_name='beneficios',
                                   null=True, blank=True)
    limite = models.IntegerField(default=0,
                                 verbose_name=_('Límite de Eventos'))
    descuento_post_limite = models.DecimalField(max_digits=10, decimal_places=2,
                                                default=0)
    aplicar_a_suspendidos = models.BooleanField(default=False)

    def __str__(self):
        return "{0} de plan {1}".format(self.nombre, self.plan.nombre)

    def get_absolute_url(self):
        return self.plan.get_absolute_url()


@python_2_unicode_compatible
class PCD(TimeStampedModel):
    persona = models.ForeignKey(Persona, related_name="pcds")
    numero = models.CharField(max_length=255, unique=True)
    pc = models.IntegerField(default=0)

    def __str__(self):
        return _('{0} {1}').format(self.persona.nombre_completo(), self.numero)

    def get_absolute_url(self):
        return self.persona.get_absolute_url()


def check_line(line, vencimiento, master_dict):
    """
    Reads one list and according to its positional contents it will act
    accordingly:

    If there exists a :class:`PCD` instance matching its contents it will update
    the :class:`Contrato` associated to the :class:`PCD` instance.

    If there is not a matching :class:`PCD` it will start creating a
    :class:`Persona`, :class:`Contrato and :class:`PCD` that reflect the
    contents of the list.

    :param line:        The list that will be read its content can be described
                        this way:
                        0. PCD
                        1. Policy
                        2. Certificate
                        3. Dependant
                        4. Full name
                        5. Sex
                        6. Birthday
                        7. Active Status Flag
                        8. Contract ending date
                        9. Identification
                        10. Exclusion
    :param vencimiento: The end date of the contract to be updated
    :return:
    """
    file_pcd = smart_text(line[0])
    file_certificado = smart_text(line[2])
    poliza_f = smart_text(line[1])
    apellido_f, nombre_f = smart_text(line[4]).split(",")
    apellido_f = apellido_f.lstrip().rstrip()
    nombre_f = nombre_f.lstrip().rstrip()
    nacimiento_f = server_timezone.localize(
        datetime.strptime(line[6], "%m/%d/%Y"))
    sexo_f = smart_text(line[5])
    identificacion = smart_text(line[9])
    vencimiento_r = vencimiento
    exclusion = smart_text(line[10])
    dependiente = int(line[3])
    activo = smart_text(line[7]).upper()

    master = master_dict[poliza_f]
    suspendido = True if activo == 'S' else False

    vencimiento_r = make_end_day(datetime.strptime(line[8], '%m/%d/%Y'))

    try:
        pcd = PCD.objects.prefetch_related(
            'persona',
            'persona__beneficiarios',
            'persona__contratos',
        ).get(numero=file_pcd)

        persona = pcd.persona

        contratos = persona.contratos.filter(certificado=file_certificado)

        contratos.update(
            suspendido=suspendido,
            exclusion=exclusion,
            master=master,
            plan=master.plan,
            vencimiento=vencimiento_r
        )

        persona.beneficiarios.filter(
            persona__contratos__certificado=file_certificado
        ).update(
            exclusion=exclusion,
        )

    except ObjectDoesNotExist:

        persona = Persona(nombre=nombre_f, apellido=apellido_f,
                          sexo=sexo_f, nacimiento=nacimiento_f,
                          identificacion=identificacion)
        persona.save()
        pcd = PCD(persona=persona, numero=file_pcd)
        pcd.save()

        if dependiente == 0:

            contract = master.create_contract(
                persona,
                vencimiento_r,
                file_certificado,
                file_pcd
            )
            contract.suspendido = suspendido
            contract.exclusion = exclusion
            contract.save()
        else:
            contract = Contrato.objects.filter(
                poliza=poliza_f,
                certificado=file_certificado
            ).first()

            if contract:
                beneficiario = Beneficiario(persona=persona, contrato=contract)
                beneficiario.exclusion = exclusion
                beneficiario.save()

    except MultipleObjectsReturned:
        pass


def update_contract(activo, contrato, exclusion, master, vencimiento):
    """
    Updates a contract to reflect the data passed as its arguments
    :param activo: Active status flag
    :param contrato: :class:`Contrato` that will be updated
    :param exclusion: The exclusions to be stored in the contract
    :param master: The :class:`MasterContract` instance that will be associated
    :param vencimiento: the ending date of the :class:`Contrato`
    :return: the newly updated :class:`Contrato` object
    """
    contrato.vencimiento = vencimiento
    contrato.plan = master.plan
    contrato.master = master
    contrato.exclusion = exclusion
    if activo == 'S':
        contrato.suspendido = True
    else:
        contrato.suspendido = False
    contrato.save()


class ImportFile(TimeStampedModel):
    archivo = models.FileField(upload_to='contracts/import/%Y/%m/%d')
    processed = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('contracts-archivo', args=[self.id])

    def assign_contracts(self):
        """Creates :class:`Contract`s for existing :class:`Persona`"""

        archivo = storage.open(self.archivo.name, 'rU')
        data = unicodecsv.reader(archivo)
        vencimiento = make_end_day(self.created) + timedelta(days=8)
        masters = MasterContract.objects.select_related(
            'plan',
            'contratante',
            'aseguradora'
        ).all()
        master_dict = {master.poliza: master for master in masters}

        # Create a :class:`Contract` for each identificacion on the file
        for line in data:
            check_line(line, vencimiento, master_dict)

        self.processed = True
        self.save()


@python_2_unicode_compatible
class MasterContract(TimeStampedModel):
    vendedor = models.ForeignKey(Vendedor, related_name='master_contracts')
    plan = models.ForeignKey(Plan, related_name='master_contracts')
    aseguradora = models.ForeignKey(Aseguradora)
    administrador = models.ForeignKey(Persona, null=True, blank=True)
    inicio = models.DateField(default=timezone.now)
    contratante = models.ForeignKey(Empleador, blank=True, null=True,
                                    related_name='master_contracts')
    poliza = models.CharField(max_length=255, null=True, blank=True)
    adicionales = models.IntegerField(default=0)
    comision = models.IntegerField(default=0)
    processed = models.BooleanField(default=False)
    gastos_medicos = models.DecimalField(max_digits=11, decimal_places=2,
                                         null=True, blank=True)
    porcentaje = models.DecimalField(max_digits=3, decimal_places=2,
                                     null=True, blank=True)
    ultimo_certificado = models.IntegerField(default=0)
    facturar_al_administrador = models.BooleanField(default=False)
    privado = models.BooleanField(default=False)

    class Meta:
        ordering = ['contratante__nombre']

    def __str__(self):
        nombre = _('Poliza {0} {1}').format(self.poliza, self.plan.nombre)
        if self.contratante:
            nombre += ' - ' + self.contratante.nombre
        if self.aseguradora:
            nombre += ' - ' + self.aseguradora.nombre
        return nombre

    def get_absolute_url(self):
        """Obtiene la url relacionada con un :class:`MasterContract`"""

        return reverse('contract-master', args=[self.id])

    def create_contract(self, persona, vencimiento, certificado, numero,
                        auto=False):
        """
        Allows the creation of :class:`Contrato` by using the data from
        :class:`MasterContract` as building blocks to create it.

        :param persona:
        :param vencimiento:
        :param certificado:
        :param numero:
        :param auto:
        :return:
        """

        if auto and certificado == 0:
            ultimo_certificado = self.contratos.aggregate(
                Max('certificado')
            )['certificado__max']
            if self.ultimo_certificado >= ultimo_certificado:
                self.ultimo_certificado = F('ultimo_certificado') + 1
            else:
                self.ultimo_certificado = ultimo_certificado + 1

            self.save()
            self.refresh_from_db()

            certificado = self.ultimo_certificado
            numero = self.ultimo_certificado

        contract = Contrato(persona=persona, poliza=self.poliza, plan=self.plan,
                            inicio=timezone.now(), vencimiento=vencimiento,
                            certificado=certificado, numero=numero,
                            vendedor=self.vendedor, empresa=self.contratante,
                            master=self)

        if auto:
            dependiente = Contrato.objects.filter(
                certificado=certificado,
                poliza=self.poliza
            ).count()

            pcd = PCD()
            pcd.persona = persona
            if dependiente > 0:
                dependiente += 1
            pcd.numero = '{0}{1:0>6}{2:0>2}'.format(self.poliza,
                                                    contract.certificado,
                                                    dependiente)
            pcd.save()
            contract.numero = pcd.numero
            contract.save()

        return contract

    def active_contracts(self):
        """
        Creates a :class:`QuerySet` that contains all active :class:`Contrato`s
        created with this :class:`MasterContract`
        :return:
        """
        vencimiento = timezone.now()

        return Contrato.objects.filter(
            master=self,
            vencimiento__gte=vencimiento
        ).all()

    def active_contracts_count(self):

        return self.active_contracts().count()

    def comision_administrativa(self):

        return (self.gastos_medicos * self.porcentaje).quantize(Decimal("0.01"))


@python_2_unicode_compatible
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
    vencimiento = models.DateTimeField()
    ultimo_pago = models.DateTimeField(default=timezone.now)
    administradores = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                             related_name='contratos',
                                             blank=True)
    renovacion = models.DateField(null=True, blank=True)
    cancelado = models.BooleanField(default=False)
    empresa = models.ForeignKey(Empleador, blank=True, null=True,
                                related_name='contratos')
    poliza = models.CharField(max_length=255, default='', blank=True)
    certificado = models.CharField(blank=True, max_length=255)
    titular = models.IntegerField(default=0)
    master = models.ForeignKey(MasterContract, related_name='contratos',
                               blank=True, null=True, verbose_name="Contrato")
    suspendido = models.BooleanField(default=False)
    exclusion = models.TextField(blank=True)

    def get_absolute_url(self):
        """Obtiene la url relacionada con un :class:`Contrato`"""

        return reverse('contrato', args=[self.id])

    def __str__(self):
        return _("Contrato {0} de {1}").format(self.numero,
                                               self.persona.nombre_completo())

    def total_hospitalizaciones(self):
        total = self.persona.admisiones.filter(ingresado__isnull=False).count()
        total += sum(
            b.persona.admisiones.filter(ingresado__isnull=False).count()
            for b in self.beneficiarios.all())
        return total

    def dias_mora(self):
        """Dias extra que pasaron desde el ultimo pago"""
        pagos = self.pagos.filter(precio=self.plan.precio, ciclo=True).count()
        ahora = timezone.now()
        cobertura = timezone.make_aware(
            datetime.combine(self.inicio, time.min)
        ) + timedelta(pagos * 30)
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

        if self.vencimiento <= timezone.now():
            return False

        else:
            return True

    def beneficios(self):

        if self.suspendido:
            return Beneficio.objects.filter(plan=self.plan,
                                            aplicar_a_suspendidos=True).all()

        return Beneficio.objects.filter(plan=self.plan).all()


@python_2_unicode_compatible
class Beneficiario(TimeStampedModel):
    persona = models.ForeignKey(Persona, related_name='beneficiarios')
    contrato = models.ForeignKey(Contrato, related_name='beneficiarios')
    inscripcion = models.DateTimeField(default=timezone.now)
    activo = models.BooleanField(default=True)
    dependiente = models.IntegerField(default=0)
    exclusion = models.TextField(blank=True)

    def __str__(self):
        return self.persona.nombre_completo()

    def get_absolute_url(self):
        """Obtiene la url relacionada con un :class:`Beneficiario`"""

        return reverse('contrato', args=[self.contrato.id])


@python_2_unicode_compatible
class TipoPago(TimeStampedModel):
    item = models.ForeignKey(ItemTemplate, related_name='tipos_pago')

    def __str__(self):
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


@python_2_unicode_compatible
class TipoEvento(TimeStampedModel):
    nombre = models.CharField(max_length=255, null=True, blank=True)
    tipo_items = models.ForeignKey(ItemType, related_name='tipo_eventos',
                                   null=True, blank=True)

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('contrato-index')


@python_2_unicode_compatible
class LimiteEvento(TimeStampedModel):
    """Especifica la cantidad máxima de :class:`Evento` por cada
    :class:`TipoEvento` que son cubiertos por un :class:`Plan`"""
    plan = models.ForeignKey(Plan, related_name='limites')
    tipo_evento = models.ForeignKey(TipoEvento, related_name='limites')
    cantidad = models.IntegerField(default=0)

    def get_absolute_url(self):
        return self.plan.get_absolute_url()

    def __str__(self):
        return _("Límite {0} de {1} en plan {2}").format(self.tipo_evento,
                                                         self.cantidad,
                                                         self.plan.nombre)


@python_2_unicode_compatible
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

    def __str__(self):
        return _("Evento {0} de {1} de {2}").format(
            self.tipo,
            self.contrato.numero,
            self.contrato.persona.nombre_completo()
        )


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


@python_2_unicode_compatible
class MetodoPago(TimeStampedModel):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre


@python_2_unicode_compatible
class Precontrato(TimeStampedModel):
    persona = models.ForeignKey(Persona, related_name='precontratos')
    metodo_de_pago = models.ForeignKey(MetodoPago, related_name='precontratos',
                                       blank=True, null=True)
    completado = models.BooleanField(default=False)
    de_acuerdo = models.BooleanField(default=True)
    plan = models.ForeignKey(Plan, related_name='precontratos',
                             blank=True, null=True)

    def __str__(self):
        return _('Precontrato de {0}').format(self.persona.nombre_completo())

    def get_absolute_url(self):
        return reverse('precontrato', args=[self.id])


class Prebeneficiario(TimeStampedModel):
    precontrato = models.ForeignKey(Precontrato,
                                    related_name='prebeneficiarios')
    persona = models.ForeignKey(Persona, related_name='prebeneficiarios')

    def get_absolute_url(self):
        return self.precontrato.get_absolute_url()


@python_2_unicode_compatible
class Autorizacion(TimeStampedModel):
    imagen = models.FileField(upload_to='contracts/autorizaciones/%Y/%m/%d')
    descripcion = models.TextField(blank=True, null=True)
    vigente = models.BooleanField(default=True)

    def __str__(self):
        return self.imagen.name


def consolidate_contracts(persona, clone):
    [transfer_object_to_persona(contrato, persona) for contrato in
     clone.contratos.all()]

    [transfer_object_to_persona(beneficiario, persona) for beneficiario in
     clone.beneficiarios.all()]

    [transfer_object_to_persona(pcd, persona) for pcd in clone.pcds.all()]


persona_consolidation_functions.append(consolidate_contracts)
