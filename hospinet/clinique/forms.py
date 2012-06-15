# -*- coding: utf-8 -*-
from clinique.models import (Paciente, Cita, Transaccion, Consultorio, Pago,
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

        model = HistoriaClinica

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

        model = Optometria

    fecha_y_hora = forms.DateTimeField(widget=forms.DateTimeInput(
                                            attrs={'class': 'datetimepicker' },
                                            format='%d/%m/%Y %H:%M'),
                                input_formats=('%d/%m/%Y %H:%M',),
                                required=False)
    
    paciente = forms.ModelChoiceField(label="",
                                  queryset=Paciente.objects.all(),
                                  widget=forms.HiddenInput(), required=False)

class PagoForm(forms.ModelForm):

    class Meta:

        model = Pago

    fecha_y_hora = forms.DateTimeField(widget=forms.DateTimeInput(
                                            attrs={'class': 'datetimepicker' },
                                            format='%d/%m/%Y %H:%M'),
                                input_formats=('%d/%m/%Y %H:%M',),
                                required=False)
    
    paciente = forms.ModelChoiceField(label="",
                                  queryset=Paciente.objects.all(),
                                  widget=forms.HiddenInput(), required=False)

class DiaForm(forms.Form):

    dia = forms.DateField(widget=forms.DateInput(attrs={'class' : 'datepicker'},
                                            format='%d/%m/%Y'),
                                input_formats=('%d/%m/%Y',))
