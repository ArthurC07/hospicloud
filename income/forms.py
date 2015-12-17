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
from crispy_forms.layout import Fieldset
from django import forms
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from hospinet.utils.forms import DateTimeWidget
from income.models import Cheque
from invoice.models import CuentaPorCobrar
from users.mixins import HiddenUserForm


class ChequeCobroForm(HiddenUserForm):
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

    cuenta_por_cobrar = forms.ModelChoiceField(
            label="",
            queryset=CuentaPorCobrar.objects.filter(status__pending=True).all(),
            widget=forms.HiddenInput(),
            required=False
    )

    def __init__(self, *args, **kwargs):
        super(ChequeCobroForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(_(u'Datos del Pago'),
                                      *self.field_names)
