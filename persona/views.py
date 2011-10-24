# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, DetailView, UpdateView
from mixins import LoginRequiredView
from persona.forms import PersonaForm, FisicoForm, EstiloVidaForm
from persona.models import Persona, Fisico, EstiloVida

class PersonaDetailView(DetailView, LoginRequiredView):
    
    """Permite mostrar los datos de una persona"""
    
    context_object_name = 'persona'
    model = Persona
    template_name = 'persona/persona_detail.djhtml'

class PersonaCreateView(CreateView, LoginRequiredView):
    
    """Permite ingresar personas a la aplicación""" 
    
    form_class = PersonaForm
    template_name = 'persona/nuevo.djhtml'
    
    def form_valid(self, form):
        
        super(PersonaCreateView, self).form_valid(form)
        fisico = Fisico(persona=self.object)
        fisico.save()
        estilo_vida = EstiloVida(persona=self.object)
        estilo_vida.save()
        
        return HttpResponseRedirect(self.get_success_url())

class PersonaUpdateView(UpdateView, LoginRequiredView):
    
    """Permite actualizar los datos de una :class:`Persona`"""
    
    model = Persona
    form_class = PersonaForm
    template_name = 'persona/persona_update.djhtml'

class FisicoUpdateView(UpdateView, LoginRequiredView):
    
    model = Fisico
    form_class = FisicoForm
    template_name = 'persona/fisico_update.djhtml'

class EstiloVidaUpdateView(UpdateView, LoginRequiredView):
    
    model = EstiloVida
    form_class = EstiloVidaForm
    template_name = 'persona/estilo_vida_update.djhtml'
