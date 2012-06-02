# -*- coding: utf-8 -*-
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import (CreateView, ListView, TemplateView,
                                  DetailView, RedirectView)
from library.protected import LoginRequiredView
from persona.models import Persona
from persona.views import PersonaCreateView
from spital.forms import AdmisionForm
from spital.models import Admision
from persona.forms import PersonaForm
from django.contrib import messages

class AdmisionIndexView(ListView, LoginRequiredView):
    
    context_object_name = 'admisiones'
    queryset = Admision.objects.filter(~Q(estado='H')&~Q(estado='C')&~Q(estado='I'))
    template_name = 'admision/index.html'
    
    def get_context_data(self, **kwargs):
        
        context = super(AdmisionIndexView, self).get_context_data(**kwargs)
        
        admisiones = self.queryset.all()
        
        if self.queryset.count() == 0:
            context['promedio'] = 0
        else:
            context['promedio'] = sum(a.tiempo_ahora()
                           for a in admisiones) / self.queryset.count()
        
        context['puntos'] = '[0 , 0],' + u','.join('[{0}, {1}]'.format(n + 1,
                                          admisiones[n].tiempo_ahora())
                      for n in range(self.queryset.count()))
        
        return context

class IngresarView(TemplateView):
    
    template_name = 'admision/ingresar.html'
    
    def get_context_data(self, **kwargs):
        
        context = super(IngresarView, self).get_context_data()
        context['persona_form'] = PersonaForm()
        return context

class PersonaAdmisionCreateView(PersonaCreateView):
    
    template_name = 'admision/persona_create.html'
    
    def get_success_url(self):
        
        return reverse('admision-persona-agregar', args=[self.object.id])

class PersonaFiadorCreateView(PersonaCreateView):
    
    template_name = 'admision/admision_fiador.html'
    
    def dispatch(self, *args, **kwargs):
        
        self.admision = get_object_or_404(Admision, pk=kwargs['admision'])
        return super(PersonaFiadorCreateView, self).dispatch(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        
        context = super(PersonaFiadorCreateView, self).get_context_data(**kwargs)
        context['admision'] = self.admision
        context['form'] = PersonaForm()
        return context
    
    def form_valid(self, form):
        
        self.object = form.save()
        self.admision.fiadores.add(self.object)
        self.admision.save()
        messages.info(self.request, u"Agregado un Fiador!")
        
        return HttpResponseRedirect(self.admision.get_absolute_url())

class PersonaReferenciaCreateView(PersonaCreateView):
    
    template_name = 'admision/admision_referencia.html'
    
    def dispatch(self, *args, **kwargs):
        
        self.admision = get_object_or_404(Admision, pk=kwargs['admision'])
        return super(PersonaFiadorCreateView, self).dispatch(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        
        context = super(PersonaReferenciaCreateView, self).get_context_data()
        context['admision'] = self.admision
        context['form'] = PersonaForm()
        return context
    
    def form_valid(self, form):
        
        self.object = form.save()
        self.admision.referencias.add(self.object)
        self.admision.save()
        messages.info(self.request, u"Agregada Referencia!")
        
        return HttpResponseRedirect(self.admision.get_absolute_url())

class ReferenciaAgregarView(RedirectView):
    
    url = '/admision/referencia/agregar'
    
    def get_redirect_url(self, **kwargs):
        
        admision = get_object_or_404(Admision, pk=kwargs['admision'])
        persona = get_object_or_404(Persona, pk=kwargs['persona'])
        admision.referencias.add(persona)
        admision.save()
        return reverse('admision-view-id', args=[admision.id])

class FiadorAgregarView(RedirectView):
    
    url = '/admision/fiador/agregar'
    
    def get_redirect_url(self, **kwargs):
        
        admision = get_object_or_404(Admision, pk=kwargs['admision'])
        persona = get_object_or_404(Persona, pk=kwargs['persona'])
        admision.fiadores.add(persona)
        admision.save()
        return reverse('admision-view-id', args=[admision.id])

class AdmisionCreateView(CreateView, LoginRequiredView):
    
    model = Admision
    form_class = AdmisionForm
    template_name = 'admision/admision_create.html'
    
    def get_form_kwargs(self):
        
        kwargs = super(AdmisionCreateView, self).get_form_kwargs()
        kwargs.update({ 'initial':{'paciente':self.persona.id}})
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
    template_name = 'admision/admision_detail.html'
    slug_field = 'uuid'
    
    def get_object(self):
        
        objeto = super(AdmisionDetailView, self).get_object()
        
        if not objeto.codigo:
            
            objeto.generar_codigo()
        
        if not objeto.qr:
            
            objeto.generar_qr()
        
        objeto.save()
        return objeto

class AutorizarView(RedirectView, LoginRequiredView):
    
    url = '/admision/autorizar'
    permanent = False
    
    def get_redirect_url(self, **kwargs):
        
        admision = get_object_or_404(Admision, pk=kwargs['pk'])
        admision.autorizar()
        messages.info(self.request, u'¡Admision Autorizada!')
        return reverse('admision-view-id', args=[admision.id])

class PagarView(RedirectView, LoginRequiredView):
    
    url = '/admision/hospitalizar'
    permanent = False
    
    def get_redirect_url(self, **kwargs):
        
        admision = get_object_or_404(Admision, pk=kwargs['pk'])
        admision.pagar()
        messages.info(self.request, u'¡Registrado el pago de la Admision!')
        return reverse('admision-view-id', args=[admision.id])

class HospitalizarView(RedirectView, LoginRequiredView):
    
    url = '/admision/hospitalizar'
    permanent = False
    
    
    def get_redirect_url(self, **kwargs):
        
        admision = get_object_or_404(Admision, pk=kwargs['pk'])
        admision.hospitalizar()
        messages.info(self.request, u'¡Admision Enviada a Enfermeria!')
        return reverse('admision-view-id', args=[admision.id])
