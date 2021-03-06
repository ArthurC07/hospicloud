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
from __future__ import unicode_literals

from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.views.generic.edit import FormMixin

from persona.forms import FieldSetModelFormMixin

try:
    from django.contrib.auth.mixins import LoginRequiredMixin

except ImportError:
    class LoginRequiredMixin(View):
        """Clase base para crear vistas que requieren inicio de sesión"""

        @method_decorator(login_required)
        def dispatch(self, request, *args, **kwargs):
            """
            Permite despachar la petición en caso que el usuario tiniciada
            su sesión en la aplicación
            """

            return super(LoginRequiredMixin, self).dispatch(request, *args,
                                                            **kwargs)


class CurrentUserFormMixin(FormMixin, LoginRequiredMixin):
    def get_initial(self):
        """Agrega la :class:`User` a los campos del formulario"""

        initial = super(CurrentUserFormMixin, self).get_initial()
        initial['usuario'] = self.request.user.id
        return initial


class HiddenUserForm(FieldSetModelFormMixin):
    usuario = forms.ModelChoiceField(queryset=User.objects.all(),
                                     widget=forms.HiddenInput(), required=True)


class UserForm(FieldSetModelFormMixin):
    usuario = forms.ModelChoiceField(queryset=User.objects.all())
