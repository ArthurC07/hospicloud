# -*- coding: utf-8 -*-
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
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, DetailView, UpdateView
from persona.forms import (PersonaForm, AntecedenteForm, FisicoForm,
                           AntecedenteFamiliarForm, AntecedenteObstetricoForm,
                           AntecedenteQuirurgicoForm, EstiloVidaForm)
from persona.models import (Persona, Antecedente, AntecedenteFamiliar,
                            AntecedenteObstetrico, Fisico, EstiloVida,
                            AntecedenteQuirurgico)
from persona.views import PersonaFormMixin
from users.mixins import LoginRequiredMixin


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


class UserPersonaDetailView(DetailView, LoginRequiredMixin):
    model = Persona
    context_object_name = 'persona'

    def get_success_url(self):

        return reverse('userena_profile_detail',
                       args=[self.request.user.username])


class UserPersonaUpdateView(UpdateView, UserRedirectMixin):
    model = Persona
    form_class = PersonaForm
    template_name = 'users/persona_form.html'

    def get_success_url(self):

        return reverse('userena_profile_detail',
                       args=[self.request.user.username])


class UserFisicoUpdateView(UpdateView, UserRedirectMixin):
    """
    Permite actualizar los datos del :class:`Fisico` de una :class:`Persona`
    """

    model = Fisico
    form_class = FisicoForm

    def get_success_url(self):

        return reverse('userena_profile_detail',
                       args=[self.request.user.username])


class UserAntecedenteUpdateView(UpdateView, UserRedirectMixin):
    """Permite actualizar los datos del :class:`Antecedente` de una
    :class:`Persona`"""

    model = Antecedente
    form_class = AntecedenteForm

    def get_success_url(self):

        return reverse('userena_profile_detail',
                       args=[self.request.user.username])


class UserAntecedenteFamiliarUpdateView(UpdateView, UserRedirectMixin):
    """Permite actualizar los datos del :class:`AntecedenteFamiliar` de una
    :class:`Persona`"""

    model = AntecedenteFamiliar
    form_class = AntecedenteFamiliarForm

    def get_success_url(self):

        return reverse('userena_profile_detail',
                       args=[self.request.user.username])


class UserAntecedenteObstetricoUpdateView(UpdateView, UserRedirectMixin):
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


class UserEstiloVidaUpdateView(UpdateView, LoginRequiredMixin):
    """Permite actualizar los datos del :class:`EstiloVida` de una
    :class:`Persona`"""

    model = EstiloVida
    form_class = EstiloVidaForm

    def get_success_url(self):

        return reverse('userena_profile_detail',
                       args=[self.request.user.username])
