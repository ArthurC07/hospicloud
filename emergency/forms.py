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
from __future__ import unicode_literals

from crispy_forms.layout import Fieldset
from django import forms
from django.contrib.auth.models import User

from emergency.models import Emergencia, RemisionInterna, RemisionExterna, \
    Tratamiento, Hallazgo, Cobro, Diagnostico, ExamenFisico
from inventory.models import ItemTemplate
from persona.forms import FieldSetModelFormMixin
from persona.models import Persona


class EmergenciaForm(FieldSetModelFormMixin):
    """Formulario para agregar :class:`Emergencia`s"""

    class Meta:
        model = Emergencia
        exclude = ('facturada',)

    persona = forms.ModelChoiceField(
        queryset=Persona.objects.all(),
        widget=forms.HiddenInput(), required=False)
    usuario = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=forms.HiddenInput(), required=False)


class EmergenciaBaseForm(FieldSetModelFormMixin):
    emergencia = forms.ModelChoiceField(
        queryset=Emergencia.objects.all(),
        widget=forms.HiddenInput(),
        required=False)
    usuario = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=forms.HiddenInput(), required=False)

    def __init__(self, *args, **kwargs):
        super(EmergenciaBaseForm, self).__init__(*args, **kwargs)


class RemisionInternaForm(EmergenciaBaseForm):
    """Formulario para agregar :class:`RemisionInterna`s"""

    class Meta:
        model = RemisionInterna
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(RemisionInternaForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset('Remitir a un Especialista',
                                      *self.field_names)


class RemisionExternaForm(EmergenciaBaseForm):
    """Formulario para agregar :class:`RemisionExterna`s"""

    class Meta:
        model = RemisionExterna
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(RemisionExternaForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset('Remitir a otro Centro',
                                      *self.field_names)


class ExamenFisicoForm(EmergenciaBaseForm):
    """Formulario para agregar :class:`ExamenFisico`s"""

    class Meta:
        model = ExamenFisico
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ExamenFisicoForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset('Agregar Examen Físico',
                                      *self.field_names)


class HallazgoForm(EmergenciaBaseForm):
    """Formulario para agregar :class:`RemisionExterna`s"""

    class Meta:
        model = Hallazgo
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(HallazgoForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset('Agregar Hallazgo', *self.field_names)


class TratamientoForm(EmergenciaBaseForm):
    """Formulario para agregar :class:`Tratamiento`s"""

    class Meta:
        model = Tratamiento
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(TratamientoForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset('Agregar Tratamiento', *self.field_names)


class DiagnosticoForm(EmergenciaBaseForm):
    """Formulario para agregar :class:`Tratamiento`s"""

    class Meta:
        model = Diagnostico
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(DiagnosticoForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset('Agregar Diagnostico', *self.field_names)


class CobroForm(EmergenciaBaseForm):
    """Formulario para agregar :class:`Cobro`s"""

    class Meta:
        model = Cobro
        exclude = ('facturado',)

    cargo = forms.ModelChoiceField(
        queryset=ItemTemplate.objects.filter(activo=True).order_by(
            'descripcion').all())

    def __init__(self, *args, **kwargs):
        super(CobroForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset('Agregar Materiales y Medicamentos',
                                      *self.field_names)
