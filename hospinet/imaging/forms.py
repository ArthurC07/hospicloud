# -*- coding: utf-8 -*-
from django import forms
from imaging.models import Examen, Imagen, Adjunto, Dicom, Remision
from persona.models import Persona

class ExamenForm(forms.ModelForm):
    
    """Permite mostrar formularios para crear :class:`Examen`es nuevos"""

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
    
    """"Permite mostrar un formulario para agregar una :class:`Imagen`
    a un :class:`Examen`"""

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

class RemisionForm(forms.ModelForm):
    
    """"Permite mostrar los formularios para crear una :class:`Remision`"""

    class Meta:
        
        model = Remision
        exclude = ('efectuado', 'usuario',)
    
    persona = forms.ModelChoiceField(label="",
                                  queryset=Persona.objects.all(),
                                  widget=forms.HiddenInput(), required=False)
