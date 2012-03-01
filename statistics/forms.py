# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation.trans_null import _

class ReporteAnualForm(forms.Form):
    
    anio = forms.IntegerField(label=_(u'Año'))

class ReporteMensualForm(forms.Form):
    
    anio = forms.IntegerField(label=_(u'Año'))
    mes = forms.IntegerField()
