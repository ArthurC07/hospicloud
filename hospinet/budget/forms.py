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
from crispy_forms.layout import Fieldset
from django import forms
from select2.fields import ModelChoiceField

from budget.models import Presupuesto, Cuenta, Gasto
from persona.forms import FieldSetModelFormMixin
from users.forms import CiudadFormMixin


class PresupuestoForm(CiudadFormMixin):
    class Meta:
        model = Presupuesto
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(PresupuestoForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Formulario de Presupuesto',
                                      *self.field_names)


class PresupuestoFormMixin(FieldSetModelFormMixin):
    presupuesto = ModelChoiceField(queryset=Presupuesto.objects.all(), name="",
                                   model="", widget=forms.HiddenInput())


class CuentaForm(PresupuestoFormMixin):
    class Meta:
        model = Cuenta
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CuentaForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Formulario de Cuenta',
                                      *self.field_names)


class CuentaFormMixin(FieldSetModelFormMixin):
    cuenta = ModelChoiceField(queryset=Cuenta.objects.all(), name="",
                              model="", widget=forms.HiddenInput())


class GastoForm(CuentaFormMixin):
    class Meta:
        model = Gasto
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(GastoForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Formulario de Gasto', *self.field_names)
