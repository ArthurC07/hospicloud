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
from crispy_forms.layout import Fieldset
from django.utils import timezone

from spital.models import Admision, Habitacion, PreAdmision, Deposito
from emergency.models import Emergencia
from persona.models import Persona
from persona.forms import DateTimeWidget, FieldSetModelFormMixin


class AdmisionForm(FieldSetModelFormMixin):
    """Permite ingresar una :class:`Admision` al Hospital"""

    class Meta:
        model = Admision
        fields = ('paciente', 'diagnostico', 'doctor',
                  'arancel', 'pago', 'poliza', 'certificado', 'aseguradora',
                  'tipo_de_ingreso', 'tipo_de_venta')

    paciente = forms.ModelChoiceField(label="",
                                      queryset=Persona.objects.all(),
                                      widget=forms.HiddenInput(),
                                      required=False)

    doctor = forms.CharField(label="Medico Tratante", required=True)
    diagnostico = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super(AdmisionForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Datos de la Admisión', *self.field_names)


class HabitacionForm(FieldSetModelFormMixin):
    """Permite gestionar los datos de una :class:`Habitacion`"""

    class Meta:
        model = Habitacion
        fields = '__all__'


class PreAdmisionForm(FieldSetModelFormMixin):
    class Meta:
        model = PreAdmision
        exclude = ('completada', )

    emergencia = forms.ModelChoiceField(label="",
                                        queryset=Emergencia.objects.all(),
                                        widget=forms.HiddenInput(),
                                        required=False)

    def __init__(self, *args, **kwargs):
        super(PreAdmisionForm, self).__init__(*args, **kwargs)


class IngresarForm(FieldSetModelFormMixin):
    """Muestra un formulario que permite ingresar a una :class:`Persona`
    al :class:`Hospital`"""

    class Meta:
        model = Admision
        fields = ('habitacion', 'ingreso', 'hospitalizacion')

    ingreso = forms.DateTimeField(widget=DateTimeWidget(), required=True,
                                  initial=timezone.now)
    hospitalizacion = forms.DateTimeField(widget=DateTimeWidget(),
                                          required=True,
                                          initial=timezone.now)

    def __init__(self, *args, **kwargs):
        super(IngresarForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Hospitalizar Paciente',
                                      *self.field_names)


class DepositoForm(FieldSetModelFormMixin):

    class Meta:
        model = Deposito
        fields = '__all__'

    fecha = forms.DateTimeField(widget=DateTimeWidget(),
                                required=False,
                                initial=timezone.now)

    def __init__(self, *args, **kwargs):
        super(DepositoForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Agregar Deposito', *self.field_names)
