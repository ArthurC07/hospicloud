# -*- coding: utf-8 -*-
from django import forms
from spital.models import Admision
from nightingale.models import (Cargo, Evolucion, Glicemia, Insulina,
                                Glucosuria, Ingesta, Excreta, NotaEnfermeria,
                                OrdenMedica, SignoVital, Medicamento)

class DateTimeWidget(forms.DateTimeInput):
    
    """Permite mostrar un input preparado para fecha y hora utilizando
    JQuery UI DateTimePicker"""

    class Media:
        js = ('js/jquery-ui-timepicker.js',)

    def __init__(self, attrs=None):
        if attrs is not None:
            self.attrs = attrs.copy()
        else:
            self.attrs = {'class': 'datetimepicker'}

        if not 'format' in self.attrs:
            self.attrs['format'] = '%d/%m/%Y %H:%M'

class IngresarForm(forms.ModelForm):
    
    """Muestra un formulario que permite ingresar a una :class:`Persona`
    al :class:`Hospital`"""

    class Meta:
        
        model = Admision
        fields = ('habitacion',)

class CargoForm(forms.ModelForm):
    
    """Muestra un formulario que permite agregar :class:`Cargo`s a una
    :class:`Persona` durante una :class:`Admision`"""

    class Meta:
        
        model = Cargo
        exclude = ("usuario",)
    
    fecha_y_hora = forms.DateTimeField(widget=DateTimeWidget(),
                                input_formats=('%d/%m/%Y %H:%M',),
                                required=False)
    
    inicio = forms.DateTimeField(widget=DateTimeWidget(),
                                input_formats=('%d/%m/%Y %H:%M',),
                                required=False)
    
    fin = forms.DateTimeField(widget=DateTimeWidget(),
                                input_formats=('%d/%m/%Y %H:%M',),
                                required=False)
    
    admision = forms.ModelChoiceField(label="",
                                  queryset=Admision.objects.all(),
                                  widget=forms.HiddenInput(), required=False)

class EvolucionForm(forms.ModelForm):
    
    """Muestra un formulario que permite agregar :class:`Evolucion`es a una
    :class:`Persona` durante una :class:`Admision`"""
    
    class Meta:
        
        model = Evolucion
        exclude = ("usuario",)
    
    fecha_y_hora = forms.DateTimeField(widget=DateTimeWidget(),
                                input_formats=('%d/%m/%Y %H:%M',),
                                required=False)
    nota = forms.CharField(widget=forms.Textarea(attrs={'class': 'big' }))
    admision = forms.ModelChoiceField(label="",
                                  queryset=Admision.objects.all(),
                                  widget=forms.HiddenInput(), required=False)

class GlicemiaForm(forms.ModelForm):
    
    """Muestra un formulario que permite agregar una lectura de
    :class:`Glicemia` a una :class:`Persona` durante una :class:`Admision`"""

    class Meta:
        
        model = Glicemia
        exclude = ("usuario",)
    
    fecha_y_hora = forms.DateTimeField(widget=DateTimeWidget(),
                                input_formats=('%d/%m/%Y %H:%M',),
                                required=False)
    
    observacion = forms.CharField(widget=forms.Textarea(attrs={'class': 'big' }))
    control = forms.CharField(widget=forms.TextInput)
    admision = forms.ModelChoiceField(label="",
                                  queryset=Admision.objects.all(),
                                  widget=forms.HiddenInput(), required=False)
    
class InsulinaForm(forms.ModelForm):
    
    """Muestra un formulario que permite registrar una administración de
    :class:`Insulina` a una :class:`Persona` durante una :class:`Admision`"""
    
    class Meta:
        
        model = Insulina
        exclude = ("usuario",)
    
    fecha_y_hora = forms.DateTimeField(widget=DateTimeWidget(),
                                input_formats=('%d/%m/%Y %H:%M',),
                                required=False)
    
    observacion = forms.CharField(widget=forms.Textarea(attrs={'class': 'big' }))
    control = forms.CharField(widget=forms.TextInput)
    admision = forms.ModelChoiceField(label="",
                                  queryset=Admision.objects.all(),
                                  widget=forms.HiddenInput(), required=False)

