# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.db.models.query_utils import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, UpdateView, DetailView, CreateView
from library.protected import LoginRequiredView
from nightingale.forms import IngresarForm, CargoForm
from nightingale.models import Cargo
from spital.models import Admision

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
            context['promedio'] = sum(a.tiempo_ahora()
                           for a in admisiones) / self.queryset.count()
        
        context['puntos'] = '[0 , 0],' + u','.join('[{0}, {1}]'.format(n + 1,
                                          admisiones[n].tiempo_ahora())
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
        
        return HttpResponseRedirect(self.get_success_url())

class CargoCreateView(BaseCreateView):
    
    """Permite crear un :class:`Examen` a una :class:`Persona`"""
    
    model = Cargo
    form_class = CargoForm
    template_name = 'enfermeria/cargo_create.djhtml'
