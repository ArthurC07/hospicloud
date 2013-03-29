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
from spital.models import Admision, Habitacion
from persona.models import Persona
from django.utils.translation.trans_null import _

class AdmisionForm(forms.ModelForm):
    
    """Permite ingresar una :class:`Admision` al Hospital"""

    class Meta:
        
        model = Admision
        fields = ('paciente', 'diagnostico', 'doctor',
                  'arancel', 'pago', 'poliza', 'certificado', 'aseguradora',
                  'deposito', 'tipo_de_ingreso',)
    
    paciente = forms.ModelChoiceField(label="",
                                  queryset=Persona.objects.all(),
                                  widget=forms.HiddenInput(), required=False)

class HabitacionForm(forms.ModelForm):

    """Permite gestionar los datos de una :class:`Habitacion`"""

    class Meta:

        model = Habitacion
