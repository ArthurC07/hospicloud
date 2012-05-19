# -*- coding: utf-8 -*-
from django.views.generic.base import TemplateView
from statistics.forms import ReporteAnualForm, ReporteMensualForm
import calendar
from django.shortcuts import redirect
from datetime import datetime
from nightingale.models import Admision

class Estadisticas(TemplateView):
    
    template_name = 'estadisticas/index.djhtml'
    
    def get_context_data(self, **kwargs):
        
        context = super(Estadisticas, self).get_context_data(**kwargs)
        context['formulario_anual'] = ReporteAnualForm()
        return context

class Atencion(object):
    
    def calcular_meses(self, context, admisiones):
        
        dict_mes = dict((k,v) for k,v in enumerate(calendar.month_abbr))
        calc_mes = lambda m: (m, admisiones.filter(momento__month=m).count())
        context['meses'] = dict()
        parejas = map(calc_mes, range(1, 13))
        for pareja in parejas:
            mes = dict_mes[pareja[0]]
            context['meses'][mes] = pareja[1]
        
        return ','.join('[{0}, {1}]'.format(p[0], p[1]) for p in parejas)

class AtencionAdulto(TemplateView, Atencion):
    
    template_name = 'estadisticas/atencion_adulto.djhtml'
    
    def get_context_data(self, **kwargs):
        
        context = super(AtencionAdulto, self).get_context_data(**kwargs)
        form = ReporteAnualForm(self.request.GET)
        if not form.is_valid():
            redirect('admision-estadisticas')
        anio = form.cleaned_data['anio']
        # obtener la fecha de nacimiento máxima
        edad_min = datetime(anio - 18, 12, 31)
        admisiones = Admision.objects.filter(
                                momento__year=anio,
                                paciente__nacimiento__lte=edad_min)
        
        context['puntos'] = self.calcular_meses(context, admisiones)
        
        return context

class AtencionInfantil(TemplateView, Atencion):
    
    template_name = 'estadisticas/atencion_infantil.djhtml'
    
    def get_context_data(self, **kwargs):
        
        context = super(AtencionInfantil, self).get_context_data(**kwargs)
        form = ReporteAnualForm(self.request.GET)
        if not form.is_valid():
            redirect('admision-estadisticas')
        anio = form.cleaned_data['anio']
        # obtener la fecha de nacimiento mínima
        edad_min = datetime(anio - 18, 12, 31)
        admisiones = Admision.objects.filter(
                                momento__year=anio,
                                paciente__nacimiento__gte=edad_min)
        
        context['puntos'] = self.calcular_meses(context, admisiones)
        
        return context

class Productividad(TemplateView):
    
    template_name = 'estadisticas/productividad.djhtml'
    
    def get_context_data(self, **kwargs):
        
        context = super(Productividad, self).get_context_data(**kwargs)
        form = ReporteMensualForm(self.request.GET)
        if not form.is_valid():
            redirect('admision-estadisticas')
        anio = form.cleaned_data['anio']
        mes = form.cleaned_data['mes']
        # obtener la fecha de nacimiento máxima
        edad_min = datetime(anio - 18, 12, 31)
        
        context['adultos_m'] = Admision.objects.filter(
                                momento__year=anio,
                                momento__month=mes,
                                paciente__nacimiento__lte=edad_min,
                                paciente__sexo='M').count()
        context['adultos_f'] = Admision.objects.filter(
                                momento__year=anio,
                                momento__month=mes,
                                paciente__nacimiento__lte=edad_min,
                                paciente__sexo='F').count()
        context['adultos'] = Admision.objects.filter(
                                momento__year=anio,
                                momento__month=mes,
                                paciente__nacimiento__lte=edad_min).count()
        
        context['infantes_m'] = Admision.objects.filter(
                                momento__year=anio,
                                momento__month=mes,
                                paciente__nacimiento__gte=edad_min,
                                sexo='M').count()
        context['infantes_f'] = Admision.objects.filter(
                                momento__year=anio,
                                momento__month=mes,
                                paciente__nacimiento__gte=edad_min,
                                paciente__sexo='F').count()
        context['adultos'] = Admision.objects.filter(
                                momento__year=anio,
                                momento__month=mes,
                                paciente__nacimiento__lte=edad_min).count()
        
        context['neonatos_m'] = Admision.objects.filter(
                                momento__year=anio,
                                momento__month=mes,
                                neonato=True,
                                sexo='M').count()
        context['neonatos_f'] = Admision.objects.filter(
                                momento__year=anio,
                                momento__month=mes,
                                neonato=True,
                                paciente__sexo='F').count()
        
        context['neonatos'] = Admision.objects.filter(
                                momento__year=anio,
                                momento__month=mes,
                                neonato=True).count()
        
        context['admisiones'] = Admision.objects.filter(
                                momento__year=anio,
                                momento__month=mes,
                                neonato=True).count()
        
        return context

class IngresosHospitalarios(TemplateView, Atencion):
    
    template_name = 'estadisticas/ingresos_hospitalarios.djhtml'
    
    def get_context_data(self, **kwargs):
        
        context = super(IngresosHospitalarios, self).get_context_data(**kwargs)
        form = ReporteAnualForm(self.request.GET)
        if not form.is_valid():
            redirect('admision-estadisticas')
        anio = form.cleaned_data['anio']
        # obtener la fecha de nacimiento mínima
        admisiones = Admision.objects.filter(
                                momento__year=anio)
        
        context['puntos'] = self.calcular_meses(context, admisiones)
        
        return context
