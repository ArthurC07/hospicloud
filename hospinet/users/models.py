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

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone
from userena.models import UserenaBaseProfile, UserenaSignup
from django_extensions.db.models import TimeStampedModel
from tastypie.models import create_api_key
from guardian.shortcuts import assign_perm

from inventory.models import Inventario, ItemTemplate
from persona.models import Persona


class Ciudad(TimeStampedModel):
    nombre = models.CharField(max_length=100)
    correlativo_de_recibo = models.IntegerField(default=0)
    direccion = models.CharField(max_length=255, blank=True)
    telefono = models.CharField(max_length=100, blank=True)
    prefijo_recibo = models.CharField(max_length=100, blank=True)
    limite_de_emision = models.DateTimeField(default=timezone.now)
    inicio_rango = models.CharField(max_length=100, blank=True)
    fin_rango = models.CharField(max_length=100, blank=True)

    def __unicode__(self):

        return self.nombre


class UserProfile(UserenaBaseProfile):
    user = models.OneToOneField(User, related_name="profile",
                                blank=True, null=True)
    inventario = models.ForeignKey(Inventario, related_name='usuarios',
                                   blank=True, null=True)
    honorario = models.ForeignKey(ItemTemplate, related_name='usuarios',
                                  blank=True, null=True)
    persona = models.OneToOneField(Persona, related_name='profile', blank=True,
                                   null=True)
    ciudad = models.ForeignKey(Ciudad, related_name='usuarios', blank=True,
                               null=True)

    def __unicode__(self):
        return self.user.username


User.userena_signup = property(
    lambda u: UserenaSignup.objects.get_or_create(user=u)[0])


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = UserProfile.objects.create(user=instance)
        profile.save()
        assign_perm('change_profile', instance, instance.profile)


post_save.connect(create_user_profile, sender=User)
post_save.connect(create_api_key, sender=User)


class UserAction(TimeStampedModel):
    user = models.ForeignKey(User)
    action = models.TextField()
