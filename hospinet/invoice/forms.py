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
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Fieldset
from select2.fields import ModelChoiceField

from invoice.models import Recibo, Venta
from persona.models import Persona
from inventory.forms import FieldSetModelFormMixin
from emergency.models import Emergencia
from spital.models import Admision
from imaging.models import Examen
from inventory.models import ItemTemplate


class ReciboForm(FieldSetModelFormMixin):
    """Genera un formulario para :class:`Recibo`:"""

    class Meta:
        model = Recibo
        exclude = ('nulo', 'cerrado')

    cajero = forms.ModelChoiceField(label="",
                                    queryset=User.objects.all(),
                                    widget=forms.HiddenInput(), required=False)

    cliente = forms.ModelChoiceField(label="",
                                     queryset=Persona.objects.all(),
                                     widget=forms.HiddenInput(), required=False)


class ReciboNewForm(ReciboForm):
    def __init__(self, *args, **kwargs):
        super(ReciboNewForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.html5_required = True
        self.field_names = self.fields.keys()
        self.helper.add_input(Submit('submit', 'Guardar'))
        self.helper.layout = Fieldset(u'Datos del Recibo', *self.field_names)


class VentaForm(FieldSetModelFormMixin):
    """Genera un formulario para :class:`Venta`"""

    class Meta:
        model = Venta
        exclude = ('precio', 'impuesto',)

    recibo = forms.ModelChoiceField(label="",
                                    queryset=Recibo.objects.all(),
                                    widget=forms.HiddenInput(), required=False)
    cargo = ModelChoiceField(name="", model="",
                             queryset=ItemTemplate.objects.filter(
                                 activo=True).order_by('descripcion').all())

    def __init__(self, *args, **kwargs):
        super(VentaForm, self).__init__(*args, **kwargs)
        self.helper.add_input(Submit('submit', 'Agregar'))
        self.helper.layout = Fieldset(u'Agregar un Cargo', *self.field_names)


class PeriodoForm(forms.Form):
    inicio = forms.DateTimeField(widget=forms.DateInput(
        attrs={'class': 'datepicker'}, format='%d/%m/%Y'),
                                 input_formats=('%d/%m/%Y',))

    fin = forms.DateTimeField(widget=forms.DateInput(
        attrs={'class': 'datepicker'}, format='%d/%m/%Y'),
                              input_formats=('%d/%m/%Y',))

    def __init__(self, *args, **kwargs):
        super(PeriodoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.html5_required = True
        self.field_names = self.fields.keys()
        self.helper.add_input(Submit('submit', 'Mostrar'))
        self.helper.form_method = 'get'
        self.helper.layout = Fieldset(u'Por Periodo', *self.field_names)

    def set_legend(self, text):
        self.helper.layout = Fieldset(text, *self.field_names)

    def set_action(self, action):
        self.helper.form_action = action


class EmergenciaFacturarForm(FieldSetModelFormMixin):
    class Meta:
        model = Emergencia
        fields = ('facturada', )

    def __init__(self, *args, **kwargs):
        super(EmergenciaFacturarForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Facturar Emergencia',
                                      *self.field_names)


class AdmisionFacturarForm(FieldSetModelFormMixin):
    class Meta:
        model = Admision
        fields = ('facturada', )

    def __init__(self, *args, **kwargs):
        super(AdmisionFacturarForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Facturar Admisión',
                                      *self.field_names)


class ExamenFacturarForm(FieldSetModelFormMixin):
    class Meta:
        model = Examen
        fields = ('facturado', 'radiologo', 'remitio')

    def __init__(self, *args, **kwargs):
        super(ExamenFacturarForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Facturar Examen',
                                      *self.field_names)


class CorteForm(PeriodoForm):
    usuario = forms.ModelChoiceField(queryset=User.objects.all())

    def __init__(self, *args, **kwargs):
        super(CorteForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Corte de Caja', *self.field_names)


class InventarioForm(PeriodoForm):
    def __init__(self, *args, **kwargs):
        super(InventarioForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Relación entre Ventas e Inventario',
                                      *self.field_names)
