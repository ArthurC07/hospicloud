# -*- coding: utf-8 -*-
from laboratory.forms import ExamenForm, ImagenForm
from laboratory.models import Examen, Imagen
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, CreateView
from library.protected import LoginRequiredView
from persona.models import Persona
from django.views.generic.base import TemplateView

class ExamenIndexView(TemplateView):
    
    template_name = 'examen/index.djhtml'

class ExamenDetailView(DetailView, LoginRequiredView):
    
    """Permite ver los detalles de un :class:`Examen`"""
    
    context_object_name = 'examen'
    model = Examen
    template_name = 'examen/examen_detail.djhtml'

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
    
    def dispatch(self, *args, **kwargs):
        
        self.persona = get_object_or_404(Persona, pk=kwargs['persona'])
        return super(ExamenCreateView, self).dispatch(*args, **kwargs)
    
    def form_valid(self):
        
        self.object = self.form.save(commit=False)
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
    
    def form_valid(self):
        
        self.object = self.form.save(commit=False)
        self.object.examen = self.examen
        self.object.save()
        
        return HttpResponseRedirect(self.get_success_url())
