# -*- coding: utf-8 -*-
from django import forms
from laboratory.models import Examen, Imagen

class ExamenForm(forms.ModelForm):
    
    class Meta:
        
        model = Examen
    
    fecha = forms.DateTimeField(widget=forms.DateTimeInput(
                                            attrs={'class': 'datetimepicker' },
                                            format='%d/%m/%Y %H:%M'),
                                input_formats=('%d/%m/%Y %H:%M',),
                                required=False)

class ImagenForm(forms.ModelForm):
    
    class Meta:
        
        model = Imagen
