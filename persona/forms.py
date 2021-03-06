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

from crispy_forms.layout import Submit, Fieldset
from django import forms
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from hospinet.utils.forms import FieldSetModelFormMixin, DateWidget, \
    DateTimeWidget, FieldSetFormMixin, FutureDateWidget, \
    FieldSetModelFormMixinNoButton
from persona.models import Persona, Fisico, EstiloVida, Antecedente, \
    AntecedenteFamiliar, AntecedenteObstetrico, AntecedenteQuirurgico, \
    Empleador, Empleo, HistoriaFisica


class PersonaForm(FieldSetModelFormMixin):
    """Permite mostrar una interfaz para capturar los datos de una
    :class:`Persona`"""

    class Meta:
        model = Persona
        exclude = ('duplicado',)

    class Media:
        js = (
            'http://ajax.aspnetcdn.com/ajax/jquery.validate/1.14.0/jquery.validate.min.js',
            'js/persona.validator.js',
        )

    nacimiento = forms.DateField(widget=DateWidget(), required=True,
                                 initial=timezone.now)
    domicilio = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super(PersonaForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(_('Agregar Persona'), *self.field_names)
        self.helper.form_id = "persona_form"


class BasePersonaForm(FieldSetModelFormMixin):
    """Permite editar la información que depende de una :class:`Persona`"""

    persona = forms.ModelChoiceField(
        queryset=Persona.objects.all(),
        widget=forms.HiddenInput()
    )


class FisicoForm(BasePersonaForm):
    """Permite editar :class:`Fisico`"""

    class Meta:
        model = Fisico
        exclude = ('bmi', 'bmr',)

    def __init__(self, *args, **kwargs):
        super(FisicoForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(_('Editar Fisico'), *self.field_names)


class EstiloVidaForm(BasePersonaForm):
    """Permite editar :class:`EstiloVida`"""

    class Meta:
        model = EstiloVida
        exclude = ('cantidad',)

    def __init__(self, *args, **kwargs):
        super(EstiloVidaForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(_('Editar Estilo de Vida'),
                                      *self.field_names)


class AntecedenteForm(BasePersonaForm):
    """Permite editar :class:`Antecedente`"""

    class Meta:
        model = Antecedente
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(AntecedenteForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(_('Editar Antecedentes Personales'),
                                      *self.field_names)


class AntecedenteFamiliarForm(BasePersonaForm):
    """Permite editar :class:`AntecedenteFamiliar`"""

    class Meta:
        model = AntecedenteFamiliar
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(AntecedenteFamiliarForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(
            _('Editar Antecedentes Patológicos Familiares'),
            *self.field_names)


class AntecedenteObstetricoForm(BasePersonaForm):
    """Permite editar :class:`AntecedenteObstetrico`"""

    class Meta:
        model = AntecedenteObstetrico
        fields = '__all__'

    menarca = forms.DateField(widget=DateWidget(), required=False,
                              initial=timezone.now)
    ultimo_periodo = forms.DateField(widget=DateWidget(), required=False,
                                     initial=timezone.now)

    def __init__(self, *args, **kwargs):
        super(AntecedenteObstetricoForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(_('Editar Antecedentes Obstétricos'),
                                      *self.field_names)


class AntecedenteQuirurgicoForm(BasePersonaForm):
    """Permite editar :class:`AntecedenteQuirurgico`"""

    class Meta:
        model = AntecedenteQuirurgico
        fields = '__all__'

    fecha = forms.DateTimeField(widget=DateTimeWidget(), required=False,
                                initial=timezone.now)

    def __init__(self, *args, **kwargs):
        super(AntecedenteQuirurgicoForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(_('Antecedente Quirúrgico'),
                                      *self.field_names)


class PersonaSearchForm(FieldSetFormMixin):
    query = forms.CharField(label=_("Nombre o Identidad"))

    def __init__(self, *args, **kwargs):
        super(PersonaSearchForm, self).__init__(*args, **kwargs)
        self.helper.add_input(Submit('submit', 'Buscar'))
        self.helper.layout = Fieldset(_('Buscar Persona'), *self.field_names)
        self.helper.form_method = 'GET'
        self.helper.form_action = 'persona-search'


class PersonaAdvancedSearchForm(FieldSetFormMixin):
    """
    Allows searching for a :class:`Persona` by filtering both nombre and
    apellido
    """
    nombre = forms.CharField()
    apellidos = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(PersonaAdvancedSearchForm, self).__init__(*args, **kwargs)
        self.helper.add_input(Submit('submit', 'Buscar'))
        self.helper.layout = Fieldset(_('Búsqueda Avanzada de Persona'),
                                      *self.field_names)
        self.helper.form_method = 'GET'
        self.helper.form_action = 'persona-advanced-search'


class EmpleadorForm(FieldSetModelFormMixin):
    class Meta:
        model = Empleador
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(EmpleadorForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(_('Datos del Empleador'),
                                      *self.field_names)


class EmpleoForm(BasePersonaForm):
    class Meta:
        model = Empleo
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(EmpleoForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(_('Datos de Empleo'), *self.field_names)


class PersonaDuplicateForm(FieldSetModelFormMixin):
    class Meta:
        model = Persona
        fields = ('duplicado',)

    def __init__(self, *args, **kwargs):
        super(PersonaDuplicateForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(_('Reportar Persona Duplicada'),
                                      *self.field_names)


class PersonaRTNForm(FieldSetModelFormMixin):
    class Meta:
        model = Persona
        fields = ('rtn',)

    def __init__(self, *args, **kwargs):
        super(PersonaRTNForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(_('Actualizar RTN de la Persona'),
                                      *self.field_names)


class HistoriaFisicaForm(BasePersonaForm):
    """
    Builds a form that allows for :class:`HistoriaFisica` adding and editing
    """
    class Meta:
        model = HistoriaFisica
        exclude = ('bmi', 'bmr', 'presion_arterial_media')

    def __init__(self, *args, **kwargs):
        super(HistoriaFisicaForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(_('Agregar Historia Física-Metabólica'),
                                      *self.field_names)
