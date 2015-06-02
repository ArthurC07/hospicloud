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
from guardian.decorators import permission_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import (CreateView, ListView, TemplateView,
                                  DetailView, UpdateView,
                                  DeleteView)
from django.contrib import messages

from persona.models import Persona
from persona.views import (PersonaCreateView, FisicoUpdateView,
                           EstiloVidaUpdateView, AntecedenteUpdateView,
                           AntecedenteFamiliarUpdateView,
                           AntecedenteObstetricoUpdateView,
                           AntecedenteQuirurgicoUpdateView,
                           AntecedenteQuirurgicoCreateView)
from persona.forms import PersonaForm
from emergency.models import (Emergencia, Tratamiento, RemisionInterna,
                              RemisionExterna, Hallazgo, Cobro, Diagnostico,
                              ExamenFisico)
from emergency.forms import (EmergenciaForm, TratamientoForm, HallazgoForm,
                             RemisionInternaForm, RemisionExternaForm,
                             CobroForm, DiagnosticoForm, ExamenFisicoForm)
from users.mixins import LoginRequiredMixin


class EmergenciaPermissionMixin(LoginRequiredMixin):
    @method_decorator(permission_required('emergency.emergencia'))
    def dispatch(self, *args, **kwargs):
        return super(EmergenciaPermissionMixin, self).dispatch(*args, **kwargs)


class EmergenciaIndexView(ListView, EmergenciaPermissionMixin):
    model = Emergencia
    context_object_name = 'emergencias'
    template_name = 'emergency/index.html'
    paginate_by = 20

    def get_queryset(self):
        """Obtiene las :class:`Emergencia`s atendidas el día de hoy"""
        return Emergencia.objects.order_by('-created')


class EmergenciaPreCreateView(TemplateView, LoginRequiredMixin):
    """Permite mostrar una interfaz donde decidir si agregar una nueva
    :class:`Persona` o agregar la :class:`Emergencia` a una ya ingresada
    previamente"""

    template_name = 'emergency/emergencia_agregar.html'

    def get_context_data(self, **kwargs):
        context = super(EmergenciaPreCreateView, self).get_context_data(
            **kwargs)
        context['persona_form'] = PersonaForm()
        context['persona_form'].helper.form_action = 'emergency-persona-create'
        return context


class PersonaEmergenciaCreateView(PersonaCreateView, LoginRequiredMixin):
    """Permite admitir una :class:`Persona` nueva"""

    template_name = 'persona/nuevo.html'

    def get_success_url(self):
        return reverse('emergency-create', args=[self.object.id])


class EmergenciaCreateView(CreateView, LoginRequiredMixin):
    """Crea una :class:`Emergencia` para una :class:`Persona` ya existente en el
    sistema"""

    model = Emergencia
    form_class = EmergenciaForm
    template_name = 'emergency/emergencia_create.html'

    def get_context_data(self, **kwargs):
        context = super(EmergenciaCreateView, self).get_context_data(**kwargs)
        context['persona'] = self.persona
        return context

    def get_form_kwargs(self):
        """Agrega el id de la :class:`Persona` a los argumentos de la sesión"""

        kwargs = super(EmergenciaCreateView, self).get_form_kwargs()
        kwargs.update({'initial': {'persona': self.persona.id}})
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


class EmergenciaDetailView(DetailView, LoginRequiredMixin):
    """Permite mostrar los datos de la :class:`Emergencia`"""

    model = Emergencia
    template_name = 'emergency/emergency_detail.html'


class EmergenciaUpdateView(UpdateView, LoginRequiredMixin):
    model = Emergencia
    template_name = 'emergency/emergencia_update.html'


class BaseCreateView(CreateView, LoginRequiredMixin):
    """Permite llenar el formulario de una clase que requiera
    :class:`Emergencia`s de manera previa - DRY"""

    template_name = 'emergency/emergencia_child_form.html'

    def get_context_data(self, **kwargs):
        context = super(BaseCreateView, self).get_context_data(**kwargs)
        context['emergencia'] = self.emergencia
        return context

    def get_form_kwargs(self):
        """Agrega la :class:`Emergencia` obtenida como el valor a utilizar en el
        formulario que será llenado posteriormente"""

        kwargs = super(BaseCreateView, self).get_form_kwargs()
        kwargs.update({'initial': {'emergencia': self.emergencia.id,
                                   'usuario': self.request.user.id}})
        return kwargs

    def dispatch(self, *args, **kwargs):
        """Obtiene la :class:`Emergencia` que se entrego como argumento en la
        url"""

        self.emergencia = get_object_or_404(Emergencia, pk=kwargs['emergencia'])
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


class RemisionInternaCreateView(BaseCreateView):
    """Registrar el envio de una :class:`Persona`, que ingreso a consulta,
    hacia un especialista"""

    model = RemisionInterna
    form_class = RemisionInternaForm


class RemisionExternaCreateView(BaseCreateView):
    """Registrar el envio de una :class:`Persona`, que ingreso a consulta,
    hacia otro centro médico"""

    model = RemisionExterna
    form_class = RemisionExternaForm


class ExamenFisicoCreateView(BaseCreateView):
    """Registrar los :class:`ExamenFisico`s efectuados a la :class:`Persona`,
    que ingreso a consulta"""

    model = ExamenFisico
    form_class = ExamenFisicoForm


