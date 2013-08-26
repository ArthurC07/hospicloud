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

from persona.models import (Persona, Fisico, EstiloVida, Antecedente,
    AntecedenteFamiliar, AntecedenteObstetrico, AntecedenteQuirurgico)
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Fieldset

class FieldSetFormMixin(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FieldSetFormMixin, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.html5_required = True
        self.field_names = self.fields.keys()
        self.helper.add_input(Submit('submit', 'Guardar'))

class DateWidget(forms.DateInput):

    """Permite mostrar un input preparado para fecha y hora utilizando
    JQuery UI DateTimePicker"""

    def __init__(self, attrs=None):
        super(DateWidget, self).__init__(attrs)
        if attrs is not None:
            self.attrs = attrs.copy()
        else:
            self.attrs = {'class': 'datepicker'}

        if not 'format' in self.attrs:
            self.attrs['format'] = '%d/%m/%Y'

class DateTimeWidget(forms.DateTimeInput):
    
    """Permite mostrar un input preparado para fecha y hora utilizando
    JQuery UI DateTimePicker"""
    
    class Media:
        js = ('js/jquery-ui-timepicker.js',)
    
    def __init__(self, attrs=None):
        super(DateTimeWidget, self).__init__(attrs)
        if attrs is not None:
            self.attrs = attrs.copy()
        else:
            self.attrs = {'class': 'datetimepicker'}
            
        if not 'format' in self.attrs:
            self.attrs['format'] = '%d/%m/%Y %H:%M'

class PersonaForm(forms.ModelForm):
    
    """Permite mostrar una interfaz para capturar los datos de una
    :class:`Persona`"""
    
    class Meta:
        
        model = Persona
    
    nacimiento = forms.DateTimeField(widget=forms.DateInput(
                    attrs={'class': 'datepicker' }, format='%d/%m/%Y'),
                 input_formats=('%d/%m/%Y',))
    
    def __init__(self, *args, **kwargs):
        
        super(PersonaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.html5_required = True
        self.field_names = self.fields.keys()
        self.helper.add_input(Submit('submit', 'Guardar'))
        self.helper.layout = Fieldset(u'Agregar Persona', *self.field_names)

class BasePersonaForm(forms.ModelForm):
    
    """Permite editar la información que depende de una :class:`Persona`"""

    persona = forms.ModelChoiceField(label="",
                                  queryset=Persona.objects.all(),
                                  widget=forms.HiddenInput())
    
    def __init__(self, *args, **kwargs):
        
        super(BasePersonaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.html5_required = True
        self.field_names = self.fields.keys()
        self.helper.add_input(Submit('submit', 'Guardar'))

class FisicoForm(BasePersonaForm):
    
    """Permite editar :class:`Fisico`"""

    class Meta:
        
        model = Fisico
    
    def __init__(self, *args, **kwargs):
        
        super(FisicoForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Editar Fisico', *self.field_names)

class EstiloVidaForm(BasePersonaForm):
    
    """Permite editar :class:`EstiloVida`"""
    
    class Meta:
        
        model = EstiloVida
    
    def __init__(self, *args, **kwargs):
        
        super(FisicoForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Editar Fisico', *self.field_names)

class AntecedenteForm(BasePersonaForm):
    
    """Permite editar :class:`Antecedente`"""
    
    class Meta:
        
        model = Antecedente
    
    def __init__(self, *args, **kwargs):
        
        super(AntecedenteForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Editar Fisico', *self.field_names)

class AntecedenteFamiliarForm(BasePersonaForm):
    
    """Permite editar :class:`AntecedenteFamiliar`"""
    
    class Meta:
        
        model = AntecedenteFamiliar
    
    def __init__(self, *args, **kwargs):
        
        super(AntecedenteFamiliarForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Editar Antecedentes Familiares',
                                      *self.field_names)

class AntecedenteObstetricoForm(BasePersonaForm):
    
    """Permite editar :class:`AntecedenteObstetrico`"""
    
    class Meta:
        
        model = AntecedenteObstetrico

    def __init__(self, *args, **kwargs):
        
        super(AntecedenteObstetricoForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Editar Antecedentes Obstetricos',
                                      *self.field_names)

class AntecedenteQuirurgicoForm(BasePersonaForm):
    
    """Permite editar :class:`AntecedenteQuirurgico`"""
    
    class Meta:
        
        model = AntecedenteQuirurgico
    
    fecha = forms.DateTimeField(widget=forms.DateInput(
                    attrs={'class': 'datepicker' }, format='%d/%m/%Y'),
                 input_formats=('%d/%m/%Y',))
    
    def __init__(self, *args, **kwargs):
        
        super(AntecedenteQuirurgicoForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Agregar Antecendete Quirúgico',
                                      *self.field_names)

class PersonaSearchForm(forms.Form):
    
    query = forms.CharField()
    
    def __init__(self, *args, **kwargs):
        
        super(PersonaSearchForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.html5_required = True
        self.field_names = self.fields.keys()
        self.helper.add_input(Submit('submit', 'Buscar'))
        self.helper.layout = Fieldset(u'Buscar Persona', *self.field_names)
