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
from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.db.models.query_utils import Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, UpdateView, ListView, \
    RedirectView
from django.views.generic.base import ContextMixin
from django.views.generic.edit import FormMixin

from persona.forms import PersonaForm, FisicoForm, EstiloVidaForm, \
    AntecedenteForm, AntecedenteFamiliarForm, AntecedenteObstetricoForm, \
    AntecedenteQuirurgicoForm, PersonaSearchForm, EmpleadorForm, EmpleoForm, \
    PersonaAdvancedSearchForm
from persona.models import Persona, Fisico, EstiloVida, Antecedente, \
    AntecedenteFamiliar, AntecedenteObstetrico, AntecedenteQuirurgico, Empleo, \
    Empleador, remove_duplicates
from users.mixins import LoginRequiredMixin


class PersonaPermissionMixin(LoginRequiredMixin):
    @method_decorator(permission_required('persona.persona'))
    def dispatch(self, *args, **kwargs):
        return super(PersonaPermissionMixin, self).dispatch(*args, **kwargs)


class PersonaMixin(ContextMixin):
    """Agrega una :class:`Persona` en la vista"""

    def dispatch(self, *args, **kwargs):
        self.persona = get_object_or_404(Persona, pk=kwargs['persona'])
        return super(PersonaMixin, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PersonaMixin, self).get_context_data(**kwargs)
        context['persona'] = self.persona
        return context


class PersonaFormMixin(FormMixin, PersonaMixin):
    """Agrega la :class:`Persona` a los argumentos iniciales de un formulario"""

    def get_initial(self):
        initial = super(PersonaFormMixin, self).get_initial()
        initial = initial.copy()
        initial['persona'] = self.persona
        return initial


class PersonaIndexView(ListView, PersonaPermissionMixin):
    context_object_name = 'personas'
    model = Persona
    template_name = 'persona/index.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(PersonaIndexView, self).get_context_data(**kwargs)

        context['advanced_search_form'] = PersonaAdvancedSearchForm()

        return context


class PersonaDetailView(DetailView, LoginRequiredMixin):
    """
    Permite mostrar los datos de una :class:`Persona`
    """
    context_object_name = 'persona'
    model = Persona

    def get_context_data(self, **kwargs):
        context = super(PersonaDetailView, self).get_context_data(**kwargs)

        if self.object.sexo == 'F':
            antecedente_obstetrico = AntecedenteObstetrico(persona=self.object)
            antecedente_obstetrico.created = timezone.now()
            antecedente_obstetrico.save()

        self.object.save()

        return context


class PersonaCreateView(CreateView, LoginRequiredMixin):
    """Permite ingresar :class:`Persona`s a la aplicación"""

    model = Persona
    form_class = PersonaForm


class PersonaUpdateView(UpdateView, LoginRequiredMixin):
    """Permite actualizar los datos de una :class:`Persona`"""

    model = Persona
    form_class = PersonaForm


class FisicoUpdateView(UpdateView, LoginRequiredMixin):
    """
    Permite actualizar los datos del :class:`Fisico` de una :class:`Persona`
    """

    model = Fisico
    form_class = FisicoForm


class EstiloVidaUpdateView(UpdateView, LoginRequiredMixin):
    """
    Permite actualizar los datos del :class:`EstiloVida` de una
    :class:`Persona`
    """
    model = EstiloVida
    form_class = EstiloVidaForm


class AntecedenteUpdateView(UpdateView, LoginRequiredMixin):
    """
    Permite actualizar los datos del :class:`Antecedente` de una
    :class:`Persona`
    """
    model = Antecedente
    form_class = AntecedenteForm


class AntecedenteFamiliarUpdateView(UpdateView, LoginRequiredMixin):
    """
    Permite actualizar los datos del :class:`AntecedenteFamiliar` de una
    :class:`Persona`
    """
    model = AntecedenteFamiliar
    form_class = AntecedenteFamiliarForm


class AntecedenteObstetricoUpdateView(UpdateView, LoginRequiredMixin):
    """
    Permite actualizar los datos del :class:`AntecedenteObstetrico` de una
    :class:`Persona`
    """
    model = AntecedenteObstetrico
    form_class = AntecedenteObstetricoForm


