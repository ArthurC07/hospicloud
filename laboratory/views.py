# -*- coding: utf-8 -*-
from laboratory.forms import ExamenForm, ImagenForm, AdjuntoForm
from laboratory.models import Examen, Imagen, Adjunto
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import (DetailView, UpdateView, CreateView,
                                  TemplateView)
from library.protected import LoginRequiredView
from persona.models import Persona

class ExamenIndexView(TemplateView):
    
    template_name = 'examen/index.djhtml'

class ExamenDetailView(DetailView, LoginRequiredView):
    
    """Permite ver los detalles de un :class:`Examen`"""
    
    context_object_name = 'examen'
    model = Examen
    template_name = 'examen/examen_detail.djhtml'

class ExamenPersonaListView(DetailView, LoginRequiredView):
    
    context_object_name = 'persona'
    model = Persona
    template_name = 'examen/examen_paciente_detail.djhtml'

class ExamenUpdateView(UpdateView, LoginRequiredView):
    
    """Permite actualizar los datos de un :class:`Examen`"""
    
    model = Examen
    form_class = ExamenForm
    template_name = 'examen/examen_update.djhtml'

class ExamenCreateView(CreateView, LoginRequiredView):
    
    """Permite crear un :class:`Examen` a una :class:`Persona`"""
    
    model = Examen
    form_class = ExamenForm
    template_name = 'examen/examen_create.djhtml'
    
    def get_form_kwargs(self):
        
        kwargs = super(ExamenCreateView, self).get_form_kwargs()
        kwargs.update({ 'initial':{'persona':self.persona.id}})
        return kwargs
    
    def dispatch(self, *args, **kwargs):
        
        self.persona = get_object_or_404(Persona, pk=kwargs['persona'])
        return super(ExamenCreateView, self).dispatch(*args, **kwargs)
    
    def form_valid(self, form):
        
        self.object = form.save(commit=False)
        self.object.persona = self.persona
        self.object.save()
        
        return HttpResponseRedirect(self.get_success_url())

class ImagenCreateView(CreateView, LoginRequiredView):
    
    """Permite crear :class:`Imagen`es a un :class:`Examen`"""
    
    model = Imagen
    form_class = ImagenForm
    template_name = "examen/imagen_create.djhtml"
    
    def dispatch(self, *args, **kwargs):
        
        self.examen = get_object_or_404(Examen, pk=kwargs['examen'])
        return super(ExamenCreateView, self).dispatch(*args, **kwargs)
    
    def get_form_kwargs(self):
        
        kwargs = super(ImagenCreateView, self).get_form_kwargs()
        kwargs.update({ 'initial':{'examen':self.examen.id}})
        return kwargs
    
    def form_valid(self, form):
        
        self.object = form.save(commit=False)
        self.object.examen = self.examen
        self.object.save()
        
        return HttpResponseRedirect(self.get_success_url())

class AdjuntoCreateView(CreateView, LoginRequiredView):
    
    """Permite crear :class:`Adjunto`s a un :class:`Examen`"""
    
    model = Adjunto
    form_class = AdjuntoForm
    template_name = "examen/adjunto_create.djhtml"
    
    def dispatch(self, *args, **kwargs):
        
        self.examen = get_object_or_404(Examen, pk=kwargs['examen'])
        return super(ExamenCreateView, self).dispatch(*args, **kwargs)
    
    def get_form_kwargs(self):
        
        kwargs = super(AdjuntoCreateView, self).get_form_kwargs()
        kwargs.update({ 'initial':{'examen':self.examen.id}})
        return kwargs
    
    def form_valid(self, form):
        
        self.object = form.save(commit=False)
        self.object.examen = self.examen
        self.object.save()
        
        return HttpResponseRedirect(self.get_success_url())
