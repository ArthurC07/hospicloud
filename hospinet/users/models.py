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
from userena.models import UserenaBaseProfile, UserenaSignup
from django_extensions.db.models import TimeStampedModel
from tastypie.models import create_api_key

from inventory.models import Inventario, ItemTemplate
from persona.models import Persona


class UserProfile(UserenaBaseProfile):
    id = models.OneToOneField(User, db_column='id', primary_key=True)
    user = models.OneToOneField(User, related_name="profile",
                                blank=True, null=True)
    inventario = models.ForeignKey(Inventario, related_name='usuarios',
                                   blank=True, null=True)
    honorario = models.ForeignKey(ItemTemplate, related_name='usuarios',
                                  blank=True, null=True)
    persona = models.OneToOneField(Persona, related_name='profile', blank=True,
                                   null=True)

    def __unicode__(self):
        return self.user.username


User.userena_signup = property(lambda u: UserenaSignup.objects.get_or_create(user=u)[0])


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(id=instance, user=instance)
        from guardian.shortcuts import assign_perm

        assign_perm('change_profile', instance, instance.get_profile())


post_save.connect(create_user_profile, sender=User)
post_save.connect(create_api_key, sender=User)


class UserAction(TimeStampedModel):
    user = models.ForeignKey(User)
    action = models.TextField()
