# -*- coding: utf-8 -*-
from django import forms
from spital.models import Admision
from nightingale.models import Cargo, Evolucion, Glucometria, Ingesta, Excreta,\
    NotaEnfermeria, OrdenMedica, SignoVital

class DateTimeWidget(forms.DateTimeInput):
  class Media:
    js = ('js/jquery-ui-timepicker-addon.js',)
  def __init__(self, attrs=None):
    if attrs is not None:
      self.attrs = attrs.copy()
    else:
      self.attrs = {'class': 'datetimepicker'}

    if not 'format' in self.attrs:
        self.attrs['format'] = '%d/%m/%Y %H:%M'

class IngresarForm(forms.ModelForm):
    
    class Meta:
        
        model = Admision
        fields = ('habitacion',)

class CargoForm(forms.ModelForm):
    
    class Meta:
        
        model = Cargo
    
    fecha_y_hora = forms.DateTimeField(widget=DateTimeWidget(),
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
    
#    fecha_y_hora = forms.DateTimeField(widget=DateTimeWidget(),
#                                       input_format=('%d/%m/%Y %H:%M',),
#                                       required=False)
    nota = forms.CharField(widget=forms.Textarea(attrs={'class': 'big' }))
    admision = forms.ModelChoiceField(label="",
                                  queryset=Admision.objects.all(),
                                  widget=forms.HiddenInput(), required=False)

class GlucometriaForm(forms.ModelForm):
    
    class Meta:
        
        model = Glucometria
    
    fecha_y_hora = forms.DateTimeField(widget=forms.DateTimeInput(
                                            attrs={'class': 'datetimepicker' },
                                            format='%d/%m/%Y %H:%M'),
                                      input_formats=('%d/%m/%Y %H:%M',))
    
    observacion = forms.CharField(widget=forms.Textarea(attrs={'class': 'big' }))
    control = forms.CharField(widget=forms.TextInput)
    admision = forms.ModelChoiceField(label="",
                                  queryset=Admision.objects.all(),
                                  widget=forms.HiddenInput(), required=False)

class IngestaForm(forms.ModelForm):
    
    class Meta:
        
        model = Ingesta
    
    fecha_y_hora = forms.DateTimeField(widget=forms.DateTimeInput(
                                            attrs={'class': 'datetimepicker' },
                                            format='%d/%m/%Y %H:%M'),
                                      input_formats=('%d/%m/%Y %H:%M',),
                                      required=False)

class ExcretaForm(forms.ModelForm):
    
    class Meta:
        
        model = Excreta
    
    fecha_hora = forms.DateTimeField(widget=forms.DateTimeInput(
                                            attrs={'class': 'datetimepicker' },
                                            format='%d/%m/%Y %H:%M'),
                                      input_formats=('%d/%m/%Y %H:%M',))
    admision = forms.ModelChoiceField(label="",
                                  queryset=Admision.objects.all(),
                                  widget=forms.HiddenInput(), required=False)

class NotaEnfermeriaForm(forms.ModelForm):
    
    class Meta:
        
        model = NotaEnfermeria
    
    fecha_y_hora = forms.DateTimeField(widget=forms.DateTimeInput(
                                            attrs={'class': 'datetimepicker' },
                                            format='%d/%m/%Y %H:%M'),
                                      input_formats=('%d/%m/%Y %H:%M',))
    
    nota = forms.CharField(widget=forms.Textarea(attrs={'class': 'big' }))
    admision = forms.ModelChoiceField(label="",
                                  queryset=Admision.objects.all(),
                                  widget=forms.HiddenInput(), required=False)

class OrdenMedicaForm(forms.ModelForm):
    
    class Meta:
        
       model = OrdenMedica
    
    fecha_y_hora = forms.DateTimeField(widget=forms.DateTimeInput(
                                            attrs={'class': 'datetimepicker' },
                                            format='%d/%m/%Y %H:%M'),
                                      input_formats=('%d/%m/%Y %H:%M',),
                                      required=False)
    orden = forms.CharField(widget=forms.Textarea(attrs={'class': 'big' }))
    admision = forms.ModelChoiceField(label="",
                                  queryset=Admision.objects.all(),
                                  widget=forms.HiddenInput(), required=False)

class SignoVitalForm(forms.ModelForm):
    
    class Meta:
        
        model = SignoVital
    
    admision = forms.ModelChoiceField(label="",
                                  queryset=Admision.objects.all(),
                                  widget=forms.HiddenInput(), required=False)
