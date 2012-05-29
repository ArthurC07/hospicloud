# -*- coding: utf-8 -*-
from django import forms
from laboratory.models import Examen, Imagen, Adjunto, Dicom
from persona.models import Persona

class ExamenForm(forms.ModelForm):
    
    class Meta:
        
        model = Examen
    
    fecha = forms.DateTimeField(widget=forms.DateTimeInput(
                                            attrs={'class': 'datetimepicker' },
                                            format='%d/%m/%Y %H:%M'),
                                input_formats=('%d/%m/%Y %H:%M',),
                                required=False)
    
    persona = forms.ModelChoiceField(label="",
                                  queryset=Persona.objects.all(),
                                  widget=forms.HiddenInput(), required=False)

class ImagenForm(forms.ModelForm):
    
    class Meta:
        
        model = Imagen
    
    examen = forms.ModelChoiceField(label="",
                                  queryset=Examen.objects.all(),
                                  widget=forms.HiddenInput())

class AdjuntoForm(forms.ModelForm):
    
    class Meta:
        
        model = Adjunto
    
    examen = forms.ModelChoiceField(label="",
                                  queryset=Examen.objects.all(),
                                  widget=forms.HiddenInput())

class DicomForm(forms.ModelForm):
    
    class Meta:
        
        model = Dicom
        fields = ('descripcion', 'archivo')
    
    examen = forms.ModelChoiceField(label="",
                                  queryset=Examen.objects.all(),
                                  widget=forms.HiddenInput())
    