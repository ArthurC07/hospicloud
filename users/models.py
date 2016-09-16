# -*- coding: utf-8 -*-
#
# Copyright (C) 2011-2015 Carlos Flores <cafg10@gmail.com>
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

from datetime import timedelta
from decimal import Decimal

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel
from guardian.shortcuts import assign_perm
from userena.models import UserenaBaseProfile

from hospinet.utils import get_current_month_range
from inventory.models import ItemTemplate
from persona.models import Persona


@python_2_unicode_compatible
class Company(TimeStampedModel):
    nombre = models.CharField(max_length=255)
    nombre_comercial = models.CharField(max_length=255, blank=True)
    rtn = models.CharField(max_length=14)
    cai = models.CharField(max_length=255)
    direccion = models.TextField()
    telefono = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    moneda = models.CharField(max_length=20, blank=True)
    chat = models.URLField(blank=True)
    help = models.URLField(blank=True)
    emergencia = models.ForeignKey(ItemTemplate, null=True, blank=True,
                                   related_name='emergencia_company')
    emergencia_extra = models.ForeignKey(ItemTemplate, null=True, blank=True,
                                         related_name='emergencia_extra_company')
    deposito = models.ForeignKey(ItemTemplate, null=True, blank=True,
                                 related_name='deposito_company')
    cambio_monetario = models.DecimalField(max_digits=11, decimal_places=4,
                                           default=0)
    receipt_days = models.IntegerField(default=30)
    sac = models.EmailField(blank=True)
    laboratorios = models.EmailField(blank=True)
    incapacidad_image = models.ImageField(upload_to='logos',blank=True, null=True)

    def __str__(self):
        return self.nombre


@python_2_unicode_compatible
class LegalData(TimeStampedModel):
    """
    Defines some data part of invoicing required by law
    """

    TIPOS = (
        ('R', _('Recibo')),
        ('CD', _('Comprobante de Deduccion')),
        ('NC', _('Nota de Credito')),

    )

    tipo = models.CharField(max_length=2, choices=TIPOS, default='R')
    ciudad_creacion = models.ForeignKey('Ciudad')
    cai = models.CharField(max_length=255, blank=True)
    correlativo = models.IntegerField(default=0)
    inicio = models.CharField(max_length=100, blank=True)
    fin = models.CharField(max_length=100, blank=True)
    prefijo = models.CharField(max_length=100, blank=True)
    limite_de_emision = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '{0} {1} {2}'.format(self.tipo, self.ciudad_creacion.nombre,
                                    self.cai)


@python_2_unicode_compatible
class Ciudad(TimeStampedModel):
    """
    Consolidates all City specific legal information for legal tending of
    :class:`Recibo`, :class:`ComprobanteDeduccion`, :class:`NotaCredito`
    """
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255, blank=True)
    telefono = models.CharField(max_length=100, blank=True)
    tiene_presupuesto_global = models.BooleanField(default=False)
    company = models.ForeignKey(Company, blank=True, null=True)
    recibo = models.OneToOneField(LegalData, blank=True, null=True,
                                  related_name='ciudad_recibo')
    comprobante = models.OneToOneField(LegalData, blank=True, null=True,
                                       related_name='ciudad_comprobante')
    nota_credito = models.OneToOneField(LegalData, blank=True, null=True,
                                        related_name='ciudad_nota_credito')
    correo_laboratorio = models.EmailField(blank=True)

    def __str__(self):
        return self.nombre


@python_2_unicode_compatible
class UserProfile(UserenaBaseProfile):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                related_name="profile", blank=True, null=True)
    inventario = models.ForeignKey('inventory.Inventario', related_name='usuarios',
                                   blank=True, null=True)
    honorario = models.ForeignKey(ItemTemplate, related_name='usuarios',
                                  blank=True, null=True)
    ciudad = models.ForeignKey(Ciudad, related_name='usuarios', blank=True,
                               null=True)
    bsc = models.ForeignKey('bsc.ScoreCard', related_name='usuarios',
                            blank=True, null=True)
    bsc2 = models.ForeignKey('bsc.ScoreCard', related_name='usuarios2',
                             blank=True, null=True)

    def __str__(self):
        return self.user.username

    def get_metas(self):
        if self.bsc is None:
            return []
        bsc = self.bsc

        return self.calculate_bsc(bsc)

    def calculate_bsc(self, bsc):
        fin, inicio = get_current_month_range()
        goal = {}
        total = Decimal()
        goal['metas'] = []
        for meta in bsc.meta_set.filter(activa=True).all():
            datos = {'logro': meta.logro(self.user, inicio, fin),
                     'tipo': meta.get_tipo_meta_display(),
                     'peso': meta.peso,
                     'meta': meta.meta,
                     'tiempo': meta.basado_en_tiempo
                     }

            datos['ponderacion'] = meta.ponderacion(datos['logro'])
            datos['logro_ponderado'] = meta.logro_ponderado(
                datos['ponderacion'])
            total += datos['logro_ponderado']
            goal['metas'].append(datos)
        goal['escalas'] = bsc.get_escala(total)
        goal['extras'] = []
        for extra in bsc.extra_set.all():
            datos = {
                'extra': extra,
                'logro': extra.cantidad(self.user, inicio, fin),
            }
            goal['extras'].append(datos)
        goal['extra'] = bsc.get_extras(self.user, inicio, fin)
        goal['total'] = total
        return goal

    def get_metas2(self):
        if self.bsc2 is None:
            return []
        bsc = self.bsc2

        return self.calculate_bsc(bsc)

    def get_current_month_emergencies(self):

        fin, inicio = get_current_month_range()

        return self.user.emergencias.filter(
            created_range=(inicio, fin)
        ).count()

    def current_month_turns(self):

        fin, inicio = get_current_month_range()

        return self.user.turno_set.filter(inicio__range=(inicio, fin)).all()


@python_2_unicode_compatible
class Turno(TimeStampedModel):
    rango_inicio = timedelta(minutes=20)
    rango_fin = timedelta(minutes=10)

    nombre = models.CharField(max_length=255)
    inicio = models.DateTimeField(default=timezone.now)
    fin = models.DateTimeField(default=timezone.now)
    usuarios = models.ManyToManyField(settings.AUTH_USER_MODEL)
    contabilizable = models.BooleanField(default=False)
    ciudad = models.ForeignKey(Ciudad, null=True, blank=True)

    def __str__(self):
        return self.nombre

    def login_inicio(self):
        return self.inicio - self.rango_inicio

    def login_fin(self):
        return self.fin + self.rango_fin


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = UserProfile.objects.create(user=instance)
        profile.save()
        assign_perm('change_profile', instance, instance.profile)


post_save.connect(create_user_profile, sender=settings.AUTH_USER_MODEL)


class UserAction(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    action = models.TextField()
