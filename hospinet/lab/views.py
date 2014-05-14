# -*- coding: utf-8 -*-
#
# Copyright (C) 2014 Carlos Flores <cafg10@gmail.com>
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
from django.utils.decorators import method_decorator

from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from guardian.decorators import permission_required
from lab.forms import ResultadoForm
from lab.models import Resultado
from persona.forms import PersonaSearchForm
from persona.views import PersonaFormMixin
from users.mixins import LoginRequiredMixin


class LabPermissionMixin(LoginRequiredMixin):
    @method_decorator(permission_required('lab.lab'))
    def dispatch(self, *args, **kwargs):
        return super(LabPermissionMixin, self).dispatch(*args, **kwargs)


class IndexView(TemplateView):
    template_name = 'lab/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['searchform'] = PersonaSearchForm()
        context['searchform'].helper.form_action = 'lab-search'
        return context


class ResultadoCreateView(PersonaFormMixin, CreateView, LoginRequiredMixin):
    model = Resultado
    form_class = ResultadoForm


class ResultadoUpdateView(UpdateView, LoginRequiredMixin):
    model = Resultado
    form_class = ResultadoForm


class ResultadoDeleteView(DeleteView, LoginRequiredMixin):
    model = Resultado

    def get_object(self, queryset=None):
        obj = super(ResultadoDeleteView, self).get_object(queryset)
        self.persona = obj.persona
        return obj

    def get_success_url(self):
        return self.persona.get_absolute_url()
