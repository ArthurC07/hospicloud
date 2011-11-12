# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic.edit import CreateView
from laboratory.models import Persona
from library.protected import LoginRequiredView
from persona.views import PersonaCreateView
from spital.forms import AdmisionForm
from spital.models import Admision

class PersonaAdmisionCreateView(PersonaCreateView):
    
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
        self.object.save()
        
        return HttpResponseRedirect(self.get_success_url())
