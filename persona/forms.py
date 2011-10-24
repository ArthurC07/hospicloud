# -*- coding: utf-8 -*-
from persona.models import Persona, Fisico, EstiloVida
from django import forms

class PersonaForm(forms.ModelForm):
    
    class Meta:
        
        model = Persona
    
    nacimiento = forms.DateTimeField(widget=forms.DateInput(
                    attrs={'class': 'datepicker' }, format='%d/%m/%Y'),
                 input_formats=('%d/%m/%Y',))
    
    def clean(self):
        
        cleaned_data = self.cleaned_data
        tipo_identidad = cleaned_data.get('tipo_identificacion')
        iden = cleaned_data.get('identificacion')
        if tipo_identidad == 'T' and not Persona.validar_identidad(iden):
            raise forms.ValidationError('La identidad ingresada no es valida')
        
        return cleaned_data

class FisicoForm(forms.ModelForm):
    
    class Meta:
        
        model = Fisico

class EstiloVidaForm(forms.ModelForm):
    
    class Meta:
        
        model = EstiloVida
