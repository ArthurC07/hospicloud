# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, ListView, TemplateView
from library.protected import LoginRequiredView
from persona.models import Persona
from persona.views import PersonaCreateView
from spital.forms import AdmisionForm
from spital.models import Admision
from django.views.generic.detail import DetailView
from persona.forms import PersonaForm

class AdmisionIndexView(ListView, LoginRequiredView):
    
    context_object_name = 'admisiones'
    model = Admision
    template_name = 'admision/index.djhtml'

class IngresarView(TemplateView):
    
    template_name = 'admision/ingresar.djhtml'
    
    def get_context_data(self, **kwargs):
        
        context = super(IngresarView, self).get_context_data()
        context['persona_form'] = PersonaForm()
        return context

class PersonaAdmisionCreateView(PersonaCreateView):
    
    template_name = 'admision/persona_create.djhtml'
    
    def get_success_url(self):
        
        return reverse('admision-iniciar', args=[self.object.id])

class AdmisionCreateView(CreateView, LoginRequiredView):
    
    model = Admision
    form_class = AdmisionForm
    template_name = 'admision/admision_create.djhtml'
    
    def get_form_kwargs(self):
        
        kwargs = super(AdmisionCreateView, self).get_form_kwargs()
        kwargs.update({ 'initial':{'persona':self.persona.id}})
        return kwargs
    
    def dispatch(self, *args, **kwargs):
        
        self.persona = get_object_or_404(Persona, pk=kwargs['persona'])
        return super(AdmisionCreateView, self).dispatch(*args, **kwargs)
    
    def form_valid(self, form):
        
        self.object = form.save(commit=False)
        self.object.persona = self.persona
        self.object.admitio = self.request.user
        self.object.save()
        
        return HttpResponseRedirect(self.get_success_url())

class AdmisionDetailView(DetailView, LoginRequiredView):
    
    context_object_name = 'admision'
    model = Admision
    template_name = 'admision/admision_detail.djhtml'
