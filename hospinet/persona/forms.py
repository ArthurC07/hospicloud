# -*- coding: utf-8 -*-
from persona.models import (Persona, Fisico, EstiloVida, Antecedente,
    AntecedenteFamiliar, AntecedenteObstetrico, AntecedenteQuirurgico)
from django import forms

class DateTimeWidget(forms.DateTimeInput):
    
    """Permite mostrar un input preparado para fecha y hora utilizando
    JQuery UI DateTimePicker"""

    class Media:
        js = ('js/jquery-ui-timepicker.js',)

    def __init__(self, attrs=None):
        super(DateTimeWidget, self).__init__(attrs)
        if attrs is not None:
            self.attrs = attrs.copy()
        else:
            self.attrs = {'class': 'datetimepicker'}

        if not 'format' in self.attrs:
            self.attrs['format'] = '%d/%m/%Y %H:%M'

class PersonaForm(forms.ModelForm):
    
    """Permite mostrar una interfaz para capturar los datos de una
    :class:`Persona`"""
    
    class Meta:
        
        model = Persona
    
    nacimiento = forms.DateTimeField(widget=forms.DateInput(
                    attrs={'class': 'datepicker' }, format='%d/%m/%Y'),
                 input_formats=('%d/%m/%Y',))
    
    def clean(self):
        
        """Realiza la validación de la identidad que fue ingresada luego de
        limpiar los datos de modo que sean seguros para la base de datos"""
        
        super(PersonaForm, self).clean()
        cleaned_data = self.cleaned_data
        tipo_identidad = cleaned_data.get('tipo_identificacion')
        iden = cleaned_data.get('identificacion')
        if tipo_identidad == 'T' and not Persona.validar_identidad(iden):
            raise forms.ValidationError('La identidad ingresada no es valida')
        
        return cleaned_data

class BasePersonaForm(forms.ModelForm):
    
    """Permite editar la información que depende de una :class:`Persona`"""

    persona = forms.ModelChoiceField(label="",
                                  queryset=Persona.objects.all(),
                                  widget=forms.HiddenInput())

class FisicoForm(BasePersonaForm):
    
    """Permite editar :class:`Fisico`"""

    class Meta:
        
        model = Fisico

class EstiloVidaForm(BasePersonaForm):
    
    """Permite editar :class:`EstiloVida`"""
    
    class Meta:
        
        model = EstiloVida

class AntecedenteForm(BasePersonaForm):
    
    """Permite editar :class:`Antecedente`"""
    
    class Meta:
        
        model = Antecedente

class AntecedenteFamiliarForm(BasePersonaForm):
    
    """Permite editar :class:`AntecedenteFamiliar`"""
    
    class Meta:
        
        model = AntecedenteFamiliar

class AntecedenteObstetricoForm(BasePersonaForm):
    
    """Permite editar :class:`AntecedenteObstetrico`"""
    
    class Meta:
        
        model = AntecedenteObstetrico

class AntecedenteQuirurgicoForm(BasePersonaForm):
    
    """Permite editar :class:`AntecedenteQuirurgico`"""
    
    class Meta:
        
        model = AntecedenteQuirurgico
