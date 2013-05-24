# -*- coding: utf-8 -*-
#
# Copyright (C) 2011-2013 Carlos Flores <cafg10@gmail.com>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library. If not, see <http://www.gnu.org/licenses/>.

from django.db.models import Q
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import (CreateView, ListView, TemplateView,
                                  DetailView, RedirectView, UpdateView)
from library.protected import LoginRequiredView
from persona.models import Persona
from persona.views import PersonaCreateView
from spital.forms import AdmisionForm, HabitacionForm, PreAdmisionForm
from spital.models import Admision, Habitacion, PreAdmision
from nightingale.models import Cargo
from emergency.models import Emergencia
from persona.forms import PersonaForm
from django.contrib import messages
from guardian.mixins import LoginRequiredMixin

class AdmisionIndexView(ListView, LoginRequiredView):
    
    """Muestra la pagina principal de el Centro de :class:`Admisiones`"""

    context_object_name = 'admisiones'
    queryset = Admision.objects.filter(~Q(estado='H')&~Q(estado='C')&~Q(estado='I'))
    template_name = 'admision/index.html'
    
    def get_context_data(self, **kwargs):
        
        """Realiza los calculos para mostrar el gráfico de tiempo de espera
        de las :class:`Admision`es"""

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
        
        context['preadmisiones'] = PreAdmision.objects.filter(completada=False)

        return context

class IngresarView(TemplateView, LoginRequiredView):
    
    """Muestra una interfaz para agregar una :class:`Admision` ya sea agregando
    una :class:`Persona` nueva o admitiendo una que ya se encuentra en el
    sistema"""

    template_name = 'admision/ingresar.html'
    
    def get_context_data(self, **kwargs):
        
        """Agrega el formulario para crear una :class:`Persona` desde la misma
        página"""

        context = super(IngresarView, self).get_context_data()
        context['persona_form'] = PersonaForm()
        return context

class PersonaAdmisionCreateView(PersonaCreateView):
    
    """Permite admitir una :class:`Persona` preexistente"""

    template_name = 'admision/persona_create.html'
    
    def get_success_url(self):
        
        return reverse('admision-persona-agregar', args=[self.object.id])

class PersonaFiadorCreateView(PersonaCreateView):
    
    """Permite ingresar una :class:`Persona` al sistema que servira como
    :class:`Fiador` a una :class:`Admision`"""

    template_name = 'admision/admision_fiador.html'
    
    def dispatch(self, *args, **kwargs):
        
        """Carga la :class:`Admision` desde la fuente de datos"""
        
        self.admision = get_object_or_404(Admision, pk=kwargs['admision'])
        return super(PersonaFiadorCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):

        """Agrega la :class:`Persona` a la lista de fiadores de la
        :class:`Admision`"""
        
        self.object = form.save()
        self.admision.fiadores.add(self.object)
        self.admision.save()
        messages.info(self.request, u"Agregado un Fiador!")
        
        return HttpResponseRedirect(self.admision.get_absolute_url())

    def get_context_data(self, **kwargs):
        
        context = super(PersonaFiadorCreateView, self).get_context_data(**kwargs)
        context['admision'] = self.admision
        return context

class PersonaReferenciaCreateView(PersonaCreateView):
    
    """Permite agregar una :class:`Persona` como referencia a una
    :class:`Admision`"""

    template_name = 'admision/admision_referencia.html'
    
    def dispatch(self, *args, **kwargs):
        
        """Carga la :class:`Admision` desde la fuente de datos"""
        
        self.admision = get_object_or_404(Admision, pk=kwargs['admision'])
        return super(PersonaReferenciaCreateView, self).dispatch(*args, **kwargs)
    
    def form_valid(self, form):

        """Agrega la :class:`Persona` a la lista de referencias de la
        :class:`Admision`"""
        
        self.object = form.save()
        self.admision.referencias.add(self.object)
        self.admision.save()
        messages.info(self.request, u"Agregada Referencia!")
        
        return HttpResponseRedirect(self.admision.get_absolute_url())

    def get_context_data(self, **kwargs):
        
        context = super(PersonaReferenciaCreateView, self).get_context_data(**kwargs)
        context['admision'] = self.admision
        return context

