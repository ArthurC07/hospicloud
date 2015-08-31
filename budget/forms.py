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
from crispy_forms.layout import Fieldset, Submit
from django import forms
from django.utils import timezone
from select2.fields import ModelChoiceField

from budget.models import Presupuesto, Cuenta, Gasto
from inventory.forms import ProveedorFormMixin
from persona.forms import FieldSetModelFormMixin, DateTimeWidget, \
    FieldSetFormMixin
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


class GastoForm(CuentaFormMixin, ProveedorFormMixin):
    class Meta:
        model = Gasto
        exclude = ('ejecutado', 'fecha_maxima_de_pago')

    fecha_de_pago = forms.DateField(widget=DateTimeWidget(),
                                    initial=timezone.now)
    periodo_de_pago = forms.DateField(widget=DateTimeWidget(),
                                      initial=timezone.now)

    def __init__(self, *args, **kwargs):
        super(GastoForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Formulario de Gasto', *self.field_names)


class GastoPendienteForm(CuentaFormMixin, ProveedorFormMixin):
    class Meta:
        model = Gasto
        exclude = ('ejecutado', 'fecha_de_pago', 'periodo_de_pago', 'cheque')

    fecha_maxima_de_pago = forms.DateTimeField(widget=DateTimeWidget(),
                                               required=False,
                                               initial=timezone.now)

    def __init__(self, *args, **kwargs):
        super(GastoPendienteForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Formulario de Cuenta por Pagar',
                                      *self.field_names)


class GastoEjecutarFrom(ProveedorFormMixin, CuentaFormMixin):
    class Meta:
        model = Gasto
        exclude = ('ejecutado', 'fecha_maxima_de_pago',)

    fecha_de_pago = forms.DateTimeField(widget=DateTimeWidget(),
                                        initial=timezone.now)
    periodo_de_pago = forms.DateTimeField(widget=DateTimeWidget(),
                                          initial=timezone.now)

    def __init__(self, *args, **kwargs):
        super(GastoEjecutarFrom, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Ejecutar un Gasto', *self.field_names)


class MontoForm(FieldSetFormMixin):
    monto = forms.DecimalField()

    def __init__(self, *args, **kwargs):
        super(MontoForm, self).__init__(*args, **kwargs)
        self.helper.add_input(Submit('submit', u'Guardar'))
        self.helper.layout = Fieldset(u'Indicar Monto', *self.field_names)