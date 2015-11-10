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
from datetime import timedelta
from decimal import Decimal

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.conf import settings
from userena.models import UserenaBaseProfile, UserenaSignup
from django_extensions.db.models import TimeStampedModel

from guardian.shortcuts import assign_perm

from emergency.models import Emergencia
from hospinet.utils import get_current_month_range
from inventory.models import Inventario, ItemTemplate
from persona.models import Persona


@python_2_unicode_compatible
class Company(TimeStampedModel):
    nombre = models.CharField(max_length=255)
    rtn = models.CharField(max_length=14)
    cai = models.CharField(max_length=255)
    direccion = models.TextField()
    telefono = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre


@python_2_unicode_compatible
class Ciudad(TimeStampedModel):
    nombre = models.CharField(max_length=100)
    cai_recibo = models.CharField(max_length=255, blank=True)
    cai_comprobante = models.CharField(max_length=255, blank=True)
    correlativo_de_recibo = models.IntegerField(default=0)
    direccion = models.CharField(max_length=255, blank=True)
    telefono = models.CharField(max_length=100, blank=True)
    prefijo_recibo = models.CharField(max_length=100, blank=True)
    limite_de_emision = models.DateTimeField(default=timezone.now)
    inicio_rango = models.CharField(max_length=100, blank=True)
    fin_rango = models.CharField(max_length=100, blank=True)
    tiene_presupuesto_global = models.BooleanField(default=False)
    company = models.ForeignKey(Company, blank=True, null=True)
    correlativo_de_comprobante = models.IntegerField(default=0)
    prefijo_comprobante = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.nombre


@python_2_unicode_compatible
class UserProfile(UserenaBaseProfile):
    user = models.OneToOneField(User, related_name="profile",
                                blank=True, null=True)
    inventario = models.ForeignKey(Inventario, related_name='usuarios',
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

        return Emergencia.objects.filter(usuario=self.user,
                                         created__range=(inicio, fin)
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


User.userena_signup = property(
    lambda u: UserenaSignup.objects.get_or_create(user=u)[0])


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = UserProfile.objects.create(user=instance)
        profile.save()
        assign_perm('change_profile', instance, instance.profile)


post_save.connect(create_user_profile, sender=User)


class UserAction(TimeStampedModel):
    user = models.ForeignKey(User)
    action = models.TextField()
