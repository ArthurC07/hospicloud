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
from django.forms import modelformset_factory
from django.utils.translation import ugettext_lazy as _

from bsc.models import Encuesta, Respuesta, Voto, Opcion, Queja
from persona.forms import FieldSetModelFormMixin, FieldSetModelFormMixinNoButton


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
        self.helper.layout = Fieldset(_(u'Formulario de Respuesta'),
                                      *self.field_names)


class VotoForm(FieldSetModelFormMixinNoButton):
    class Meta:
        model = Voto
        fields = '__all__'

    respuesta = forms.ModelChoiceField(label='',
                                       queryset=Respuesta.objects.all(),
                                       widget=forms.HiddenInput(),
                                       required=False)
    opcion = forms.ModelChoiceField(label='',
                                    queryset=Opcion.objects.all(),
                                    widget=forms.RadioSelect(),
                                    required=False)

    def __init__(self, *args, **kwargs):
        super(VotoForm, self).__init__(*args, **kwargs)
        self.fields['pregunta'].widget.attrs['readonly'] = True
        self.helper.layout = Fieldset(_(u'Formulario de Voto'),
                                      *self.field_names)


VotoFormSet = modelformset_factory(Voto, form=VotoForm, extra=0)


class QuejaForm(FieldSetModelFormMixin):
    class Meta:
        model = Queja
        exclude = ('resuelta',)

    respuesta = forms.ModelChoiceField(label='',
                                       queryset=Respuesta.objects.all(),
                                       widget=forms.HiddenInput(),
                                       required=False)

    def __init__(self, *args, **kwargs):
        super(QuejaForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(_(u'Registrar Queja'), *self.field_names)
