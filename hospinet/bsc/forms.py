# -*- coding: utf-8 -*-
#
# Copyright (C) 2015 Carlos Flores <cafg10@gmail.com>
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
from crispy_forms.layout import Fieldset
from django import forms

from bsc.models import Encuesta, Respuesta, Voto
from persona.forms import FieldSetModelFormMixin


class EncuestaFormMixin(FieldSetModelFormMixin):
    encuesta = forms.ModelChoiceField(label="", queryset=Encuesta.objects.all(),
                                      widget=forms.HiddenInput(),
                                      required=False)


class RespuestaForm(FieldSetModelFormMixin):
    class Meta:
        model = Respuesta
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(RespuestaForm, self).__init__(*args, **kwargs)
        self.fields['encuesta'].widget.attrs['readonly'] = True
        self.fields['consulta'].widget.attrs['readonly'] = True
        self.helper.layout = Fieldset(u'Formulario de Respuesta',
                                      *self.field_names)


class VotoForm(FieldSetModelFormMixin):
    class Meta:
        model = Voto
        fields = '__all__'

    respuesta = forms.ModelChoiceField(label='',
                                       queryset=Respuesta.objects.all(),
                                       widget=forms.HiddenInput(),
                                       required=False)

    def __init__(self, *args, **kwargs):
        super(VotoForm, self).__init__(*args, **kwargs)
        self.fields['pregunta'].widget.attrs['readonly'] = True
        self.helper.layout = Fieldset(u'Formulario de Voto', *self.field_names)
