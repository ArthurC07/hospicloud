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
from django.utils.translation import ugettext_lazy as _
from budget.models import Presupuesto, Cuenta, Gasto, Fuente
from inventory.forms import ProveedorFormMixin
from invoice.forms import PeriodoForm
from persona.forms import FieldSetModelFormMixin, DateTimeWidget, \
    FieldSetFormMixin
from users.forms import CiudadFormMixin
from users.mixins import HiddenUserForm


class FuenteFormMixin(FieldSetModelFormMixin):
    fuente_de_pago = forms.ModelChoiceField(queryset=Fuente.objects.all())


class PresupuestoForm(CiudadFormMixin):
    class Meta:
        model = Presupuesto
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(PresupuestoForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(_(u'Formulario de Presupuesto'),
                                      *self.field_names)


class PresupuestoFormMixin(FieldSetModelFormMixin):
    presupuesto = forms.ModelChoiceField(queryset=Presupuesto.objects.all(),
                                         widget=forms.HiddenInput())


class CuentaForm(PresupuestoFormMixin):
    class Meta:
        model = Cuenta
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CuentaForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(_(u'Formulario de Cuenta'),
                                      *self.field_names)


class CuentaFormMixin(FieldSetModelFormMixin):
    cuenta = forms.ModelChoiceField(queryset=Cuenta.objects.all(),
                                    label=_(u'Tipo de Gasto'))


class GastoForm(CuentaFormMixin, ProveedorFormMixin, HiddenUserForm):
    class Meta:
        model = Gasto
        exclude = ('ejecutado', 'fecha_maxima_de_pago', 'numero_pagos',
                   'comprobante_de_pago', 'numero_de_comprobante_de_pago',
                   'recepcion_de_facturas_originales',
                   'fecha_de_recepcion_de_factura')

    descripcion = forms.CharField(required=True, widget=forms.Textarea(
        attrs={'rows': 2, 'cols': 40}))
    fecha_de_pago = forms.DateTimeField(widget=DateTimeWidget(),
                                        initial=timezone.now)
    fuente_de_pago = forms.ModelChoiceField(queryset=Fuente.objects.filter(
        caja=True)
    )
    fecha_en_factura = forms.DateTimeField(widget=DateTimeWidget(),
                                           initial=timezone.now)

    def __init__(self, *args, **kwargs):
        super(GastoForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(_(u'Formulario de Gastos'),
                                      *self.field_names)


class GastoPendienteForm(CuentaFormMixin, ProveedorFormMixin, HiddenUserForm):
    class Meta:
        model = Gasto
        exclude = ('ejecutado', 'fecha_de_pago', 'comprobante_de_pago',
                   'recepcion_de_facturas_originales', 'fuente_de_pago',
                   'numero_de_comprobante_de_pago', 'numero_pagos',
                   'fecha_de_recepcion_de_factura',
                   'recepcion_de_facturas_originales')

    descripcion = forms.CharField(required=True, widget=forms.Textarea(
        attrs={'rows': 2, 'cols': 40}))

    fecha_maxima_de_pago = forms.DateTimeField(widget=DateTimeWidget(),
                                               required=False,
                                               initial=timezone.now)
    fecha_en_factura = forms.DateTimeField(widget=DateTimeWidget(),
                                           initial=timezone.now)

    def __init__(self, *args, **kwargs):
        super(GastoPendienteForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(_(u'Formulario de Cuenta por Pagar'),
                                      *self.field_names)


class GastoEjecutarFrom(ProveedorFormMixin, CuentaFormMixin):
    class Meta:
        model = Gasto
        exclude = ('ejecutado', 'fecha_maxima_de_pago', 'comprobante_entregado',
                   'numero_pagos', 'usuario', 'fecha_de_recepcion_de_factura',
                   'recepcion_de_facturas_originales')

    descripcion = forms.CharField(required=True, widget=forms.Textarea(
        attrs={'rows': 2, 'cols': 40}))
    fuente_de_pago = forms.ModelChoiceField(queryset=Fuente.objects.filter(
                                          caja=False)
    )
    fecha_de_pago = forms.DateTimeField(widget=DateTimeWidget(),
                                        initial=timezone.now)
    fecha_en_factura = forms.DateTimeField(widget=DateTimeWidget(),
                                           initial=timezone.now)

    def __init__(self, *args, **kwargs):
        super(GastoEjecutarFrom, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(_(u'Ejecutar un Gasto'),
                                      *self.field_names)


class MontoForm(FieldSetFormMixin):
    monto = forms.DecimalField()

    def __init__(self, *args, **kwargs):
        super(MontoForm, self).__init__(*args, **kwargs)
        self.helper.add_input(Submit('submit', _(u'Guardar')))
        self.helper.layout = Fieldset(_(u'Indicar Monto'), *self.field_names)


class GastoPeriodoCuentaForm(PeriodoForm, FieldSetFormMixin):
    cuenta = forms.ModelChoiceField(queryset=Cuenta.objects.all())

    def __init__(self, *args, **kwargs):
        super(GastoPeriodoCuentaForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(_(u'Gastos Por Periodo y Cuenta'),
                                      *self.field_names)


class GastoPresupuestoPeriodoCuentaForm(PeriodoForm, FieldSetFormMixin):
    presupuesto = forms.ModelChoiceField(queryset=Presupuesto.objects.all())

    def __init__(self, *args, **kwargs):
        super(GastoPresupuestoPeriodoCuentaForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(_(u'Gastos Por Periodo y Presupuesto'),
                                      *self.field_names)