class GlucosuriaForm(forms.ModelForm):
    
    """Muestra un formulario que permite registrar :class:`Glucosuria`s a una
    :class:`Persona` durante una :class:`Admision`"""

    class Meta:
        
        model = Glucosuria
        exclude = ("usuario",)
    
    fecha_y_hora = forms.DateTimeField(widget=DateTimeWidget(),
                                input_formats=('%d/%m/%Y %H:%M',),
                                required=False)
    
    observacion = forms.CharField(widget=forms.Textarea(attrs={'class': 'big' }))
    control = forms.CharField(widget=forms.TextInput)
    admision = forms.ModelChoiceField(label="",
                                  queryset=Admision.objects.all(),
                                  widget=forms.HiddenInput(), required=False)

class IngestaForm(forms.ModelForm):
    
    """Muestra un formulario que permite registrar :class:`Ingesta`s a una
    :class:`Persona` durante una :class:`Admision`"""
    
    class Meta:
        
        model = Ingesta
        exclude = ("usuario",)
    
    fecha_y_hora = forms.DateTimeField(widget=DateTimeWidget(),
                                input_formats=('%d/%m/%Y %H:%M',),
                                required=False)

class ExcretaForm(forms.ModelForm):
    
    """Muestra un formulario que permite agregar :class:`Excreta`s a una
    :class:`Persona` durante una :class:`Admision`"""
    
    class Meta:
        
        model = Excreta
        exclude = ("usuario",)
    
    fecha_hora = forms.DateTimeField(widget=DateTimeWidget(),
                                input_formats=('%d/%m/%Y %H:%M',),
                                required=False)
    admision = forms.ModelChoiceField(label="",
                                  queryset=Admision.objects.all(),
                                  widget=forms.HiddenInput(), required=False)

class NotaEnfermeriaForm(forms.ModelForm):
    
    """Muestra un formulario que permite agregar :class:`Cargo`s a una
    :class:`Persona` durante una :class:`Admision`"""
    
    class Meta:
        
        model = NotaEnfermeria
        exclude = ("usuario",)
    
    fecha_y_hora = forms.DateTimeField(widget=DateTimeWidget(),
                                input_formats=('%d/%m/%Y %H:%M',),
                                required=False)
    
    nota = forms.CharField(widget=forms.Textarea(attrs={'class': 'big' }))
    admision = forms.ModelChoiceField(label="",
                                  queryset=Admision.objects.all(),
                                  widget=forms.HiddenInput(), required=False)

class OrdenMedicaForm(forms.ModelForm):
    
    """Muestra un formulario que permite agregar :class:`OrdenMedica`s a una
    :class:`Persona` durante una :class:`Admision`"""
    
    class Meta:
        
       model = OrdenMedica
       exclude = ('usuario',)

    fecha_y_hora = forms.DateTimeField(widget=DateTimeWidget(),
                                input_formats=('%d/%m/%Y %H:%M',),
                                required=False)
    orden = forms.CharField(widget=forms.Textarea(attrs={'class': 'big' }))
    admision = forms.ModelChoiceField(label="",
                                  queryset=Admision.objects.all(),
                                  widget=forms.HiddenInput(), required=False)

class SignoVitalForm(forms.ModelForm):

    """Muestra un formulario que permite registrar lectura de
    :class:`SignoVital`es a una :class:`Persona` durante una
    :class:`Admision`"""
    
    class Meta:
        
        model = SignoVital
        exclude = ("presion_arterial_media", 'usuario')
    
    fecha_y_hora = forms.DateTimeField(widget=DateTimeWidget(),
                                input_formats=('%d/%m/%Y %H:%M',),
                                required=False)
    admision = forms.ModelChoiceField(label="",
                                  queryset=Admision.objects.all(),
                                  widget=forms.HiddenInput(), required=False)

class MedicamentoForm(forms.ModelForm):

    """Permite Agregar o modificar los datos de un :class:`Medicamento`"""

    class Meta:

        model = Medicamento
        exclude = ('usuario',)
    
    fecha_y_hora = forms.DateTimeField(widget=DateTimeWidget(),
                                input_formats=('%d/%m/%Y %H:%M',),
                                required=False)
