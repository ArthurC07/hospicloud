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
from emergency.models import (Emergencia, RemisionInterna, RemisionExterna,
                              Tratamiento, Hallazgo, Cobro)
from inventory.models import ItemTemplate
from persona.models import Persona
from django.contrib.auth.models import User

class EmergenciaForm(forms.ModelForm):

    """Formulario para agregar :class:`Emergencia`s"""

    class Meta:

        model = Emergencia
    
    persona = forms.ModelChoiceField(label="",
                                  queryset=Persona.objects.all(),
                                  widget=forms.HiddenInput(), required=False)
    usuario = forms.ModelChoiceField(label="",
                                  queryset=User.objects.all(),
                                  widget=forms.HiddenInput(), required=False)

class RemisionInternaForm(forms.ModelForm):

    """Formulario para agregar :class:`RemisionInterna`s"""

    class Meta:

        model = RemisionInterna
    
    emergencia = forms.ModelChoiceField(label="",
                                  queryset=Emergencia.objects.all(),
                                  widget=forms.HiddenInput(), required=False)
    usuario = forms.ModelChoiceField(label="",
                                  queryset=User.objects.all(),
                                  widget=forms.HiddenInput(), required=False)

class RemisionExternaForm(forms.ModelForm):

    """Formulario para agregar :class:`RemisionExterna`s"""

    class Meta:

        model = RemisionExterna
    
    emergencia = forms.ModelChoiceField(label="",
                                  queryset=Emergencia.objects.all(),
                                  widget=forms.HiddenInput(), required=False)
    usuario = forms.ModelChoiceField(label="",
                                  queryset=User.objects.all(),
                                  widget=forms.HiddenInput(), required=False)

class HallazgoForm(forms.ModelForm):

    """Formulario para agregar :class:`RemisionExterna`s"""

    class Meta:

        model = Hallazgo
    
    emergencia = forms.ModelChoiceField(label="",
                                  queryset=Emergencia.objects.all(),
                                  widget=forms.HiddenInput(), required=False)
    usuario = forms.ModelChoiceField(label="",
                                  queryset=User.objects.all(),
                                  widget=forms.HiddenInput(), required=False)

class TratamientoForm(forms.ModelForm):

    """Formulario para agregar :class:`Tratamiento`s"""

    class Meta:

        model = Tratamiento
    
    emergencia = forms.ModelChoiceField(label="",
                                  queryset=Emergencia.objects.all(),
                                  widget=forms.HiddenInput(), required=False)
    usuario = forms.ModelChoiceField(label="",
                                  queryset=User.objects.all(),
                                  widget=forms.HiddenInput(), required=False)

class CobroForm(forms.ModelForm):

    """Formulario para agregar :class:`Cobro`s"""

    class Meta:

        model = Cobro
    
    emergencia = forms.ModelChoiceField(label="",
                                  queryset=Emergencia.objects.all(),
                                  widget=forms.HiddenInput(), required=False)
    cargo = forms.ModelChoiceField(label="",
                                  queryset=ItemTemplate.objects.filter(emergencia=True).all(),
                                  required=False)
    usuario = forms.ModelChoiceField(label="",
                                  queryset=User.objects.all(),
                                  widget=forms.HiddenInput(), required=False)
