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
from django.utils import timezone
from select2.fields import ModelChoiceField

from invoice.models import Recibo, Venta, Pago, TurnoCaja, CierreTurno, TipoPago
from persona.forms import DateTimeWidget, FieldSetModelFormMixinNoButton
from persona.models import Persona
from inventory.forms import FieldSetModelFormMixin
from emergency.models import Emergencia
from spital.models import Admision
from imaging.models import Examen
from inventory.models import ItemTemplate, ItemType
from users.mixins import HiddenUserForm


class PersonaForm(FieldSetModelFormMixinNoButton):
    class Meta:
        model = Persona
        fields = ('nombre', 'apellido')

    def __init__(self, *args, **kwargs):
        super(PersonaForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Datos del Cliente', *self.field_names)
        self.helper.form_id = "persona_form"


class ReciboForm(FieldSetModelFormMixin):
    """Genera un formulario para :class:`Recibo`:"""

    class Meta:
        model = Recibo
        exclude = (
            'nulo', 'cerrado', 'discount', 'radiologo', 'remite', 'ciudad',
            'emision', 'correlativo')

    cajero = forms.ModelChoiceField(label="",
                                    queryset=User.objects.all(),
                                    widget=forms.HiddenInput(), required=False)

    cliente = forms.ModelChoiceField(label="",
                                     queryset=Persona.objects.all(),
                                     widget=forms.HiddenInput(), required=False)

    def __init__(self, *args, **kwargs):
        super(ReciboForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Datos del Recibo', *self.field_names)


class VentaForm(FieldSetModelFormMixin):
    """Genera un formulario para :class:`Venta`"""

    class Meta:
        model = Venta
        fields = ('item', 'cantidad', 'precio', 'descripcion', 'recibo')

    recibo = forms.ModelChoiceField(label="",
                                    queryset=Recibo.objects.all(),
                                    widget=forms.HiddenInput(), required=False)
    item = ModelChoiceField(name="", model="",
                            queryset=ItemTemplate.objects.filter(
                                activo=True).order_by('descripcion').all())

    def __init__(self, *args, **kwargs):
        super(VentaForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Agregar un Cargo', *self.field_names)


class PeriodoForm(forms.Form):
    inicio = forms.DateTimeField(widget=DateTimeWidget)

    fin = forms.DateTimeField(widget=DateTimeWidget)

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
        fields = ('facturada',)

    def __init__(self, *args, **kwargs):
        super(EmergenciaFacturarForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Facturar Emergencia',
                                      *self.field_names)


class AdmisionFacturarForm(FieldSetModelFormMixin):
    class Meta:
        model = Admision
        fields = ('facturada',)

    def __init__(self, *args, **kwargs):
        super(AdmisionFacturarForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Facturar Admisión',
                                      *self.field_names)


class ExamenFacturarForm(FieldSetModelFormMixin):
    class Meta:
        model = Examen
        fields = ('facturado', 'radiologo', 'tecnico', 'remitio')

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


class PagoForm(FieldSetModelFormMixin):
    class Meta:
        model = Pago
        exclude = ('status',)

    recibo = forms.ModelChoiceField(label="",
                                    queryset=Recibo.objects.all(),
                                    widget=forms.HiddenInput(), required=False)

    def __init__(self, *args, **kwargs):
        super(PagoForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Agregar un método de Pago',
                                      *self.field_names)


class TurnoCajaForm(HiddenUserForm):
    class Meta:
        model = TurnoCaja
        exclude = ('finalizado', 'fin')

    inicio = forms.DateTimeField(widget=DateTimeWidget(), required=False,
                                 initial=timezone.now)

    def __init__(self, *args, **kwargs):
        super(TurnoCajaForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Iniciar un Turno', *self.field_names)


class CierreTurnoForm(FieldSetModelFormMixin):
    class Meta:
        model = CierreTurno
        fields = '__all__'

    turno = forms.ModelChoiceField(label="",
                                   queryset=TurnoCaja.objects.all(),
                                   widget=forms.HiddenInput(), required=False)

    def __init__(self, *args, **kwargs):
        super(CierreTurnoForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Agregar cierre de Turno',
                                      *self.field_names)


class TurnoCajaCierreForm(FieldSetModelFormMixin):
    class Meta:
        model = TurnoCaja
        fields = ()

    id = forms.ModelChoiceField(label="",
                                queryset=TurnoCaja.objects.all(),
                                widget=forms.HiddenInput(), required=False)

    def __init__(self, *args, **kwargs):
        super(TurnoCajaCierreForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Cerrar Turno',
                                      *self.field_names)


class VentaPeriodoForm(PeriodoForm):
    item = ModelChoiceField(name="", model="",
                            queryset=ItemTemplate.objects.filter(
                                activo=True).order_by('descripcion').all())

    def __init__(self, *args, **kwargs):
        super(VentaPeriodoForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Detalle de Ventas de un Periodo',
                                      *self.field_names)


class TipoPagoPeriodoForm(PeriodoForm):
    tipo = ModelChoiceField(name="", model="", queryset=TipoPago.objects.all())

    def __init__(self, *args, **kwargs):
        super(TipoPagoPeriodoForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Pagos por Tipo y Periodo',
                                      *self.field_names)


class PeriodoAreaForm(PeriodoForm):
    area = ModelChoiceField(name="", model="",
                            queryset=ItemType.objects.all())


class PagoStatusForm(FieldSetModelFormMixin):
    class Meta:
        model = Pago
        fields = ('status',)

    def __init__(self, *args, **kwargs):
        super(PagoStatusForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Cambiar Estado de Pago',
                                      *self.field_names)
