# -*- coding: utf-8 -*-
from clinique.models import (Paciente, Cita, Transaccion, Consultorio, Pago,
                             Consulta, Receta, HistoriaClinica, Optometria)
from django import forms
from django.contrib.auth.models import User
from persona.forms import DateTimeWidget

class DateForm(forms.ModelForm):

    """Formulario base para los distintos ingresos de información que requieren
    una fecha y hora"""

    fecha_y_hora = forms.DateTimeField(widget=DateTimeWidget(), required=False)
    
class ConsultorioForm(forms.ModelForm):
    
    """Permite editar los datos  de un :class:`Consultorio`"""

    class Meta:
        
        model = Consultorio
        fields = ('nombre', )
    
    doctor = forms.ModelChoiceField(label="",
                                  queryset=User.objects.all(),
                                  widget=forms.HiddenInput(), required=False)

class PacienteForm(forms.ModelForm):
    
    """Permite editar los datos de un :class:`Paciente`"""

    class Meta:
        
        model = Paciente
    
    consultorio = forms.ModelChoiceField(label="",
                                  queryset=Consultorio.objects.all(),
                                  widget=forms.HiddenInput(), required=False)

class CitaForm(DateForm):

    """Permite editar los datos de una :class:`Cita`"""

    class Meta:
        
        model = Cita
    
    consultorio = forms.ModelChoiceField(label="",
                                  queryset=Consultorio.objects.all(),
                                  widget=forms.HiddenInput(), required=False)

class TransaccionForm(DateForm):
    
    class Meta:
        
        model = Transaccion
    
    paciente = forms.ModelChoiceField(label="",
                                  queryset=Paciente.objects.all(),
                                  widget=forms.HiddenInput(), required=False)

class ConsultaForm(DateForm):

    """Crea un formulario para agregar una :class:`Consulta`"""

    class Meta:

        model = Consulta

    paciente = forms.ModelChoiceField(label="",
                                  queryset=Paciente.objects.all(),
                                  widget=forms.HiddenInput(), required=False)

class RecetaForm(DateForm):

    """Crea un formulario para agregar una :class:`Receta`"""

    class Meta:

        model = Receta
    
    paciente = forms.ModelChoiceField(label="",
                                  queryset=Paciente.objects.all(),
                                  widget=forms.HiddenInput(), required=False)

class HistoriaClinicaForm(DateForm):

    """Crea un formulario para agregar una :class:`Historiaclinica`"""

    class Meta:

        model = HistoriaClinica
    
    paciente = forms.ModelChoiceField(label="",
                                  queryset=Paciente.objects.all(),
                                  widget=forms.HiddenInput(), required=False)

class OptometriaForm(DateForm):

    """Crea un formulario para agregar una :class:`Optometria`"""

    class Meta:

        model = Optometria
    
    paciente = forms.ModelChoiceField(label="",
                                  queryset=Paciente.objects.all(),
                                  widget=forms.HiddenInput(), required=False)

class PagoForm(DateForm):

    class Meta:

        model = Pago
    
    paciente = forms.ModelChoiceField(label="",
                                  queryset=Paciente.objects.all(),
                                  widget=forms.HiddenInput(), required=False)

class DiaForm(forms.Form):

    dia = forms.DateField(widget=forms.DateInput(attrs={'class' : 'datepicker'},
                                            format='%d/%m/%Y'),
                                input_formats=('%d/%m/%Y',))
