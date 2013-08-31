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
from spital.models import Admision, Habitacion, PreAdmision
from emergency.models import Emergencia
from persona.models import Persona
from persona.forms import FieldSetModelFormMixin
from django.utils.translation.trans_null import _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Fieldset

class AdmisionForm(FieldSetModelFormMixin):
    
    """Permite ingresar una :class:`Admision` al Hospital"""

    class Meta:
        
        model = Admision
        fields = ('paciente', 'diagnostico', 'doctor',
                  'arancel', 'pago', 'poliza', 'certificado', 'aseguradora',
                  'deposito', 'tipo_de_ingreso', 'tipo_de_venta')
    
    paciente = forms.ModelChoiceField(label="",
                                  queryset=Persona.objects.all(),
                                  widget=forms.HiddenInput(), required=False)

    doctor = forms.CharField(label="Medico Tratante", required=True)
    diagnostico = forms.CharField(required=True)

class HabitacionForm(FieldSetModelFormMixin):

    """Permite gestionar los datos de una :class:`Habitacion`"""

    class Meta:

        model = Habitacion

class PreAdmisionForm(FieldSetModelFormMixin):
    
    class Meta:
        
        model = PreAdmision
        exclude = ('completada', )
    
    emergencia = forms.ModelChoiceField(label="",
                                  queryset=Emergencia.objects.all(),
                                  widget=forms.HiddenInput(), required=False)

    def __init__(self, *args, **kwargs):

        super(PreAdmisionForm, self).__init__(*args, **kwargs)

class IngresarForm(FieldSetModelFormMixin):
    
    """Muestra un formulario que permite ingresar a una :class:`Persona`
    al :class:`Hospital`"""

    class Meta:
        
        model = Admision
        fields = ('habitacion',)

    def __init__(self, *args, **kwargs):

        super(IngresarForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Hospitalizar Paciente',
                                      *self.field_names)
