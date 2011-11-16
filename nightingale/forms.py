# -*- coding: utf-8 -*-
from django import forms
from spital.models import Admision
from nightingale.models import Cargo, Evolucion, Glucometria, Ingesta, Excreta,\
    NotaEnfermeria, OrdenMedica, SignoVital

class IngresarForm(forms.ModelForm):
    
    class Meta:
        
        model = Admision
        fields = ('habitacion',)

class CargoForm(forms.ModelForm):
    
    class Meta:
        
        model = Cargo
    
    fecha_y_hora = forms.DateTimeField(widget=forms.DateTimeInput(
                                            attrs={'class': 'datetimepicker' },
                                            format='%d/%m/%Y %H:%M'),
                                input_formats=('%d/%m/%Y %H:%M',),
                                required=False)
    
    inicio = forms.DateTimeField(widget=forms.DateTimeInput(
                                            attrs={'class': 'datetimepicker' },
                                            format='%d/%m/%Y %H:%M'),
                                input_formats=('%d/%m/%Y %H:%M',),
                                required=False)
    
    fin = forms.DateTimeField(widget=forms.DateTimeInput(
                                            attrs={'class': 'datetimepicker' },
                                            format='%d/%m/%Y %H:%M'),
                                input_formats=('%d/%m/%Y %H:%M',),
                                required=False)
    
    admision = forms.ModelChoiceField(label="",
                                  queryset=Admision.objects.all(),
                                  widget=forms.HiddenInput(), required=False)

class EvolucionForm(forms.ModelForm):
    
    class Meta:
        
        model = Evolucion
    
    nota = forms.CharField(widget=forms.Textarea(attrs={'class': 'big' }))

class GlucometriaForm(forms.ModelForm):
    
    class Meta:
        
        document = Glucometria
    
    fecha_y_hora = forms.DateTimeField(widget=forms.DateTimeInput(
                                            attrs={'class': 'datetimepicker' },
                                            format='%d/%m/%Y %H:%M'),
                                      input_formats=('%d/%m/%Y %H:%M',))
    
    observacion = forms.CharField(widget=forms.Textarea(attrs={'class': 'big' }))
    control = forms.CharField(widget=forms.TextInput)

class IngestaForm(forms.ModelForm):
    
    class Meta:
        
        document = Ingesta
    
    fecha_y_hora = forms.DateTimeField(widget=forms.DateTimeInput(
                                            attrs={'class': 'datetimepicker' },
                                            format='%d/%m/%Y %H:%M'),
                                      input_formats=('%d/%m/%Y %H:%M',),
                                      required=False)

class ExcretaForm(forms.ModelForm):
    
    class Meta:
        
        document = Excreta
    
    fecha_hora = forms.DateTimeField(widget=forms.DateTimeInput(
                                            attrs={'class': 'datetimepicker' },
                                            format='%d/%m/%Y %H:%M'),
                                      input_formats=('%d/%m/%Y %H:%M',))
class NotaEnfermeriaForm(forms.ModelForm):
    
    class Meta:
        
        document = NotaEnfermeria
    
    fecha_y_hora = forms.DateTimeField(widget=forms.DateTimeInput(
                                            attrs={'class': 'datetimepicker' },
                                            format='%d/%m/%Y %H:%M'),
                                      input_formats=('%d/%m/%Y %H:%M',))
    
    nota = forms.CharField(widget=forms.Textarea(attrs={'class': 'big' }))

class OrdenMedicaForm(forms.ModelForm):
    
    class Meta:
        
        document = OrdenMedica
    
    fecha_y_hora = forms.DateTimeField(widget=forms.DateTimeInput(
                                            attrs={'class': 'datetimepicker' },
                                            format='%d/%m/%Y %H:%M'),
                                      input_formats=('%d/%m/%Y %H:%M',),
                                      required=False)
    orden = forms.CharField(widget=forms.Textarea(attrs={'class': 'big' }))

class SignoVitalForm(forms.ModelForm):
    
    class Meta:
        
        document = SignoVital
