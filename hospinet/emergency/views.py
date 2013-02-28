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
from persona.forms import PersonaForm
from emergency.models import (Emergencia, Tratamiento, RemisionInterna,
                            RemisionExterna, Hallazgo)
from emergency.forms import (EmergenciaForm, TratamientoForm, HallazgoForm,
                             RemisionInternaForm, RemisionExternaForm)
from django.contrib import messages
from datetime import datetime, time, date
from django.utils import timezone

class EmergenciaPreCreateView(TemplateView, LoginRequiredView):
    
    """Permite mostrar una interfaz donde decidir si agregar una nueva
    :class:`Persona` o agregar la :class:`Emergencia` a una ya ingresada
    previamente"""
    
    template_name = 'emergency/emergencia_agregar.html'
    
    def get_context_data(self, **kwargs):
        
        context = super(EmergenciaPreCreateView, self).get_context_data()
        context['persona_form'] = PersonaForm()
        return context

class PersonaEmergenciaCreateView(PersonaCreateView, LoginRequiredView):
    
    """Permite admitir una :class:`Persona` nueva"""

    template_name = 'persona/nuevo.html'
    
    def get_success_url(self):
        
        return reverse('emergency-persona-agregar', args=[self.object.id])

class EmergenciaCreateView(CreateView, LoginRequiredView):
    
    """Crea una :class:`Emergencia` para una :class:`Persona` ya existente en el
    sistema"""

    model = Emergencia
    form_class = EmergenciaForm
    template_name = 'emergency/emergencia_create.html'
    
    def get_form_kwargs(self):
        
        """Agrega el id de la :class:`Persona` a los argumentos de la sesión"""

        kwargs = super(EmergenciaCreateView, self).get_form_kwargs()
        kwargs.update({ 'initial':{'persona':self.persona.id}})
        return kwargs
    
    def dispatch(self, *args, **kwargs):
        
        """Carga la :class:`Persona` desde el origen de datos"""

        self.persona = get_object_or_404(Persona, pk=kwargs['persona'])
        return super(EmergenciaCreateView, self).dispatch(*args, **kwargs)
    
    def form_valid(self, form):
        
        """Agrega la :class:`Persona que se esta admitiendo y el :class:`User`
        que esta realizando la :class:`Emergencia`"""

        self.object = form.save(commit=False)
        self.object.persona = self.persona
        self.object.usuario = self.request.user
        self.object.save()
        
        return HttpResponseRedirect(self.get_success_url())

class EmergenciaDetailView(DetailView, LoginRequiredView):

    """Permite mostrar los datos de la :class:`Emergencia`"""

    model = Emergencia
    template_name = 'emergency/emergency_detail.html'

class EmergenciaUpdateView(UpdateView, LoginRequiredView):

    model = Emergencia
    template_name = 'emergency/emergencia_update.html'

class BaseCreateView(CreateView, LoginRequiredView):
    
    """Permite llenar el formulario de una clase que requiera
    :class:`Emergencia`s de manera previa - DRY"""

    def get_context_data(self, **kwargs):
        
        context = super(BaseCreateView, self).get_context_data(**kwargs)
        context['emergencia'] = self.emergencia
        return context
    
    def get_form_kwargs(self):
        
        """Agrega la :class:`Emergencia` obtenida como el valor a utilizar en el
        formulario que será llenado posteriormente"""

        kwargs = super(BaseCreateView, self).get_form_kwargs()
        kwargs.update({'initial':{'emergencia':self.emergencia.id,
                                  'usuario':self.request.user.id}})
        return kwargs
    
    def dispatch(self, *args, **kwargs):
        
        """Obtiene la :class:`Emergencia` que se entrego como argumento en la
        url"""

        self.admision = get_object_or_404(Emergencia, pk=kwargs['emergencia'])
        return super(BaseCreateView, self).dispatch(*args, **kwargs)
    
    def form_valid(self, form):
        
        """Guarda el objeto generado espeficando la :class:`Emergencia` obtenida
        de los argumentos y el :class:`User` que esta utilizando la aplicación
        """

        self.object = form.save(commit=False)
        self.object.emergencia = self.emergencia
        self.usuario = self.request.user
        self.object.save()
        
        messages.info(self.request, u"Emergencia Actualizada")
        
        return HttpResponseRedirect(self.get_success_url())

class TratamientoCreateView(BaseCreateView):

    """Permite agregar un :class:`Tratamiento` a una :class:`Emergencia`"""

    model = Tratamiento
    form_class = TratamientoForm
    template_name = 'emergency/tratamiento_create.html'

class RemisionInternaCreateView(BaseCreateView):

    """Registrar el envio de una :class:`Persona`, que ingreso a consulta,
    hacia un especialista"""

    model = RemisionInterna
    form_class = RemisionInternaForm
    template_name = 'emergency/remision_interna_create.html'

class RemisionExternaCreateView(BaseCreateView):

    """Registrar el envio de una :class:`Persona`, que ingreso a consulta,
    hacia otro centro médico"""

    model = RemisionExterna
    form_class = RemisionExternaForm
    template_name = 'emergency/remision_externa_create.html'

class HallazgoCreateView(BaseCreateView):

    """Registrar los hallazgos de un examen físico a la :class:`Persona`,
    que ingreso a consulta"""

    model = Hallazgo
    form_class = HallazgoForm
    template_name = 'emergency/hallazgo_create.html'

class EmergenciaListView(ListView, LoginRequiredView):

    context_object_name = 'emergencias'
    template_name = 'emergency/index.html'

    def get_queryset(self):

        """Obtiene las :class:`Emergencia`s atendidas el día de hoy"""

        inicio = timezone.make_aware(
                                datetime.combine(date.today(), time.min),
                                timezone.get_default_timezone())
        fin = timezone.make_aware(datetime.combine(date.today(), time.max),
                                        timezone.get_default_timezone())
        return Emergencia.objects.filter(created__range=(inicio, fin))
