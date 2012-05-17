# -*- coding: utf-8 -*-
from django import forms
from clinique.models import Paciente, Visitante, Cita, Transaccion, Consultorio

class PacienteForm(forms.ModelForm):
    
    class Meta:
        
        model = Paciente
    
    consultorio = forms.ModelChoiceField(queryset=Consultorio.objects.all())
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(PacienteForm, self).__init__(*args, **kwargs)

        if user:
            self.fields['consultorio'].queryset = user.profile.consultorios.all()

class VisitanteForm(forms.ModelForm):
    
    class Meta:
        
        model = Visitante
    
    llegada = forms.DateTimeField(widget=forms.DateTimeInput(
                                            attrs={'class': 'datetimepicker' },
                                            format='%d/%m/%Y %H:%M'),
                                input_formats=('%d/%m/%Y %H:%M',),
                                required=False)
    programacion = forms.DateTimeField(widget=forms.DateTimeInput(
                                            attrs={'class': 'datetimepicker' },
                                            format='%d/%m/%Y %H:%M'),
                                input_formats=('%d/%m/%Y %H:%M',),
                                required=False)
    
    consultorio = forms.ModelChoiceField(label="",
                                  queryset=Consultorio.objects.all(),
                                  widget=forms.HiddenInput(), required=False)

class CitaForm(forms.ModelForm):

    class Meta:
        
        model = Cita
    
    fecha_y_hora = forms.DateTimeField(widget=forms.DateTimeInput(
                                            attrs={'class': 'datetimepicker' },
                                            format='%d/%m/%Y %H:%M'),
                                input_formats=('%d/%m/%Y %H:%M',),
                                required=False)
    
    consultorio = forms.ModelChoiceField(label="",
                                  queryset=Consultorio.objects.all(),
                                  widget=forms.HiddenInput(), required=False)

class TransaccionForm(forms.ModelForm):
    
    class Meta:
        
        model = Transaccion
    
    fecha_y_hora = forms.DateTimeField(widget=forms.DateTimeInput(
                                            attrs={'class': 'datetimepicker' },
                                            format='%d/%m/%Y %H:%M'),
                                input_formats=('%d/%m/%Y %H:%M',),
                                required=False)
    
    paciente = forms.ModelChoiceField(label="",
                                  queryset=Paciente.objects.all(),
                                  widget=forms.HiddenInput(), required=False)
