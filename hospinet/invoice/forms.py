# -*- coding: utf-8 -*-
from invoice.models import Recibo, Producto, Venta
from django.contrib.auth.models import User
from django import forms

class ReciboForm(forms.ModelForm):

    """Genera un formulario para :class:`Recibo`:"""

    class Meta:

        model = Recibo
    
    cajero = forms.ModelChoiceField(label="",
                                  queryset=User.objects.all(),
                                  widget=forms.HiddenInput(), required=False)

class VentaForm(forms.ModelForm):

    """Genera un formulario para :class:`Venta`"""

    class Meta:

        model = Venta
