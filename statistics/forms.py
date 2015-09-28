# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation.trans_null import _
from persona.forms import FieldSetFormMixin


class ReporteAnualForm(FieldSetFormMixin):
    anio = forms.IntegerField(label=_(u'Año'))


class ReporteMensualForm(FieldSetFormMixin):
    anio = forms.IntegerField(label=_(u'Año'))
    mes = forms.IntegerField()
