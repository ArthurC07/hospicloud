# -*- coding: utf-8 -*-
from clinique.models import (Paciente, Cita, Transaccion, Consultorio,
                             Consulta, Receta, HistoriaClinica, Optometria)
from django import forms
from users.models import Profile

class ConsultorioForm(forms.ModelForm):
    
    class Meta:
        
        model = Consultorio
        fields = ('nombre', )
    
    doctor = forms.ModelChoiceField(label="",
                                  queryset=Profile.objects.all(),
                                  widget=forms.HiddenInput(), required=False)

class PacienteForm(forms.ModelForm):
    
    class Meta:
        
        model = Paciente
    
    consultorio = forms.ModelChoiceField(label="",
                                  queryset=Consultorio.objects.all(),
                                  widget=forms.HiddenInput(), required=False)
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(PacienteForm, self).__init__(*args, **kwargs)

        if user:
            self.fields['consultorio'].queryset = user.profile.consultorios.all()

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

class ConsultaForm(forms.ModelForm):

    """Crea un formulario para agregar una :class:`Consulta`"""

    class Meta:

        model = Consulta
    
    fecha_y_hora = forms.DateTimeField(widget=forms.DateTimeInput(
                                            attrs={'class': 'datetimepicker' },
                                            format='%d/%m/%Y %H:%M'),
                                input_formats=('%d/%m/%Y %H:%M',),
                                required=False)

    paciente = forms.ModelChoiceField(label="",
                                  queryset=Paciente.objects.all(),
                                  widget=forms.HiddenInput(), required=False)

class RecetaForm(forms.ModelForm):

    """Crea un formulario para agregar una :class:`Receta`"""

    class Meta:

        model = Receta

    fecha_y_hora = forms.DateTimeField(widget=forms.DateTimeInput(
                                            attrs={'class': 'datetimepicker' },
                                            format='%d/%m/%Y %H:%M'),
                                input_formats=('%d/%m/%Y %H:%M',),
                                required=False)
    
    paciente = forms.ModelChoiceField(label="",
                                  queryset=Paciente.objects.all(),
                                  widget=forms.HiddenInput(), required=False)

class HistoriaClinicaForm(forms.ModelForm):

    """Crea un formulario para agregar una :class:`Historiaclinica`"""

    class Meta:

        model = Historiaclinica

    fecha_y_hora = forms.DateTimeField(widget=forms.DateTimeInput(
                                            attrs={'class': 'datetimepicker' },
                                            format='%d/%m/%Y %H:%M'),
                                input_formats=('%d/%m/%Y %H:%M',),
                                required=False)
    
    paciente = forms.ModelChoiceField(label="",
                                  queryset=Paciente.objects.all(),
                                  widget=forms.HiddenInput(), required=False)

class OptometriaForm(forms.ModelForm):

    """Crea un formulario para agregar una :class:`Optometria`"""

    class Meta:

        model = Historiaclinica

    fecha_y_hora = forms.DateTimeField(widget=forms.DateTimeInput(
                                            attrs={'class': 'datetimepicker' },
                                            format='%d/%m/%Y %H:%M'),
                                input_formats=('%d/%m/%Y %H:%M',),
                                required=False)
    
    paciente = forms.ModelChoiceField(label="",
                                  queryset=Paciente.objects.all(),
                                  widget=forms.HiddenInput(), required=False)