class AntecedenteQuirurgicoCreateView(CreateView, LoginRequiredMixin,
                                      PersonaFormMixin):
    """Permite actualizar los datos del :class:`AntecedenteQuirurgico` de una
    :class:`Persona`"""
    model = AntecedenteQuirurgico
    form_class = AntecedenteQuirurgicoForm


class AntecedenteQuirurgicoUpdateView(UpdateView, LoginRequiredMixin):
    """Permite actualizar los datos del :class:`AntecedenteQuirurgico` de una
    :class:`Persona`"""
    model = AntecedenteQuirurgico
    form_class = AntecedenteQuirurgicoForm


class PersonaSearchView(ListView, LoginRequiredMixin):
    """
    Allows searching for :class:`Persona` by using information entered in a form
    in the UI
    """
    context_object_name = 'personas'
    model = Persona
    template_name = 'persona/index.html'
    paginate_by = 10

    def get_queryset(self):
        """
        Builds the queryset that will filter the :class:`Persona` objects based
        in the :class:`PersonaSearchForm` given information
        :return: a filtered :class:`QuerySet`
        """
        form = PersonaSearchForm(self.request.GET)

        if form.is_valid():
            query = form.cleaned_data['query']

            queryset = Persona.objects.filter(
                    Q(nombre__icontains=query) |
                    Q(apellido__icontains=query) |
                    Q(identificacion__icontains=query)
            )

            return queryset.all()

        return Persona.objects.none()


class PersonaAdvancedSearchView(ListView, LoginRequiredMixin):
    """
    Allows searching for a :class:`Persona` using its nombre and apellidos
    """
    context_object_name = 'personas'
    model = Persona
    template_name = 'persona/index.html'
    paginate_by = 10

    def get_queryset(self):
        """
        Filters the queryset using the supplied data from a
        :class:`PersonaAdvancedSearchForm`
        :return: a queryset filtering the nombre and apellido fields using the
                 values indicated by the form
        """
        form = PersonaAdvancedSearchForm(self.request.GET)

        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            apellidos = form.cleaned_data['apellidos']

            queryset = Persona.objects.filter(
                    nombre__icontains=nombre,
                    apellido__icontains=apellidos,
            )

            return queryset

        return Persona.objects.none()

    def get_context_data(self, **kwargs):
        """
        Adds the PersonaAdvancedSearchForm to the view's context
        :param kwargs:
        :return: context
        """
        context = super(PersonaAdvancedSearchView, self).get_context_data(
                **kwargs)

        context['advanced_search_form'] = PersonaAdvancedSearchForm()

        return context


class EmpleadorCreateView(CreateView, LoginRequiredMixin):
    model = Empleador
    form_class = EmpleadorForm


class EmpleadorDetailView(DetailView, LoginRequiredMixin):
    model = Empleador
    context_object_name = 'empleador'


class EmpleoCreateView(PersonaFormMixin, CreateView):
    model = Empleo
    form_class = EmpleoForm


class PersonaDuplicateView(RedirectView, LoginRequiredMixin):
    """
    Reports a :class:`Persona` instance as duplicate for consolidation
    """
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        persona = get_object_or_404(Persona, pk=kwargs['pk'])
        persona.duplicado = True
        persona.save()
        messages.info(self.request, u'¡Se marcado como duplicada!')

        if self.request.META['HTTP_REFERER']:
            return self.request.META['HTTP_REFERER']
        else:
            return persona.get_absolute_url()


class AntecedenteObstetricoCreateView(PersonaFormMixin, CreateView,
                                      LoginRequiredMixin):
    model = AntecedenteObstetrico
    form_class = AntecedenteObstetricoForm


class PersonaDuplicateRemoveView(RedirectView, LoginRequiredMixin):
    """
    Allows the user to remove all reported duplicates from the :class:`Persona`
    data
    """
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        """
        Processes the duplicates and return to the persona index.
        :param args:
        :param kwargs:
        :return:
        """
        cantidad = remove_duplicates()
        messages.info(self.request,
                      u'¡Se han limpiado {0} duplicados!'.format(cantidad))

        if self.request.META['HTTP_REFERER']:
            return self.request.META['HTTP_REFERER']
        else:
            return 'persona-index'