class ReferenciaAgregarView(RedirectView, LoginRequiredView):
    
    """Permite agregar una :class:`Persona` como referencia de una
    :class:`Admision`"""

    url = '/admision/referencia/agregar'
    
    def get_redirect_url(self, **kwargs):
        
        admision = get_object_or_404(Admision, pk=kwargs['admision'])
        persona = get_object_or_404(Persona, pk=kwargs['persona'])
        admision.referencias.add(persona)
        admision.save()
        return reverse('admision-view-id', args=[admision.id])

class FiadorAgregarView(RedirectView, LoginRequiredView):
    
    """Permite agregar una :class:`Persona` como fiador de una
    :class:`Admision`"""

    url = '/admision/fiador/agregar'
    
    def get_redirect_url(self, **kwargs):
        
        admision = get_object_or_404(Admision, pk=kwargs['admision'])
        persona = get_object_or_404(Persona, pk=kwargs['persona'])
        admision.fiadores.add(persona)
        admision.save()
        return reverse('admision-view-id', args=[admision.id])

class AdmisionCreateView(CreateView, LoginRequiredView):
    
    """Crea una :class:`Admision` para una :class:`Persona` ya existente en el
    sistema"""

    model = Admision
    form_class = AdmisionForm
    template_name = 'admision/admision_create.html'
    
    def get_form_kwargs(self):
        
        """Agrega el id de la :class:`Persona` a los argumentos de la sesión"""

        kwargs = super(AdmisionCreateView, self).get_form_kwargs()
        kwargs.update({ 'initial':{'paciente':self.persona.id}})
        return kwargs
    
    def dispatch(self, *args, **kwargs):
        
        """Carga la :class:`Persona` desde el origen de datos"""

        self.persona = get_object_or_404(Persona, pk=kwargs['persona'])
        return super(AdmisionCreateView, self).dispatch(*args, **kwargs)
    
    def form_valid(self, form):
        
        """Agrega la :class:`Persona que se esta admitiendo y el :class:`User`
        que esta realizando la :class:`Admision`"""

        self.object = form.save(commit=False)
        self.object.persona = self.persona
        self.object.admitio = self.request.user
        self.object.save()
        
        return HttpResponseRedirect(self.get_success_url())

class AdmisionDetailView(DetailView, LoginRequiredView):
    
    """Permite mostrar los datos de una :class:`Admision`"""

    context_object_name = 'admision'
    model = Admision
    template_name = 'admision/admision_detail.html'
    slug_field = 'uuid'

class AutorizarView(RedirectView, LoginRequiredView):
    
    """Permite marcar como autorizada una :class:`Admision`"""

    url = '/admision/autorizar'
    permanent = False
    
    def get_redirect_url(self, **kwargs):
        
        admision = get_object_or_404(Admision, pk=kwargs['pk'])
        admision.autorizar()
        messages.info(self.request, u'¡Admision Autorizada!')
        return reverse('admision-view-id', args=[admision.id])

class PagarView(RedirectView, LoginRequiredView):
    
    """Permite marcar como pagada una :class:`Admision`"""

    url = '/admision/hospitalizar'
    permanent = False
    
    def get_redirect_url(self, **kwargs):
        
        admision = get_object_or_404(Admision, pk=kwargs['pk'])
        admision.pagar()
        messages.info(self.request, u'¡Registrado el pago de la Admision!')
        return reverse('admision-view-id', args=[admision.id])

class HospitalizarView(RedirectView, LoginRequiredView):
    
    """Permite marcar como hospitalizada una :class:`Admision`"""

    url = '/admision/hospitalizar'
    permanent = False
    
    def get_redirect_url(self, **kwargs):
        
        admision = get_object_or_404(Admision, pk=kwargs['pk'])
        admision.hospitalizar()
        messages.info(self.request, u'¡Admision Enviada a Enfermeria!')
        return reverse('admision-view-id', args=[admision.id])

class HabitacionListView(ListView, LoginRequiredView):

    """Muestra la lista de las :class:`Habitacion`es para tener una vista
    rápida de las que se encuentran disponibles en un determinado momento"""

    context_object_name = 'habitaciones'
    queryset = Habitacion.objects
    template_name = 'admision/habitaciones.html'

