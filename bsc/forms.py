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
from __future__ import unicode_literals

from crispy_forms.layout import Fieldset
from django import forms
from django.forms import modelformset_factory
from django.utils.translation import ugettext_lazy as _

from bsc.models import Encuesta, Respuesta, Voto, Opcion, Queja, ArchivoNotas, \
    Solucion, Rellamar
from clinique.models import Consulta
from persona.forms import FieldSetModelFormMixin, FieldSetModelFormMixinNoButton
from users.mixins import HiddenUserForm


class EncuestaFormMixin(FieldSetModelFormMixin):
    encuesta = forms.ModelChoiceField(queryset=Encuesta.objects.all(),
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
        self.helper.layout = Fieldset(_('Formulario de Respuesta'),
                                      *self.field_names)


class VotoForm(FieldSetModelFormMixinNoButton):
    class Meta:
        model = Voto
        fields = '__all__'

    respuesta = forms.ModelChoiceField(queryset=Respuesta.objects.all(),
                                       widget=forms.HiddenInput(),
                                       required=False)
    opcion = forms.ModelChoiceField(queryset=Opcion.objects.all(),
                                    widget=forms.RadioSelect(),
                                    required=True, empty_label=None)

    def __init__(self, *args, **kwargs):
        super(VotoForm, self).__init__(*args, **kwargs)
        self.fields['pregunta'].widget.attrs['readonly'] = True
        self.helper.layout = Fieldset(_('Formulario de Voto'),
                                      *self.field_names)


VotoFormSet = modelformset_factory(Voto, form=VotoForm, extra=0)


class QuejaForm(FieldSetModelFormMixin):
    class Meta:
        model = Queja
        exclude = ('resuelta',)

    respuesta = forms.ModelChoiceField(queryset=Respuesta.objects.all(),
                                       widget=forms.HiddenInput(),
                                       required=False)

    def __init__(self, *args, **kwargs):
        super(QuejaForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(_('Registrar Queja'), *self.field_names)


class QuejaFormMixin(FieldSetModelFormMixin):
    queja = forms.ModelChoiceField(queryset=Queja.objects.all(),
                                   widget=forms.HiddenInput(),
                                   required=False)


class SolucionForm(QuejaFormMixin, HiddenUserForm):
    class Meta:
        model = Solucion
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(SolucionForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(_('Registrar Solución'),
                                      *self.field_names)


class ArchivoNotasForm(FieldSetModelFormMixin):
    class Meta:
        model = ArchivoNotas
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ArchivoNotasForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(_('Subir Archivo de Notas'),
                                      *self.field_names)


class RellamarForm(FieldSetModelFormMixin):
    class Meta:
        model = Rellamar
        fields = '__all__'

    consulta = forms.ModelChoiceField(widget=forms.HiddenInput(),
                                      queryset=Consulta.objects.all())
    encuesta = forms.ModelChoiceField(widget=forms.HiddenInput(),
                                      queryset=Encuesta.objects.all())

    def __init__(self, *args, **kwargs):
        super(RellamarForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(_('Programar Lllamada'),
                                      *self.field_names)
