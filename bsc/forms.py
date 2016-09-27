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

from crispy_forms.layout import Fieldset, Submit
from crispy_forms.helper import FormHelper
from django import forms
from django.forms import modelformset_factory
from django.utils.translation import ugettext_lazy as _

from bsc.models import Encuesta, Respuesta, Voto, Opcion, Queja, ArchivoNotas, \
    Solucion, Rellamar, Departamento
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
                                    required=False, empty_label=None)

    def __init__(self, *args, **kwargs):
        super(VotoForm, self).__init__(*args, **kwargs)
        self.fields['pregunta'].widget.attrs['readonly'] = True
        self.helper.layout = Fieldset(_('Formulario de Voto'),
                                      *self.field_names)


VotoFormSet = modelformset_factory(Voto, form=VotoForm, extra=0)


class QuejaForm(FieldSetModelFormMixinNoButton):
    class Meta:
        model = Queja
        exclude = ('resuelta', 'aseguradora')

    respuesta = forms.ModelChoiceField(queryset=Respuesta.objects.all(),
                                       widget=forms.HiddenInput(),
                                       required=False)

    def __init__(self, *args, **kwargs):
        super(QuejaForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(_('Registrar Queja'), *self.field_names)
        self.helper.add_input(Submit('submit', _('Guardar Solo la Queja')))


class QuejaFormMixin(FieldSetModelFormMixin):
    queja = forms.ModelChoiceField(queryset=Queja.objects.all(),
                                   widget=forms.HiddenInput(),
                                   required=False)


class QuejaAseguradoraForm(FieldSetModelFormMixin):
    """
    Defines a form used to create :class:`Queja` that have been sent by a
    :class:`Aseguradora
    """
    class Meta:
        model = Queja
        exclude = ('resuelta', )

    def __init__(self, *args, **kwargs):
        super(QuejaAseguradoraForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(_('Registrar Queja'), *self.field_names)


class SolucionForm(QuejaFormMixin, HiddenUserForm):
    """
    Shows a form to create or modify :class:`Solucion`
    """
    class Meta:
        model = Solucion
        exclude = ('aceptada', 'rechazada', 'notificada')

    def __init__(self, *args, **kwargs):
        super(SolucionForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(_('Enviar Solución'), *self.field_names)


class ArchivoNotasForm(FieldSetModelFormMixin):
    class Meta:
        model = ArchivoNotas
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ArchivoNotasForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(_('Subir Archivo de Notas'),
                                      *self.field_names)


class RellamarForm(FieldSetModelFormMixin):
    """
    Defines a form used to create :class:`Rellamada`
    """
    class Meta:
        model = Rellamar
        fields = '__all__'

    consulta = forms.ModelChoiceField(widget=forms.HiddenInput(),
                                      queryset=Consulta.objects.all())
    encuesta = forms.ModelChoiceField(widget=forms.HiddenInput(),
                                      queryset=Encuesta.objects.all())

    def __init__(self, *args, **kwargs):
        super(RellamarForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(_('Programar Llamada'),
                                      *self.field_names)


class SolucionAceptadaForm(FieldSetModelFormMixinNoButton):
    """
    Creates a form that allows marking a :class:`Solucion` as acepted
    """
    class Meta:
        model = Solucion
        fields = ('aceptada',)

    aceptada = forms.BooleanField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        if 'initial' not in kwargs:
            kwargs['initial'] = {'aceptada': True}
        else:
            kwargs['initial']['aceptada'] = True
        super(SolucionAceptadaForm, self).__init__(*args, **kwargs)
        self.helper.label_class = ''
        self.helper.field_class = ''
        self.helper.form_class = ''
        self.helper.add_input(
            Submit(
                'submit',
                _('Aceptar Solución'),
                css_class='btn-block',
            ))
        self.helper.form_tag = False


class SolucionRechazadaForm(FieldSetModelFormMixinNoButton):
    """
    Creates a form that allows marking a :class:`Solucion` as rejected
    """
    class Meta:
        model = Solucion
        fields = ('rechazada', )

    rechazada = forms.BooleanField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        if 'initial' not in kwargs:
            kwargs['initial'] = {'rechazada': True}
        else:
            kwargs['initial']['rechazada'] = True
        super(SolucionRechazadaForm, self).__init__(*args, **kwargs)
        self.helper.add_input(
            Submit(
                'submit',
                _('Rechazar Solución'),
                css_class='btn-danger btn-block'
            ))

class QuejaDepartamentoForm(forms.Form):
    """
    Builds a form that allows specifying a :class:`Departamento`
    """
    
    area = forms.ModelChoiceField(
        queryset = Departamento.objects.all()
    )  

    def __init__(self, *args, **kwargs):
        super(QuejaDepartamentoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.html5_required = True
        self.field_names = self.fields.keys()
        self.helper.form_method = 'get'
        self.helper.layout = Fieldset(_('Quejas por Area'),
                                      *self.field_names)

    def set_action(self, action):
        self.helper.form_action = action