class HallazgoCreateView(BaseCreateView):
    """Registrar los hallazgos de un examen físico a la :class:`Persona`,
    que ingreso a consulta"""

    model = Hallazgo
    form_class = HallazgoForm


class CobroCreateView(BaseCreateView):
    """Registrar los :class:`Cobro`s efectuados a la :class:`Persona`,
    que ingreso a consulta"""

    model = Cobro
    form_class = CobroForm

    def dispatch(self, *args, **kwargs):
        """Obtiene la :class:`Emergencia` que se entrego como argumento en la
        url"""

        self.emergencia = get_object_or_404(Emergencia, pk=kwargs['emergencia'])
        if self.request.user.profile.inventario is None:
            messages.info(self.request,
                          u'Su usuario no tiene un inventario asociado, '
                          u'por favor modifique su perfil para indicar su '
                          u'inventario')
            return HttpResponseRedirect(self.emergencia.get_absolute_url())
        return super(BaseCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        item = self.request.user.profile.inventario.buscar_item(
            self.object.cargo)
        item.disminuir(self.object.cantidad)
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


class CobroDeleteView(DeleteView, LoginRequiredMixin):
    model = Cobro

    def delete(self, request, *args, **kwargs):
        """
        Calls the delete() method on the fetched object and then
        redirects to the success URL.
        """
        self.object = self.get_object()

        item = self.request.user.profile.inventario.buscar_item(
            self.object.cargo)
        item.incrementar(self.object.cantidad)

        self.object.delete()
        return HttpResponseRedirect(self.get_success_url())

    def get_object(self, queryset=None):
        obj = super(CobroDeleteView, self).get_object(queryset)
        self.emergencia = obj.emergencia
        return obj

    def get_success_url(self):
        return self.emergencia.get_absolute_url()


class DiagnosticoCreateView(BaseCreateView):
    """Registrar los :class:`Diagnostico`s efectuados a la :class:`Persona`,
    que ingreso a consulta"""

    model = Diagnostico
    form_class = DiagnosticoForm


class EmergenciaFisicoUpdateView(FisicoUpdateView):
    def dispatch(self, *args, **kwargs):
        """Obtiene la :class:`Emergencia` que se entrego como argumento en la
        url"""

        self.emergencia = get_object_or_404(Emergencia, pk=kwargs['emergencia'])
        return super(EmergenciaFisicoUpdateView, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse('emergency-view-id', args=[self.emergencia.id])


class EmergenciaEstiloVidaUpdateView(EstiloVidaUpdateView):
    def dispatch(self, *args, **kwargs):
        """Obtiene la :class:`Emergencia` que se entrego como argumento en la
        url"""

        self.emergencia = get_object_or_404(Emergencia, pk=kwargs['emergencia'])
        return super(EmergenciaEstiloVidaUpdateView,
                     self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse('emergency-view-id', args=[self.emergencia.id])


class EmergenciaAntecedenteUpdateView(AntecedenteUpdateView):
    def dispatch(self, *args, **kwargs):
        """Obtiene la :class:`Emergencia` que se entrego como argumento en la
        url"""

        self.emergencia = get_object_or_404(Emergencia, pk=kwargs['emergencia'])
        return super(EmergenciaAntecedenteUpdateView, self).dispatch(*args,
                                                                     **kwargs)

    def get_success_url(self):
        return reverse('emergency-view-id', args=[self.emergencia.id])


class EmergenciaAntecedenteFamiliarUpdateView(AntecedenteFamiliarUpdateView):
    def dispatch(self, *args, **kwargs):
        """Obtiene la :class:`Emergencia` que se entrego como argumento en la
        url"""

        self.emergencia = get_object_or_404(Emergencia, pk=kwargs['emergencia'])
        return super(EmergenciaAntecedenteFamiliarUpdateView, self).dispatch(
            *args, **kwargs)

    def get_success_url(self):
        return reverse('emergency-view-id', args=[self.emergencia.id])


class EmergenciaAntecedenteObstetricoUpdateView(
    AntecedenteObstetricoUpdateView):
    def dispatch(self, *args, **kwargs):
        """Obtiene la :class:`Emergencia` que se entrego como argumento en la
        url"""

        self.emergencia = get_object_or_404(Emergencia, pk=kwargs['emergencia'])
        return super(EmergenciaAntecedenteObstetricoUpdateView,
                     self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse('emergency-view-id', args=[self.emergencia.id])


class EmergenciaAntecedenteQuirurgicoUpdateView(
    AntecedenteQuirurgicoUpdateView):
    def dispatch(self, *args, **kwargs):
        """Obtiene la :class:`Emergencia` que se entrego como argumento en la
        url"""

        self.emergencia = get_object_or_404(Emergencia, pk=kwargs['emergencia'])
        return super(EmergenciaAntecedenteQuirurgicoUpdateView,
                     self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse('emergency-view-id', args=[self.emergencia.id])


class EmergenciaAntecedenteQuirurgicoCreateView(
    AntecedenteQuirurgicoCreateView):
    def dispatch(self, *args, **kwargs):
        """Obtiene la :class:`Emergencia` que se entrego como argumento en la
        url"""

        self.emergencia = get_object_or_404(Emergencia, pk=kwargs['emergencia'])
        return super(EmergenciaAntecedenteQuirurgicoCreateView,
                     self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse('emergency-view-id', args=[self.emergencia.id])