class HabitacionCreateView(CreateView, LoginRequiredView):

    """Permite agregar una :class:`Habitacion` al :class:`Hospital`"""

    model = Habitacion
    form_class = HabitacionForm
    template_name = 'admision/habitacion_create.html'

class HabitacionDetailView(DetailView, LoginRequiredView):

    """Permite mostrar el estado de una :class:`Habitacion`"""
    
    context_object_name = 'habitacion'
    model = Habitacion
    template_name = 'admision/habitacion_detail.html'
    
    def get_context_data(self, **kwargs):
        
        """Permite paginar las admisiones que la :class:`Habitacion` ha
        recibido a lo largo del tiempo"""

        context = super(HabitacionDetailView, self).get_context_data(**kwargs)
        
        paginator = Paginator(self.object.admisiones, 10)
        try:
            page = int(request.GET.get("page", '1'))
        except ValueError:
            page = 1
        
        try:
            context['admisiones'] = paginator.page(page)
        except (InvalidPage, EmptyPage):
            context['admisiones'] = paginator.page(paginator.num_pages)

        return context

class HabitacionUpdateView(UpdateView, LoginRequiredView):

    """Permite editar los datos de una :class:`Habitacion`"""

    model = Habitacion
    form_class = HabitacionForm
    template_name = 'admision/habitacion_create.html'

class PreAdmisionCreateView(CreateView, LoginRequiredView):
    
    model = PreAdmision
    form_class = PreAdmisionForm
    
    def get_form_kwargs(self):
        
        """Agrega el id de la :class:`Persona` a los argumentos de la sesión"""

        kwargs = super(PreAdmisionCreateView, self).get_form_kwargs()
        kwargs.update({ 'initial':{'emergencia':self.emergencia.id}})
        return kwargs
    
    def dispatch(self, *args, **kwargs):
        
        """Carga la :class:`Persona` desde el origen de datos"""

        self.emergencia = get_object_or_404(Emergencia, pk=kwargs['emergencia'])
        return super(PreAdmisionCreateView, self).dispatch(*args, **kwargs)
    
    def form_valid(self, form):
        
        """Agrega la :class:`Persona que se esta admitiendo y el :class:`User`
        que esta realizando la :class:`Admision`"""

        self.object = form.save(commit=False)
        self.object.persona = self.emergencia.persona
        self.object.save()
        
        return HttpResponseRedirect(self.get_success_url())

class AdmisionPreCreateView(CreateView, LoginRequiredView):
    
    """Crea una :class:`Admision` para una :class:`Persona` ya existente en el
    sistema"""
    
    model = Admision
    form_class = AdmisionForm
    template_name = 'admision/admision_precreate.html'
    
    def get_form_kwargs(self):
        
        """Agrega el id de la :class:`Persona` a los argumentos de la sesión"""
        
        kwargs = super(AdmisionPreCreateView, self).get_form_kwargs()
        kwargs.update({ 'initial':{'paciente':self.preadmision.emergencia.persona.id}})
        return kwargs
    
    def dispatch(self, *args, **kwargs):
        
        """Carga la :class:`Persona` desde el origen de datos"""
        
        self.preadmision = get_object_or_404(PreAdmision, pk=kwargs['preadmision'])
        return super(AdmisionPreCreateView, self).dispatch(*args, **kwargs)
    
    def form_valid(self, form):
        
        """Agrega la :class:`Persona que se esta admitiendo y el :class:`User`
        que esta realizando la :class:`Admision`"""
        
        self.object = form.save(commit=False)
        self.object.persona = self.preadmision.emergencia.persona
        self.object.admitio = self.request.user
        self.preadmision.compleatada = True
        if self.preadmision.transferir_cobros:
            
            for cobro in self.preadmision.emergencia.cobros.all():
                cargo = Cargo()
                cargo.admision = self.object
                cargo.cargo = cobro.cargo
                cargo.cantidad = cobro.cantidad
                cargo.save()
        
        self.object.save()
        self.preadmision.save()
        
        return HttpResponseRedirect(self.get_success_url())
    
    def get_context_data(self, **kwargs):
        
        """Realiza los calculos para mostrar el gráfico de tiempo de espera
        de las :class:`Admision`es"""
        
        context = super(AdmisionPreCreateView, self).get_context_data(**kwargs)
        
        context['preadmision'] = self.preadmision
        
        return context
