# -*- coding: utf-8 -*-
from clinique.forms import (PacienteForm, TransaccionForm, CitaForm,
    ConsultorioForm, ConsultaForm, RecetaForm, HistoriaClinicaForm,
    OptometriaForm)
from clinique.models import (Consultorio, Paciente, Transaccion, Cita,
    Esperador, Consulta, Receta, HistoriaClinica, Optometria)
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, DetailView, CreateView, ListView
from library.protected import LoginRequiredView
from persona.forms import PersonaForm
from persona.models import Persona
from persona.views import PersonaCreateView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.base import RedirectView

class ConsultorioIndex(TemplateView):
    
    template_name = "consultorio/index.html"

class ConsultorioCreateView(CreateView, LoginRequiredView):
    
    """Permite crear un :class:`Consultorio` para el usuario actual en caso de
    que el mismo sea un doctor"""
    
    model = Consultorio
    form_class = ConsultorioForm
    template_name = "consultorio/consultorio_create.html"
    
    def form_valid(self, form):
        
        self.object = form.save(commit=False)
        self.object.doctor = self.request.user.profile
        self.object.save()
        
        return HttpResponseRedirect(self.get_success_url())

class ConsultorioDetailView(DetailView, LoginRequiredView):
    
    """Permite mostrar los detalles de un :class:`Consultorio`
    
    En especifico se encarga de funciones como listar los pacientes, mostrar
    el estado de las cuentas, mostrar la sala de espera
    """
    
    template_name = 'consultorio/consultorio_detail.html'
    model = Consultorio
    context_object_name = 'consultorio'
    slug_field = 'uuid'

class BaseCreateView(CreateView, LoginRequiredView):
    
    """Permite llenar el formulario de una clase que requiera
    :class:`Consultorio`s de manera previa - DRY"""
    
    def get_context_data(self, **kwargs):
        
        context = super(BaseCreateView, self).get_context_data(**kwargs)
        context['consultorio'] = self.consultorio
        return context
    
    def get_form_kwargs(self):
        
        kwargs = super(BaseCreateView, self).get_form_kwargs()
        kwargs.update({ 'initial':{'consultorio':self.consultorio.id}})
        return kwargs
    
    def dispatch(self, *args, **kwargs):
        
        self.consultorio = get_object_or_404(Consultorio, pk=kwargs['consultorio'])
        return super(BaseCreateView, self).dispatch(*args, **kwargs)
    
    def form_valid(self, form):
        
        self.object = form.save(commit=False)
        self.object.consultorio = self.consultorio
        self.object.save()
        
        return HttpResponseRedirect(self.get_success_url())

class SecretariaCreateView(BaseCreateView):
    
    """Permite crear un :class:`User` que actuará como Secretaria(o) del
    :class:`Usuario` doctor que es dueño del :class:`Consultorio`"""
    
    model = User
    form_class = UserCreationForm
    template_name = 'consultorio/secretaria_create.html'
    
    def form_valid(self, form):
        
        self.object = form.save()
        self.consultorio.secretaria = self.object.profile
        perfil_doctor = self.consultorio.doctor
        self.object.profile.suscripcion = perfil_doctor.suscripcion
        self.object.profile.suscriptor = perfil_doctor.user
        self.consultorio.save()
        self.object.save()
        
        return HttpResponseRedirect(self.get_success_url())
    
    def get_success_url(self):
        
        return reverse('consultorio-view', args=[self.consultorio.uuid])

class PersonaPacienteCreateView(PersonaCreateView):
    
    template_name = 'persona/persona_nuevo.html'
    
    def get_success_url(self):
        
        return reverse('paciente-agregar', args=[self.object.id])

