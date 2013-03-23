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

from invoice.models import Recibo, Producto, Venta
from django.contrib.auth.models import User
from django import forms
from persona.models import Persona

class ReciboForm(forms.ModelForm):

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

class VentaForm(forms.ModelForm):

    """Genera un formulario para :class:`Venta`"""

    class Meta:

        model = Venta
        exclude = ('precio', 'impuesto',)
    
    recibo = forms.ModelChoiceField(label="",
                                  queryset=Recibo.objects.all(),
                                  widget=forms.HiddenInput(), required=False)

class PeriodoForm(forms.Form):

    inicio = forms.DateTimeField(widget=forms.DateInput(
                    attrs={'class': 'datepicker' }, format='%d/%m/%Y'),
                 input_formats=('%d/%m/%Y',))

    fin = forms.DateTimeField(widget=forms.DateInput(
                    attrs={'class': 'datepicker' }, format='%d/%m/%Y'),
                 input_formats=('%d/%m/%Y',))
