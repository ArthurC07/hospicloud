# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import (DetailView, UpdateView, CreateView, ListView,
                                  TemplateView)
from imaging.forms import ExamenForm, ImagenForm, AdjuntoForm, DicomForm
from imaging.models import Examen, Imagen, Adjunto, Dicom, Remision
from library.protected import LoginRequiredView
from persona.forms import PersonaForm
from persona.models import Persona
from persona.views import PersonaCreateView

class ExamenIndexView(ListView):
    
    template_name = 'examen/index.html'
    queryset = Examen.objects.all().order_by('-fecha')[:5]
    context_object_name = 'examenes'

class PersonaExamenCreateView(PersonaCreateView):
    
    template_name = 'persona/persona_nuevo.html'
    
    def get_success_url(self):
        
        return reverse('examen-agregar', args=[self.object.id])

class ExamenPreCreateView(TemplateView):
    
    template_name = 'examen/examen_agregar.html'
    
    def get_context_data(self, **kwargs):
        
        context = super(ExamenPreCreateView, self).get_context_data()
        context['persona_form'] = PersonaForm()
        return context

class ExamenDetailView(DetailView, LoginRequiredView):
    
    """Permite ver los detalles de un :class:`Examen`"""
    
    context_object_name = 'examen'
    model = Examen
    template_name = 'examen/examen_detail.html'
    slug_field = 'uuid'

class ExamenPersonaListView(DetailView, LoginRequiredView):
    
    context_object_name = 'persona'
    model = Persona
    template_name = 'examen/examen_paciente_detail.html'

class ExamenUpdateView(UpdateView, LoginRequiredView):
    
    """Permite actualizar los datos de un :class:`Examen`"""
    
    model = Examen
    form_class = ExamenForm
    template_name = 'examen/examen_update.html'

class ExamenCreateView(CreateView, LoginRequiredView):
    
    """Permite crear un :class:`Examen` a una :class:`Persona`"""
    
    model = Examen
    form_class = ExamenForm
    template_name = 'examen/examen_create.html'
    
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

class ExamenDocBaseCreateView(CreateView, LoginRequiredView):
    
    """Permite crear objetos que pertenecen a un :class:`Examen`"""

    def dispatch(self, *args, **kwargs):
        
        self.examen = get_object_or_404(Examen, pk=kwargs['examen'])
        return super(ExamenDocBaseCreateView, self).dispatch(*args, **kwargs)
    
    def get_form_kwargs(self):
        
        kwargs = super(ExamenDocBaseCreateView, self).get_form_kwargs()
        kwargs.update({ 'initial' : { 'examen' : self.examen.id } })
        return kwargs
    
    def form_valid(self, form):
        
        self.object = form.save(commit=False)
        self.object.examen = self.examen
        self.object.save()
        
        return HttpResponseRedirect(self.get_success_url())

class ImagenCreateView(ExamenDocBaseCreateView):
    
    """Permite crear :class:`Imagen`es a un :class:`Examen`"""
    
    model = Imagen
    form_class = ImagenForm
    template_name = "examen/imagen_create.html"

class AdjuntoCreateView(ExamenDocBaseCreateView):
    
    """Permite crear :class:`Adjunto`s a un :class:`Examen`"""
    
    model = Adjunto
    form_class = AdjuntoForm
    template_name = "examen/adjunto_create.html"

class DicomCreateView(ExamenDocBaseCreateView):
    
    """Permite agregar un archivo :class:`Dicom` a un examen"""
    
    model = Dicom
    form_class = DicomForm
    template_name = "examen/dicom_create.html"
    
    def form_valid(self, form):
        
        self.object = form.save(commit=False)
        self.object.examen = self.examen
        self.object.save()
        self.object.extraer_imagen()
        
        return HttpResponseRedirect(self.get_success_url())

class DicomDetailView(DetailView, LoginRequiredView):
    
    context_object_name = 'dicom'
    model = Dicom
    template_name = "examen/dicom_detail.html"
    slug_field = 'uuid'

class RemisionCreateView(CreateView, LoginRequiredView):

    """Permite recetar un :class:`Examen` a una :class:`Persona"""

    model = Remision
