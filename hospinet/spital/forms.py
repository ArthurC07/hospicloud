# -*- coding: utf-8 -*-
from django import forms
from spital.models import Admision, Habitacion
from persona.models import Persona
from django.utils.translation.trans_null import _

class AdmisionForm(forms.ModelForm):
    
    """Permite ingresar una :class:`Admision` al Hospital"""

    class Meta:
        
        model = Admision
        fields = ('paciente', 'diagnostico', 'doctor', 'tipo_de_habitacion',
                  'arancel', 'pago', 'poliza', 'certificado', 'aseguradora',
                  'deposito', 'tipo_de_ingreso',)
    
    paciente = forms.ModelChoiceField(label="",
                                  queryset=Persona.objects.all(),
                                  widget=forms.HiddenInput(), required=False)

class HabitacionForm(forms.ModelForm):

    """Permite gestionar los datos de una :class:`Habitacion`"""

    class Meta:

        model = Habitacion
