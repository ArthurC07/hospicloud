# Create your views here.
from django.views.generic import (TemplateView, DetailView, CreateView)
from library.protected import LoginRequiredView
from clinique.models import Consultorio, Paciente, Transaccion, Cita
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from clinique.forms import PacienteForm, TransaccionForm, CitaForm #@UnresolvedImport

class ConsultorioIndex(TemplateView):
    
    template_name = "consultorio/index.djhtml"

class ConsultorioDetailView(DetailView, LoginRequiredView):
    
    template_name = 'consultorio/consultorio.djhtml'
    model = Consultorio
    context_object_name = 'consultorio'

class AgregarPacienteCreateView(CreateView, LoginRequiredView):
    
    model = Paciente
    form_class = PacienteForm
    template_name = "consultorio/paciente_create.djhtml"
    
    def dispatch(self, *args, **kwargs):
        
        self.consultorio = get_object_or_404(Consultorio, pk=kwargs['examen'])
        return super(AgregarPacienteCreateView, self).dispatch(*args, **kwargs)
    
    def get_form_kwargs(self):
        
        kwargs = super(AgregarPacienteCreateView, self).get_form_kwargs()
        kwargs.update({'user' : self.request.user})
        return kwargs
    
    def form_valid(self, form):
        
        self.object = form.save(commit=False)
        self.object.consultorio = self.consultorio
        self.object.save()
        
        return HttpResponseRedirect(self.get_success_url())

class PacienteDetailView(DetailView, LoginRequiredView):
    
    model = Paciente
    template_name = 'consultorio/paciente_detail.djhtml'
    context_object_name = 'paciente'

class TransaccionCreateView(CreateView, LoginRequiredView):
    
    model = Transaccion
    form_class = TransaccionForm
    template_name = 'consultorio/transaccion.djhtml'
    
    def dispatch(self, *args, **kwargs):
        
        self.persona = get_object_or_404(Paciente, pk=kwargs['paciente'])
        return super(TransaccionCreateView, self).dispatch(*args, **kwargs)
    
    def get_form_kwargs(self):
        
        kwargs = super(TransaccionCreateView, self).get_form_kwargs()
        kwargs.update({'initial' : {'paciente' : self.paciente.id}})
        return kwargs
    
    def form_valid(self, form):
        
        self.object = form.save(commit=False)
        self.object.persona = self.persona
        self.object.save()
        
        return HttpResponseRedirect(self.get_success_url())

class AgregarCitaCreateView(CreateView, LoginRequiredView):
    
    model = Cita
    form_class = CitaForm
    template_name = "consultorio/paciente_create.djhtml"
    
    def dispatch(self, *args, **kwargs):
        
        self.consultorio = get_object_or_404(Consultorio, pk=kwargs['examen'])
        return super(AgregarCitaCreateView, self).dispatch(*args, **kwargs)
    
    def get_form_kwargs(self):
        
        kwargs = super(AgregarCitaCreateView, self).get_form_kwargs()
        kwargs.update({'initial': {'consultorio' : self.consultorio.id}})
        return kwargs
    
    def form_valid(self, form):
        
        self.object = form.save(commit=False)
        self.object.consultorio = self.consultorio
        self.object.save()
        
        return HttpResponseRedirect(self.get_success_url())

class AgregarVisitanteCreateView(CreateView, LoginRequiredView):
    
    model = Cita
    form_class = CitaForm
    template_name = "consultorio/paciente_create.djhtml"
    
    def dispatch(self, *args, **kwargs):
        
        self.consultorio = get_object_or_404(Consultorio, pk=kwargs['examen'])
        return super(AgregarVisitanteCreateView, self).dispatch(*args, **kwargs)
    
    def get_form_kwargs(self):
        
        kwargs = super(AgregarVisitanteCreateView, self).get_form_kwargs()
        kwargs.update({'initial': {'consultorio' : self.consultorio.id}})
        return kwargs
    
    def form_valid(self, form):
        
        self.object = form.save(commit=False)
        self.object.consultorio = self.consultorio
        self.object.save()
        
        return HttpResponseRedirect(self.get_success_url())