class PacientePreCreateView(TemplateView):
    
    template_name = 'consultorio/paciente_agregar.html'
    
    def dispatch(self, *args, **kwargs):
        
        self.consultorio = get_object_or_404(Consultorio, pk=kwargs['consultorio'])
        return super(PacientePreCreateView, self).dispatch(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        
        context = super(PacientePreCreateView, self).get_context_data()
        context['consultorio'] = self.consultorio
        context['persona_form'] = PersonaForm()
        return context

class PersonaConsultorioCreateView(PersonaCreateView):
    
    template_name = 'persona/persona_nuevo.html'
    
    def dispatch(self, *args, **kwargs):
        
        self.consultorio = get_object_or_404(Consultorio, pk=kwargs['consultorio'])
        return super(PersonaConsultorioCreateView, self).dispatch(*args, **kwargs)
    
    def get_success_url(self):
        
        return reverse('consultorio-paciente-agregar', args=[self.consultorio.id, self.object.id])

class PacienteCreateView(RedirectView):
    
    """Crea un :class:`Paciente` para el :class:`Consultorio` especificado y
    redirige hacia el recien creado"""
    
    model = Paciente
    form_class = PacienteForm
    template_name = "consultorio/paciente_create.html"
    
    def dispatch(self, *args, **kwargs):
        
        self.consultorio = get_object_or_404(Consultorio, pk=kwargs['consultorio'])
        self.persona = get_object_or_404(Persona, pk=kwargs['persona'])
        del kwargs['persona']
        del kwargs['consultorio']
        self.paciente = Paciente(consultorio=self.consultorio,
                                     persona=self.persona)
        self.paciente.save()
        
        return super(PacienteCreateView, self).dispatch(*args, **kwargs)
    
    def get_redirect_url(self):
        
        return self.paciente.get_absolute_url()

class PacienteDetailView(DetailView, LoginRequiredView):
    
    """Permite al :class:`User` doctor o secretaria ver los detalles de una
    :class:`Persona` que tenga como paciente"""
    
    model = Paciente
    template_name = 'consultorio/paciente_detail.html'
    context_object_name = 'paciente'
    slug_field = 'uuid'

class TransaccionCreateView(BaseCreateView):
    
    """Permite agregar una :class:`Transaccion` entre un :class:`Consultorio`
    y un :class:`Paciente`"""
    
    model = Transaccion
    form_class = TransaccionForm
    template_name = 'consultorio/transaccion.html'
    
    def dispatch(self, *args, **kwargs):
        
        self.paciente = get_object_or_404(Paciente, pk=kwargs['paciente'])
        return super(TransaccionCreateView, self).dispatch(*args, **kwargs)
    
    def get_form_kwargs(self):
        
        kwargs = super(TransaccionCreateView, self).get_form_kwargs()
        kwargs.update({'initial' : {'paciente' : self.paciente.id}})
        return kwargs
    
    def form_valid(self, form):
        
        self.object = form.save(commit=False)
        self.object.persona = self.paciente
        self.object.save()
        
        return HttpResponseRedirect(self.get_success_url())

class AgregarCitaCreateView(BaseCreateView):
    
    """Permite agregar una :class:`Cita` al consultorio"""
    
    model = Cita
    form_class = CitaForm
    template_name = "consultorio/paciente_create.html"

class ConsultorioPacientes(ListView, LoginRequiredView):

    model = Paciente
    template_name = 'consultorio/pacientes_list.html'
    
    def dispatch(self, *args, **kwargs):
        
        self.consultorio = get_object_or_404(Consultorio, pk=kwargs['paciente'])
        return super(ConsultorioPacientes, self).dispatch(*args, **kwargs)

class EsperaPacientes(ListView, LoginRequiredView):

    """Muestra la lista de :class:`Paciente` que se encuentran actualmente en
    la Sala de Espera del :class:`Consultorio`"""

    model = Esperador
    template_name = 'consultorio/espera_list.html'
    context_object_name = 'pacientes'
    
    def dispatch(self, *args, **kwargs):
        
        self.consultorio = get_object_or_404(Consultorio, pk=kwargs['consultorio'])
        return super(ConsultorioPacientes, self).dispatch(*args, **kwargs)

    def get_queryset(self):

        return Esperador.objects.filter(consultorio=self.Consultorio, atendido=False)

class EsperadorAgregarView(RedirectView, LoginRequiredView):
    
    """Permite agregar un :class:`Paciente` a la sala de espera del consultorio en
    el cual se esta trabajando actualmente"""
    
    permanent = False
    
    def get_redirect_url(self, **kwargs):
        
        paciente  = get_object_or_404(Paciente, pk=kwargs['paciente'])
        esperador = Esperador()
        esperador.consultorio = paciente.consultorio
        esperador.paciente = paciente
        esperador.save()
        messages.info(self.request, u'¡Se agrego al paciente a la sala de espera!')
        return reverse('consultorio-view', args=[consultorio.uuid])

class EsperadorAtendido(RedirectView, LoginRequiredView):

    permanent = False

    def get_redirect_url(self, **kwargs):

        esperador = get_object_or_404(Esperador, pk=kwargs['esperador'])
        esperador.atendido = True
        esperador.save()
        messages.info(self.request, u'¡Se marco al Paciente como atendido!')
        return reverse('consultorio-view', args=[esperador.consultorio.uuid])

class PacienteBasecreateView(CreateView, LoginRequiredView):

    def dispatch(self, *args, **kwargs):
        
        self.paciente = get_object_or_404(Paciente, pk=kwargs['paciente'])
        return super(ConsultaCreateView, self).dispatch(*args, **kwargs)
    
    def get_form_kwargs(self):
        
        kwargs = super(ConsultaCreateView, self).get_form_kwargs()
        kwargs.update({'initial' : {'paciente' : self.paciente.id}})
        return kwargs
    
    def form_valid(self, form):
        
        self.object = form.save(commit=False)
        self.object.persona = self.paciente
        self.object.save()
        
        return HttpResponseRedirect(self.get_success_url())

class ConsultaCreateView(PacienteBasecreateView):
    
    """Permite agregar una :class:`Consulta` a un :class:`Paciente`"""

    model = Consulta
    form_class = ConsultaForm
    template_name = 'consultorio/consulta_form.html'

class ConsultaDetailview(DetailView, LoginRequiredView):
    
    model = Consulta
    template_name = 'consultorio/consulta_detail.html'
    context_object_name = 'consulta'

class RecetaCreateView(PacienteBasecreateView):

    model = Receta
    form_class = RecetaForm
    template_name = 'consultorio/receta_create.html'

class RecetaDetailView(DetailView, LoginRequiredView):

    model = Receta
    template_name = 'consultorio/receta_detail.html'
    context_object_name = 'receta'

class OptometriaCreateView(PacienteBasecreateView):

    model = Optometria
    form_class = OptometriaForm
    template_name = 'consultorio/optometria_create.html'

class OptometriaDetailView(DetailView, LoginRequiredView):

    model = Optometria
    template_name = 'consultorio/optometria_detail.html'
    context_object_name = 'Optometria'

class HistoriaClinicaCreateView(PacienteBasecreateView):

    model = HistoriaClinica
    form_class = HistoriaClinicaForm
    template_name = 'Consultorio/historia_clinica_create.html'
