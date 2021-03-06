# -*- coding: utf-8 -*-
# Copyright (C) 2015 Carlos Flores <cafg10@gmail.com>
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

from django.apps import AppConfig
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _


class UsersAppConfig(AppConfig):
    name = 'users'
    verbose_name = _('Perfiles de Usuario')

    def ready(self):
        from userena.models import UserenaSignup
        get_user_model().userena_signup = property(
                lambda u: UserenaSignup.objects.get_or_create(user=u)[0]
        )
