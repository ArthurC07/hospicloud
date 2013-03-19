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
                              Tratamiento, Hallazgo, Cobro, Diagnostico, ExamenFisico)
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

class EmergenciaBaseForm(forms.ModelForm):
    
    emergencia = forms.ModelChoiceField(label="",
                                  queryset=Emergencia.objects.all(),
                                  widget=forms.HiddenInput(), required=False)
    usuario = forms.ModelChoiceField(label="",
                                  queryset=User.objects.all(),
                                  widget=forms.HiddenInput(), required=False)

class RemisionInternaForm(EmergenciaBaseForm):

    """Formulario para agregar :class:`RemisionInterna`s"""

    class Meta:

        model = RemisionInterna

class RemisionExternaForm(EmergenciaBaseForm):

    """Formulario para agregar :class:`RemisionExterna`s"""

    class Meta:

        model = RemisionExterna

class ExamenFisicoForm(EmergenciaBaseForm):

    """Formulario para agregar :class:`ExamenFisico`s"""

    class Meta:

        model = ExamenFisico

class HallazgoForm(EmergenciaBaseForm):

    """Formulario para agregar :class:`RemisionExterna`s"""

    class Meta:

        model = Hallazgo

class TratamientoForm(EmergenciaBaseForm):

    """Formulario para agregar :class:`Tratamiento`s"""

    class Meta:

        model = Tratamiento

class DiagnosticoForm(EmergenciaBaseForm):

    """Formulario para agregar :class:`Tratamiento`s"""

    class Meta:

        model = Diagnostico

class CobroForm(EmergenciaBaseForm):

    """Formulario para agregar :class:`Cobro`s"""

    class Meta:

        model = Cobro
