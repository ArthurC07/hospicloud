# -*- coding: utf-8 -*-
#
# Copyright (C) 2011-2013 Carlos Flores <cafg10@gmail.com>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library. If not, see <http://www.gnu.org/licenses/>.

from django import forms
from django.http import HttpRequest
from imaging.models import Examen, Imagen, Adjunto, Dicom, EstudioProgramado
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
    
    """Muestra el formulario para agregar archivos :class:`Adjunto`s a un
    :class:`Examen`"""

    class Meta:
        
        model = Adjunto
    
    examen = forms.ModelChoiceField(label="",
                                  queryset=Examen.objects.all(),
                                  widget=forms.HiddenInput())

class DicomForm(forms.ModelForm):
    
    """Muestra el formulario para agregar un archivo :class:`Dicom` a un
    :class:`Examen`"""

    class Meta:
        
        model = Dicom
        fields = ('descripcion', 'archivo')
    
    examen = forms.ModelChoiceField(label="",
                                  queryset=Examen.objects.all(),
                                  widget=forms.HiddenInput())

class EstudioProgramadoForm(forms.ModelForm):
    
    """"Permite mostrar los formularios para crear una :class:`Remision`"""

    class Meta:
        
        model = EstudioProgramado
        exclude = ('efectuado', 'usuario',)
    
    persona = forms.ModelChoiceField(label="",
                                  queryset=Persona.objects.all(),
                                  widget=forms.HiddenInput(), required=False)

class EmailForm(forms.Form):

    """Permite mostrar un formulario para enviar notificaciones a diversos
    correos"""

    email = forms.CharField()
    examen = forms.ModelChoiceField(label="",
                                  queryset=Examen.objects.all(),
                                  widget=forms.HiddenInput())

    def send_email(self):

        """Realiza el envio del correo electrónico"""
        
        pass
