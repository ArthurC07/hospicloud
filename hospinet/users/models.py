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
from userena.models import UserenaBaseProfile
from django_extensions.db.models import TimeStampedModel

from inventory.models import Inventario, ItemTemplate


class UserProfile(UserenaBaseProfile):
    user = models.OneToOneField(User, primary_key=True)
    inventario = models.ForeignKey(Inventario, related_name='usuarios',
                                   blank=True, null=True)
    honorario = models.ForeignKey(ItemTemplate, related_name='usuarios',
                                  blank=True, null=True)

    def __unicode__(self):
        return self.user.username


User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        from guardian.shortcuts import assign_perm

        assign_perm('change_profile', instance, instance.get_profile())


post_save.connect(create_user_profile, sender=User)


class UserAction(TimeStampedModel):
    user = models.ForeignKey(User)
    action = models.TextField()


class Hospital(models.Model):
    nombre = models.CharField(max_length=200)
