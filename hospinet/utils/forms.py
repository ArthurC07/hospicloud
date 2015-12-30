# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Fieldset
from django import forms
from django.utils.translation import ugettext_lazy as _


class FieldSetFormMixin(forms.Form):
    def __init__(self, *args, **kwargs):
        super(FieldSetFormMixin, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.html5_required = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-4'
        self.helper.field_class = 'col-md-7'
        self.field_names = self.fields.keys()


class FieldSetModelFormMixinNoButton(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FieldSetModelFormMixinNoButton, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.html5_required = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-4'
        self.helper.field_class = 'col-md-7'
        self.field_names = self.fields.keys()


class FieldSetModelFormMixin(FieldSetModelFormMixinNoButton):
    def __init__(self, *args, **kwargs):
        super(FieldSetModelFormMixin, self).__init__(*args, **kwargs)
        self.helper.add_input(Submit('submit', _('Guardar')))


class DateWidget(forms.DateInput):
    """Permite mostrar un input preparado para fecha y hora utilizando
    JQuery UI DatePicker"""

    def __init__(self, attrs=None):
        super(DateWidget, self).__init__(attrs)
        if attrs is not None:
            self.attrs = attrs.copy()
        else:
            self.attrs = {'class': 'datepicker'}

        if 'format' not in self.attrs:
            self.attrs['format'] = '%d/%m/%Y'


class FutureDateWidget(forms.DateInput):
    """Permite mostrar un input preparado para fecha y hora utilizando
    JQuery UI DatePicker"""

    def __init__(self, attrs=None):
        super(FutureDateWidget, self).__init__(attrs)
        if attrs is not None:
            self.attrs = attrs.copy()
        else:
            self.attrs = {'class': 'future-datepicker'}

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

        if 'format' not in self.attrs:
            self.attrs['format'] = '%d/%m/%Y %H:%M'


class PeriodoForm(forms.Form):
    inicio = forms.DateTimeField(widget=DateTimeWidget)

    fin = forms.DateTimeField(widget=DateTimeWidget)

    def __init__(self, *args, **kwargs):
        super(PeriodoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.html5_required = True
        self.field_names = self.fields.keys()
        self.helper.add_input(Submit('submit', 'Mostrar'))
        self.helper.form_method = 'get'
        self.helper.layout = Fieldset(_('Por Periodo'), *self.field_names)

    def set_legend(self, text):
        self.helper.layout = Fieldset(text, *self.field_names)

    def set_action(self, action):
        self.helper.form_action = action
