# -*- coding: utf-8 -*-
from django import forms
from spital.models import Admision
from nightingale.models import (Cargo, Evolucion, Glicemia, Insulina, Dosis,
                                Glucosuria, Ingesta, Excreta, NotaEnfermeria,
                                OrdenMedica, SignoVital, Medicamento, Devolucion)
from django.contrib.auth.models import User
from persona.forms import DateTimeWidget

class BaseForm(forms.ModelForm):

    """Formulario base para los distintos ingresos de información de parte de
    los diversos modelos de enfermeria"""

    fecha_y_hora = forms.DateTimeField(widget=DateTimeWidget(), required=False)
    
    admision = forms.ModelChoiceField(label="",
                                  queryset=Admision.objects.all(),
                                  widget=forms.HiddenInput(), required=False)
    
    usuario = forms.ModelChoiceField(label="",
                                  queryset=User.objects.all(),
                                  widget=forms.HiddenInput(), required=False)

class IngresarForm(forms.ModelForm):
    
    """Muestra un formulario que permite ingresar a una :class:`Persona`
    al :class:`Hospital`"""

    class Meta:
        
        model = Admision
        fields = ('habitacion',)

class CargoForm(BaseForm):
    
    """Muestra un formulario que permite agregar :class:`Cargo`s a una
    :class:`Persona` durante una :class:`Admision`"""

    class Meta:
        
        model = Cargo
    
    inicio = forms.DateTimeField(widget=DateTimeWidget(),
                                input_formats=('%d/%m/%Y %H:%M',),
                                required=False)
    
    fin = forms.DateTimeField(widget=DateTimeWidget(),
                                input_formats=('%d/%m/%Y %H:%M',),
                                required=False)

class EvolucionForm(BaseForm):
    
    """Muestra un formulario que permite agregar :class:`Evolucion`es a una
    :class:`Persona` durante una :class:`Admision`"""
    
    class Meta:
        
        model = Evolucion

    nota = forms.CharField(widget=forms.Textarea(attrs={'class': 'big' }))

class GlicemiaForm(BaseForm):
    
    """Muestra un formulario que permite agregar una lectura de
    :class:`Glicemia` a una :class:`Persona` durante una :class:`Admision`"""

    class Meta:
        
        model = Glicemia
    
    observacion = forms.CharField(widget=forms.Textarea(attrs={'class': 'big' }))
    control = forms.CharField(widget=forms.TextInput)
    
class InsulinaForm(BaseForm):
    
    """Muestra un formulario que permite registrar una administración de
    :class:`Insulina` a una :class:`Persona` durante una :class:`Admision`"""
    
    class Meta:
        
        model = Insulina
    
    control = forms.CharField(widget=forms.TextInput)

class GlucosuriaForm(BaseForm):
    
    """Muestra un formulario que permite registrar :class:`Glucosuria`s a una
    :class:`Persona` durante una :class:`Admision`"""

    class Meta:
        
        model = Glucosuria
    
    observacion = forms.CharField(widget=forms.Textarea(attrs={'class': 'big' }))
    control = forms.CharField(widget=forms.TextInput)

class IngestaForm(BaseForm):
    
    """Muestra un formulario que permite registrar :class:`Ingesta`s a una
    :class:`Persona` durante una :class:`Admision`"""
    
    class Meta:
        
        model = Ingesta
        exclude = ("usuario",)

class ExcretaForm(BaseForm):
    
    """Muestra un formulario que permite agregar :class:`Excreta`s a una
    :class:`Persona` durante una :class:`Admision`"""
    
    class Meta:
        
        model = Excreta

class NotaEnfermeriaForm(BaseForm):
    
    """Muestra un formulario que permite agregar :class:`Cargo`s a una
    :class:`Persona` durante una :class:`Admision`"""
    
    class Meta:
        
        model = NotaEnfermeria
    
    nota = forms.CharField(widget=forms.Textarea(attrs={'class': 'big' }))
    admision = forms.ModelChoiceField(label="",
                                  queryset=Admision.objects.all(),
                                  widget=forms.HiddenInput(), required=False)

class OrdenMedicaForm(BaseForm):
    
    """Muestra un formulario que permite agregar :class:`OrdenMedica`s a una
    :class:`Persona` durante una :class:`Admision`"""
    
    class Meta:
        
       model = OrdenMedica

    orden = forms.CharField(widget=forms.Textarea(attrs={'class': 'big' }))

class SignoVitalForm(BaseForm):

    """Muestra un formulario que permite registrar lectura de
    :class:`SignoVital`es a una :class:`Persona` durante una
    :class:`Admision`"""
    
    class Meta:
        
        model = SignoVital
        exclude = ("presion_arterial_media")

class MedicamentoForm(BaseForm):

    """Permite Agregar o modificar los datos de un :class:`Medicamento`"""

    class Meta:

        model = Medicamento

    inicio = forms.DateTimeField(widget=DateTimeWidget(), required=False)

class DosisForm(forms.ModelForm):

    class Meta:

        model = Dosis
    
    fecha_y_hora = forms.DateTimeField(widget=DateTimeWidget(), required=False)
    
    medicamento = forms.ModelChoiceField(label="",
                                  queryset=Medicamento.objects.all(),
                                  widget=forms.HiddenInput(), required=False)
    
    usuario = forms.ModelChoiceField(label="",
                                  queryset=User.objects.all(),
                                  widget=forms.HiddenInput(), required=False)
    
    administrador = forms.ModelChoiceField(label="",
                                  queryset=User.objects.all(),
                                  widget=forms.HiddenInput(), required=False)

class DevolucionForm(BaseForm):

    """Permite editar los datos de una :class:`Devolucion`"""

    class Meta:
         
        model = Devolucion
