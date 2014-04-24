# !/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2011-2014 Carlos Flores <cafg10@gmail.com>
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

from contracts.models import (Plan, Contrato, TipoEvento, Evento, Pago,
                              Vendedor, Beneficiario, LimiteEvento, Meta,
                              Cancelacion)
from persona.forms import (FieldSetModelFormMixin, DateTimeWidget, DateWidget,
                           FieldSetFormMixin, FieldSetModelFormMixinNoButton,
                           FutureDateWidget)
from persona.models import Persona, Empleador


class PersonaForm(FieldSetModelFormMixinNoButton):
    class Meta:
        model = Persona

    def __init__(self, *args, **kwargs):
        super(PersonaForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Datos del Titular', *self.field_names)


class PlanForm(FieldSetModelFormMixin):
    class Meta:
        model = Plan

    def __init__(self, *args, **kwargs):
        super(PlanForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Formulario de Plan', *self.field_names)


class ContratoForm(FieldSetModelFormMixin):
    class Meta:
        model = Contrato
        exclude = ('cancelado', 'empresa',)

    vencimiento = forms.DateField(widget=FutureDateWidget)
    ultimo_pago = forms.DateTimeField(widget=DateTimeWidget(), required=False,
                                      initial=timezone.now)
    inicio = forms.DateField(widget=FutureDateWidget())

    def __init__(self, *args, **kwargs):
        super(ContratoForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Formulario de Contrato',
                                      *self.field_names)


class ContratoEmpresarialForm(FieldSetModelFormMixin):
    class Meta:
        model = Contrato
        exclude = ('cancelado', )

    vencimiento = forms.DateField(widget=FutureDateWidget)
    ultimo_pago = forms.DateTimeField(widget=DateTimeWidget(), required=False,
                                      initial=timezone.now)
    inicio = forms.DateField(widget=FutureDateWidget())

    def __init__(self, *args, **kwargs):
        super(ContratoEmpresarialForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Formulario de Contrato',
                                      *self.field_names)


class TipoEventoForm(FieldSetModelFormMixin):
    class Meta:
        model = TipoEvento

    def __init__(self, *args, **kwargs):
        super(TipoEventoForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Formulario de Tipo de Evento',
                                      *self.field_names)


class ContratoMixin(FieldSetModelFormMixin):
    contrato = forms.ModelChoiceField(label="",
                                      queryset=Contrato.objects.all(),
                                      widget=forms.HiddenInput(),
                                      required=False)


class EventoForm(ContratoMixin):
    class Meta:
        model = Evento

    def __init__(self, *args, **kwargs):
        super(EventoForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Formulario de Evento',
                                      *self.field_names)


class PagoForm(ContratoMixin):
    class Meta:
        model = Pago

    def __init__(self, *args, **kwargs):
        super(PagoForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Formulario de Registro de Pago',
                                      *self.field_names)


class VendedorForm(FieldSetModelFormMixin):
    class Meta:
        model = Vendedor

    def __init__(self, *args, **kwargs):
        super(VendedorForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Formulario de Vendedor',
                                      *self.field_names)


class VendedorChoiceForm(FieldSetFormMixin):
    vendedor = forms.ModelChoiceField(queryset=Vendedor.objects.all())

    def __init__(self, *args, **kwargs):
        super(VendedorChoiceForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Buscar Vendedor', *self.field_names)
        self.helper.add_input(Submit('submit', u'Buscar'))


class ContratoSearchForm(FieldSetFormMixin):
    numero = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        super(ContratoSearchForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Buscar Contrato', *self.field_names)
        self.helper.add_input(Submit('submit', u'Buscar'))


class BeneficiarioForm(ContratoMixin):
    class Meta:
        model = Beneficiario

    inscripcion = forms.DateTimeField(widget=DateTimeWidget(), required=False,
                                      initial=timezone.now)

    def __init__(self, *args, **kwargs):
        super(BeneficiarioForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Formulario de Registro de Beneficiario',
                                      *self.field_names)


class BeneficiarioPersonaForm(FieldSetModelFormMixin):
    class Meta:
        model = Beneficiario

    contrato = ModelChoiceField(
        queryset=Contrato.objects.all(),
        name="nombre", model="")
    inscripcion = forms.DateTimeField(widget=DateTimeWidget(), required=False,
                                      initial=timezone.now)

    def __init__(self, *args, **kwargs):
        super(BeneficiarioPersonaForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Formulario de Registro de Beneficiario',
                                      *self.field_names)


class PlanFormMixin(FieldSetModelFormMixin):

    plan = forms.ModelChoiceField(label="", queryset=Plan.objects.all(),
                                  widget=forms.HiddenInput(),
                                  required=False)


class LimiteEventoForm(PlanFormMixin):
    class Meta:
        model = LimiteEvento

    def __init__(self, *args, **kwargs):
        super(LimiteEventoForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Agregar Limite de Evento',
                                      *self.field_names)


class PlanChoiceForm(FieldSetFormMixin):
    plan = forms.ModelChoiceField(queryset=Plan.objects.all())

    def __init__(self, *args, **kwargs):
        super(PlanChoiceForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Buscar Contrato por Nombre',
                                      *self.field_names)
        self.helper.add_input(Submit('submit', u'Buscar'))


class EmpleadorChoiceForm(FieldSetFormMixin):
    empresa = forms.ModelChoiceField(queryset=Empleador.objects.all())

    def __init__(self, *args, **kwargs):
        super(EmpleadorChoiceForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Buscar Contratos Empresariales',
                                      *self.field_names)
        self.helper.add_input(Submit('submit', u'Buscar'))


class MetaForm(FieldSetModelFormMixin):
    class Meta:
        model = Meta

    fecha = forms.DateField(widget=FutureDateWidget(), required=False,
                            initial=timezone.now().date())

    def __init__(self, *args, **kwargs):
        super(MetaForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Formulario de Meta', *self.field_names)


class CancelacionForm(ContratoMixin):
    class Meta:
        model = Cancelacion

    fecha = forms.DateField(widget=FutureDateWidget(), required=False,
                            initial=timezone.now().date())

    def __init__(self, *args, **kwargs):
        super(CancelacionForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Cancelar Contrato', *self.field_names)

