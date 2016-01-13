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
from crispy_forms.layout import Fieldset
from django import forms
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from hospinet.utils.forms import DateTimeWidget, FieldSetModelFormMixin
from income.models import Cheque, DetallePago, Deposito, CierrePOS
from invoice.models import Pago
from persona.models import Persona
from users.mixins import HiddenUserForm


class DepositoForm(HiddenUserForm):
    """
    Defines the UI and validation required to create :class:`Deposito`
    """

    class Meta:
        model = Deposito
        exclude = ('aplicado',)

    fecha_de_deposito = forms.DateTimeField(widget=DateTimeWidget(),
                                            required=False,
                                            initial=timezone.now)

    def __init__(self, *args, **kwargs):
        super(DepositoForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(_('Datos del Dep&oacute;sito'),
                                      *self.field_names)


class ChequeForm(HiddenUserForm):
    """
    Creates the UI and validation required to create :class:`Cheque`s
    """

    class Meta:
        model = Cheque
        exclude = ('aplicado',)

    emisor = forms.ModelChoiceField(
            queryset=Persona.objects.filter(mostrar_en_cardex=True)
    )
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
        super(ChequeForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(_('Datos del Cheque de Pago'),
                                      *self.field_names)


class CierrePOSForm(HiddenUserForm):
    """
    Defines a form that will be used to create and edit :class:`CierrePOS`
    """
    class Meta:
        model = CierrePOS
        exclude = ('aplicado', )

    fecha_de_deposito = forms.DateTimeField(widget=DateTimeWidget(),
                                            required=False,
                                            initial=timezone.now)

    def __init__(self, *args, **kwargs):
        super(CierrePOSForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(_('Datos del Cierre de POS'),
                                      *self.field_names)


class DetallePagoForm(FieldSetModelFormMixin):
    """
    Defines the form that will be used to register :class:`DetallePago`
    """

    class Meta:
        model = DetallePago
        fields = '__all__'

    cheque = forms.ModelChoiceField(label='',
                                    queryset=Cheque.objects.all(),
                                    widget=forms.HiddenInput(),
                                    required=False)
    pago = forms.ModelChoiceField(label='',
                                  queryset=Pago.objects.all(),
                                  widget=forms.HiddenInput(),
                                  required=False)

    def __init__(self, *args, **kwargs):
        super(DetallePagoForm, self).__init__(*args, **kwargs)
        self.fields['cheque'].widget.attrs['readonly'] = True
        self.fields['pago'].widget.attrs['readonly'] = True
        self.helper.layout = Fieldset(_('Registrar Detalle del Pago'),
                                      *self.field_names)
