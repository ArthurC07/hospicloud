# -*- coding: utf-8 -*-
from django import forms
from spital.models import Admision
from persona.models import Persona
from django.utils.translation.trans_null import _

class AdmisionForm(forms.ModelForm):
    
    class Meta:
        
        model = Admision
        fields = ('paciente', 'diagnostico', 'doctor', 'tipo_de_habitacion',
                  'arancel', 'pago', 'poliza', 'certificado', 'aseguradora',
                  'deposito', )
    
    paciente = forms.ModelChoiceField(label="",
                                  queryset=Persona.objects.all(),
                                  widget=forms.HiddenInput(), required=False)

class ReporteAnualForm(forms.Form):
    
    anio = forms.IntegerField(label=_(u'Año'))
