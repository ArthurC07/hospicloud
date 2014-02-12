#!/usr/bin/env python
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
from crispy_forms.layout import Fieldset
from django import forms
from contracts.models import Plan, Contrato, TipoEvento, Evento, Pago
from persona.forms import FieldSetModelFormMixin


class PlanForm(FieldSetModelFormMixin):
    class Meta:
        model = Plan

    def __init__(self, *args, **kwargs):
        super(PlanForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Formulario de Plan', *self.field_names)


class ContratoForm(FieldSetModelFormMixin):
    class Meta:
        model = Contrato

    def __init__(self, *args, **kwargs):
        super(ContratoForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Formulario de Contrato', *self.field_names)


class TipoEventoForm(FieldSetModelFormMixin):
    class Meta:
        model = TipoEvento

    def __init__(self, *args, **kwargs):
        super(TipoEventoForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Formulario de Tipo de Evento',
                                      *self.field_names)


class ContratoMixin(FieldSetModelFormMixin):

    admision = forms.ModelChoiceField(label="",
                                      queryset=Contrato.objects.all(),
                                      widget=forms.HiddenInput(),
                                      required=False)


class EventoForm(ContratoMixin):
    class Meta:
        model = Evento

    def __init__(self, *args, **kwargs):
        super(ContratoForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Formulario de Evento',
                                      *self.field_names)


class PagoForm(ContratoMixin):
    class Meta:
        model = Pago

    def __init__(self, *args, **kwargs):
        super(ContratoForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Formulario de Registro de Pago',
                                      *self.field_names)
