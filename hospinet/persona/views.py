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
from django.contrib import messages
from django.contrib.auth.decorators import permission_required

from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.generic import (CreateView, DetailView, UpdateView,
                                  ListView, View)
from django.views.generic.edit import FormMixin
from django.shortcuts import get_object_or_404
from django.db.models.query_utils import Q

from persona.forms import (PersonaForm, FisicoForm, EstiloVidaForm,
                           AntecedenteForm, AntecedenteFamiliarForm,
                           AntecedenteObstetricoForm,
                           AntecedenteQuirurgicoForm, PersonaSearchForm)
from persona.models import (Persona, Fisico, EstiloVida, Antecedente,
                            AntecedenteFamiliar, AntecedenteObstetrico,
                            AntecedenteQuirurgico)
from users.mixins import LoginRequiredMixin


class PersonaPermissionMixin(LoginRequiredMixin):
    @method_decorator(permission_required('persona.persona'))
    def dispatch(self, *args, **kwargs):
        return super(PersonaPermissionMixin, self).dispatch(*args, **kwargs)


class PersonaIndexView(ListView, PersonaPermissionMixin):
    context_object_name = 'personas'
    model = Persona
    template_name = 'persona/index.html'
    paginate_by = 10


class PersonaDetailView(DetailView, LoginRequiredMixin):
    """Permite mostrar los datos de una :class:`Persona`"""

    context_object_name = 'persona'
    model = Persona
    template_name = 'persona/persona_detail.html'


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
    """Permite actualizar los datos del :class:`EstiloVida` de una
    :class:`Persona`"""

    model = EstiloVida
    form_class = EstiloVidaForm


class AntecedenteUpdateView(UpdateView, LoginRequiredMixin):
    """Permite actualizar los datos del :class:`Antecedente` de una
    :class:`Persona`"""

    model = Antecedente
    form_class = AntecedenteForm


class AntecedenteFamiliarUpdateView(UpdateView, LoginRequiredMixin):
    """Permite actualizar los datos del :class:`AntecedenteFamiliar` de una
    :class:`Persona`"""

    model = AntecedenteFamiliar
    form_class = AntecedenteFamiliarForm


class AntecedenteObstetricoUpdateView(UpdateView, LoginRequiredMixin):
    """Permite actualizar los datos del :class:`AntecedenteObstetrico` de una
    :class:`Persona`"""

    model = AntecedenteObstetrico
    form_class = AntecedenteObstetricoForm


class AntecedenteQuirurgicoCreateView(CreateView, LoginRequiredMixin):
    """Permite actualizar los datos del :class:`AntecedenteQuirurgico` de una
    :class:`Persona`"""

    model = AntecedenteQuirurgico
    form_class = AntecedenteQuirurgicoForm

    def get_context_data(self, **kwargs):
        context = super(AntecedenteQuirurgicoCreateView, self).get_context_data(
            **kwargs)
        context['persona'] = self.persona
        return context

    def dispatch(self, *args, **kwargs):
        """Obtiene la :class:`Persona` que se entrego como argumento en la
        url"""

        self.persona = get_object_or_404(Persona, pk=kwargs['pk'])
        return super(AntecedenteQuirurgicoCreateView, self).dispatch(*args,
                                                                     **kwargs)

    def get_form_kwargs(self):
        """Agrega la :class:`Persona` obtenida como el valor a utilizar en el
        formulario que será llenado posteriormente"""

        kwargs = super(AntecedenteQuirurgicoCreateView, self).get_form_kwargs()
        kwargs.update({'initial': {'persona': self.persona.id}})
        return kwargs

    def form_valid(self, form):
        """Guarda el objeto generado espeficando la :class:`Admision` obtenida
        de los argumentos y el :class:`User` que esta utilizando la aplicación
        """

        self.object = form.save(commit=False)
        self.object.persona = self.persona
        self.object.save()

        messages.info(self.request, u"Agregado Antecedente Quirúrgico")

        return HttpResponseRedirect(self.get_success_url())


class AntecedenteQuirurgicoUpdateView(UpdateView, LoginRequiredMixin):
    """Permite actualizar los datos del :class:`AntecedenteQuirurgico` de una
    :class:`Persona`"""

    model = AntecedenteQuirurgico
    form_class = AntecedenteQuirurgicoForm


class PersonaSearchView(ListView, LoginRequiredMixin):
    context_object_name = 'personas'
    model = Persona
    template_name = 'persona/index.html'
    paginate_by = 10

    def get_queryset(self):
        form = PersonaSearchForm(self.request.GET)

        #if not form.is_valid():
        #    redirect('admision-estadisticas')
        form.is_valid()

        query = form.cleaned_data['query']

        queryset = Persona.objects.filter(
            Q(nombre__icontains=query) |
            Q(apellido__icontains=query) |
            Q(identificacion__icontains=query)
        )

        return queryset.all()


class PersonaMixin(View):
    """Agrega una :class:`Persona` en la vista"""

    def dispatch(self, *args, **kwargs):
        self.persona = get_object_or_404(Persona, pk=kwargs['persona'])
        return super(PersonaMixin, self).dispatch(*args, **kwargs)


class PersonaFormMixin(FormMixin, PersonaMixin):
    """Agrega la :class:`Persona` a los argumentos iniciales de un formulario"""

    def get_initial(self):
        initial = super(PersonaFormMixin, self).get_initial()
        initial = initial.copy()
        initial['persona'] = self.persona.id
        return initial
