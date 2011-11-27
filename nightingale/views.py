# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.db.models.query_utils import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, UpdateView, DetailView, CreateView
from library.protected import LoginRequiredView
from nightingale.forms import (IngresarForm, CargoForm, EvolucionForm, 
    GlucometriaForm, IngestaForm, ExcretaForm, NotaEnfermeriaForm,
    OrdenMedicaForm, SignoVitalForm)
from nightingale.models import (Cargo, Evolucion, Glucometria, Ingesta, Excreta,
    NotaEnfermeria, OrdenMedica, SignoVital)
from spital.models import Admision
from django.contrib import messages

class NightingaleIndexView(ListView, LoginRequiredView):
    
    queryset = Admision.objects.filter(Q(estado='H'))
    context_object_name = 'admitidos'
    template_name = 'enfermeria/index.djhtml'
    
    def get_context_data(self, **kwargs):
        
        context = super(NightingaleIndexView, self).get_context_data(**kwargs)
        
        admisiones = self.queryset.all()
        context['hospitalizados'] = Admision.objects.filter(Q(estado='I'))
        if self.queryset.count() == 0:
            context['promedio'] = 0
        else:
            context['promedio'] = sum(a.tiempo_hospitalizacion()
                           for a in admisiones) / self.queryset.count()
        
        context['puntos'] = '[0 , 0],' + u','.join('[{0}, {1}]'.format(n + 1,
                                          admisiones[n].tiempo_hospitalizacion())
                      for n in range(self.queryset.count()))
        
        return context

class IngresarView(UpdateView, LoginRequiredView):
    
    model = Admision
    form_class = IngresarForm
    template_name = 'enfermeria/ingresar.djhtml'
    
    def get_success_url(self):
        
        self.object.ingresar()
        return reverse('nightingale-view-id', args=[self.object.id])

class NightingaleDetailView(DetailView, LoginRequiredView):
    
    model = Admision
    template_name = 'enfermeria/nightingale_detail.djhtml'

class SignosDetailView(DetailView, LoginRequiredView):
    
    model = Admision
    template_name = 'enfermeria/signos_grafico.djhtml'
    
    def get_context_data(self, **kwargs):
        
        context = super(SignosDetailView, self).get_context_data(**kwargs)
        signos = self.object.signos_vitales
        if self.object.signos_vitales.count() == 0:
            context['temp_promedio'] = 0
        else:
            context['temp_promedio'] = self.object.temperatura_promedio
        
        context['temperatura'] = '[0 , 0],' + u','.join('[{0}, {1}]'.format(n + 1, signos.all()[n].temperatura) for n in range(signos.count()))
        
        return context

class BaseCreateView(CreateView, LoginRequiredView):
    
    """Permite crear llenar el formulario de una clase que requiera
    :class:`Admision`es de manera previa - DRY"""
    
    def get_context_data(self, **kwargs):
        
        context = super(BaseCreateView, self).get_context_data(**kwargs)
        context['admision'] = self.admision
        return context
    
    def get_form_kwargs(self):
        
        kwargs = super(BaseCreateView, self).get_form_kwargs()
        kwargs.update({ 'initial':{'admision':self.admision.id}})
        return kwargs
    
    def dispatch(self, *args, **kwargs):
        
        self.admision = get_object_or_404(Admision, pk=kwargs['admision'])
        return super(BaseCreateView, self).dispatch(*args, **kwargs)
    
    def form_valid(self, form):
        
        self.object = form.save(commit=False)
        self.object.admision = self.admision
        self.object.save()
        
        messages.info(self.request, u"Hospitalización Actualizada")
        
        return HttpResponseRedirect(self.get_success_url())

class CargoCreateView(BaseCreateView):
    
    """Permite crear un :class:`Examen` a una :class:`Persona`"""
    
    model = Cargo
    form_class = CargoForm
    template_name = 'enfermeria/cargo_create.djhtml'

class EvolucionCreateView(BaseCreateView):
    
    """Permite crear un :class:`Examen` a una :class:`Persona`"""
    
    model = Evolucion
    form_class = EvolucionForm
    template_name = 'enfermeria/evolucion_create.djhtml'

class GlucometriaCreateView(BaseCreateView):
    
    """Permite crear un :class:`Examen` a una :class:`Persona`"""
    
    model = Glucometria
    form_class = GlucometriaForm
    template_name = 'enfermeria/glucometria_create.djhtml'

class IngestaCreateView(BaseCreateView):
    
    """Permite crear un :class:`Examen` a una :class:`Persona`"""
    
    model = Ingesta
    form_class = IngestaForm
    template_name = 'enfermeria/ingesta_create.djhtml'

class ExcretaCreateView(BaseCreateView):
    
    """Permite crear un :class:`Examen` a una :class:`Persona`"""
    
    model = Excreta
    form_class = ExcretaForm
    template_name = 'enfermeria/excreta_create.djhtml'

class NotaCreateView(BaseCreateView):
    
    """Permite crear un :class:`Examen` a una :class:`Persona`"""
    
    model = NotaEnfermeria
    form_class = NotaEnfermeriaForm
    template_name = 'enfermeria/nota_create.djhtml'

class OrdenCreateView(BaseCreateView):
    
    """Permite crear un :class:`Examen` a una :class:`Persona`"""
    
    model = OrdenMedica
    form_class = OrdenMedicaForm
    template_name = 'enfermeria/orden_create.djhtml'

class SignoVitalCreateView(BaseCreateView):
    
    """Permite crear un :class:`Examen` a una :class:`Persona`"""
    
    model = SignoVital
    form_class = SignoVitalForm
    template_name = 'enfermeria/signo_create.djhtml'
