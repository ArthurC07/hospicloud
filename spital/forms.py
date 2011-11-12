# -*- coding: utf-8 -*-
from django import forms
from spital.models import Admision

class AdmisionForm(forms.ModelForm):
    
    class Meta:
        
        model = Admision
    
    fields = ('diagnostico', 'doctor', 'tipo_de_habitacion',
              'arancel', 'pago', 'poliza', 'certificado', 'aseguradora',
              'deposito', )
