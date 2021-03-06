# -*- coding: utf-8 -*-
# Copyright (C) 2015 Carlos Flores <cafg10@gmail.com>
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
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, DetailView, UpdateView
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.edit import FormMixin

from persona.forms import PersonaForm, AntecedenteForm, FisicoForm, \
    AntecedenteFamiliarForm, AntecedenteObstetricoForm, \
    AntecedenteQuirurgicoForm, EstiloVidaForm
from persona.models import Persona, Antecedente, AntecedenteFamiliar, \
    AntecedenteObstetrico, Fisico, EstiloVida, AntecedenteQuirurgico
from persona.views import PersonaFormMixin
from users.mixins import LoginRequiredMixin
from users.models import Ciudad


class UserRedirectMixin(LoginRequiredMixin):
    def get_success_url(self):
        return reverse('userena_profile_detail',
                       args=[self.request.user.username])


class UserPersonaCreateView(CreateView, UserRedirectMixin):
    model = Persona
    form_class = PersonaForm
    template_name = 'users/persona_form.html'

    def form_valid(self, form):
        self.object = form.save()
        self.request.user.profile.persona = self.object
        self.request.user.profile.save()
        self.request.user.first_name = self.object.nombre
        self.request.user.last_name = self.object.apellido
        self.request.user.save()

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('userena_profile_detail',
                       args=[self.request.user.username])


class UserPersonaDetailView(LoginRequiredMixin, DetailView):
    model = Persona
    context_object_name = 'persona'

    def get_success_url(self):
        return reverse('userena_profile_detail',
                       args=[self.request.user.username])


class UserPersonaUpdateView(UserRedirectMixin, UpdateView):
    model = Persona
    form_class = PersonaForm
    template_name = 'users/persona_form.html'

    def get_success_url(self):
        return reverse('userena_profile_detail',
                       args=[self.request.user.username])


class UserFisicoUpdateView(UserRedirectMixin, UpdateView):
    """
    Permite actualizar los datos del :class:`Fisico` de una :class:`Persona`
    """

    model = Fisico
    form_class = FisicoForm

    def get_success_url(self):
        return reverse('userena_profile_detail',
                       args=[self.request.user.username])


class UserAntecedenteUpdateView(UserRedirectMixin, UpdateView):
    """Permite actualizar los datos del :class:`Antecedente` de una
    :class:`Persona`"""

    model = Antecedente
    form_class = AntecedenteForm

    def get_success_url(self):
        return reverse('userena_profile_detail',
                       args=[self.request.user.username])


class UserAntecedenteFamiliarUpdateView(UserRedirectMixin, UpdateView):
    """Permite actualizar los datos del :class:`AntecedenteFamiliar` de una
    :class:`Persona`"""

    model = AntecedenteFamiliar
    form_class = AntecedenteFamiliarForm

    def get_success_url(self):
        return reverse('userena_profile_detail',
                       args=[self.request.user.username])


class UserAntecedenteObstetricoUpdateView(UserRedirectMixin, UpdateView):
    """Permite actualizar los datos del :class:`AntecedenteObstetrico` de una
    :class:`Persona`"""

    model = AntecedenteObstetrico
    form_class = AntecedenteObstetricoForm

    def get_success_url(self):
        return reverse('userena_profile_detail',
                       args=[self.request.user.username])


class UserAntecedenteQuirurgicoCreateView(CreateView, PersonaFormMixin):
    """Permite actualizar los datos del :class:`AntecedenteQuirurgico` de una
    :class:`Persona`"""

    model = AntecedenteQuirurgico
    form_class = AntecedenteQuirurgicoForm

    def get_success_url(self):
        return reverse('userena_profile_detail',
                       args=[self.request.user.username])


class UserAntecedenteQuirurgicoUpdateView(UpdateView, UserRedirectMixin):
    """Permite actualizar los datos del :class:`AntecedenteQuirurgico` de una
    :class:`Persona`"""

    model = AntecedenteQuirurgico
    form_class = AntecedenteQuirurgicoForm

    def get_success_url(self):
        return reverse('userena_profile_detail',
                       args=[self.request.user.username])


class UserEstiloVidaUpdateView(LoginRequiredMixin, UpdateView):
    """Permite actualizar los datos del :class:`EstiloVida` de una
    :class:`Persona`"""

    model = EstiloVida
    form_class = EstiloVidaForm

    def get_success_url(self):
        return reverse('userena_profile_detail',
                       args=[self.request.user.username])


class CiudadMixin(TemplateResponseMixin):
    """Permite obtener un :class:`Ciudad` desde los argumentos en una url"""

    def dispatch(self, *args, **kwargs):
        self.ciudad = get_object_or_404(Ciudad, pk=kwargs['ciudad'])
        return super(CiudadMixin, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CiudadMixin, self).get_context_data(**kwargs)

        context['cotizacion'] = self.cotizacion

        return context


class CiudadFormMixin(CiudadMixin, FormMixin):
    """Permite inicializar el :class:`Ciudad` que se utilizará en un
    formulario"""

    def get_initial(self):
        initial = super(CiudadFormMixin, self).get_initial()
        initial = initial.copy()
        initial['ciudad'] = self.ciudad
        return initial
