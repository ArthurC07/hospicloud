# -*- coding: utf-8 -*-
#
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
from crispy_forms.layout import Fieldset, Submit
from django import forms
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from hospinet.utils.forms import DateTimeWidget, FieldSetModelFormMixin, \
    FieldSetFormMixin
from income.models import Cheque, DetallePago, Deposito
from invoice.models import Pago
from users.mixins import HiddenUserForm


class ChequeCobroForm(HiddenUserForm):
    """
    Creates the UI and validation required to create :class:`Cheque`s
    """

    class Meta:
        model = Cheque
        exclude = ('aplicado',)

    fecha_de_deposito = forms.DateTimeField(widget=DateTimeWidget(),
                                            required=False,
                                            initial=timezone.now)

    fecha_de_entrega = forms.DateTimeField(widget=DateTimeWidget(),
                                           required=False,
                                           initial=timezone.now)
    fecha_de_emision = forms.DateTimeField(widget=DateTimeWidget(),
                                           required=False,
                                           initial=timezone.now)

    def __init__(self, *args, **kwargs):
        super(ChequeCobroForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(_('Datos del Cheque de Pago'),
                                      *self.field_names)


class DetallePagoForm(FieldSetModelFormMixin):
    class Meta:
        model = DetallePago
        fields = '__all__'

    deposito = forms.ModelChoiceField(label='',
                                      queryset=Deposito.objects.all(),
                                      widget=forms.HiddenInput(),
                                      required=False)
    pago = forms.ModelChoiceField(label='',
                                  queryset=Pago.objects.all(),
                                  widget=forms.HiddenInput(),
                                  required=False)

    def __init__(self, *args, **kwargs):
        super(DetallePagoForm, self).__init__(*args, **kwargs)
        self.fields['deposito'].widget.attrs['readonly'] = True
        self.fields['pago'].widget.attrs['readonly'] = True
        self.helper.layout = Fieldset(_('Registrar Detalle del Pago'),
                                      *self.field_names)