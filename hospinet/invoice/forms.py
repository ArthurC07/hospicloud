# -*- coding: utf-8 -*-
from invoice.models import Recibo, Producto, Venta
from django.contrib.auth.models import User
from django import forms
from persona.models import Persona

class ReciboForm(forms.ModelForm):

    """Genera un formulario para :class:`Recibo`:"""

    class Meta:

        model = Recibo
    
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
    descripcion = forms.CharField(widget=forms.Textarea(attrs={'class': 'big' }))

class PeriodoForm(forms.Form):

    inicio = forms.DateTimeField(widget=forms.DateInput(
                    attrs={'class': 'datepicker' }, format='%d/%m/%Y'),
                 input_formats=('%d/%m/%Y',))

    fin = forms.DateTimeField(widget=forms.DateInput(
                    attrs={'class': 'datepicker' }, format='%d/%m/%Y'),
                 input_formats=('%d/%m/%Y',))
