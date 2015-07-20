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
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, CreateView
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.edit import FormMixin
from budget.forms import CuentaForm
from budget.models import Presupuesto, Cuenta
from users.mixins import LoginRequiredMixin


class PresupuestoDetailView(DetailView, LoginRequiredMixin):
    model = Presupuesto
    context_object_name = 'presupuesto'


class PresupuestoMixin(TemplateResponseMixin):
    """Permite obtener un :class:`Cotizacion` desde los argumentos en una url"""

    def dispatch(self, *args, **kwargs):
        self.presupuesto = get_object_or_404(Presupuesto, pk=kwargs['presupuesto'])
        return super(PresupuestoMixin, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PresupuestoMixin, self).get_context_data(**kwargs)

        context['presupuesto'] = self.presupuesto

        return context


class PresupuestoFormMixin(PresupuestoMixin, FormMixin):
    """Permite inicializar el :class:`Presupuesto` que se utilizará en un
    formulario"""

    def get_initial(self):
        initial = super(PresupuestoFormMixin, self).get_initial()
        initial = initial.copy()
        initial['presupuesto'] = self.presupuesto
        return initial


class CuentaDetailView(DetailView, LoginRequiredMixin):
    model = Cuenta
    context_object_name = 'cuenta'


class CuentaCreateView(PresupuestoFormMixin, CreateView, LoginRequiredMixin):
    model = Cuenta
    form_class = CuentaForm


class CuentaMixin(TemplateResponseMixin):
    """Permite obtener un :class:`Cotizacion` desde los argumentos en una url"""

    def dispatch(self, *args, **kwargs):
        self.cuenta = get_object_or_404(Cuenta, pk=kwargs['cuenta'])
        return super(CuentaMixin, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CuentaMixin, self).get_context_data(**kwargs)

        context['cuenta'] = self.cuenta

        return context


class CuentaFormMixin(CuentaMixin, FormMixin):
    """Permite inicializar el :class:`Presupuesto` que se utilizará en un
    formulario"""

    def get_initial(self):
        initial = super(CuentaFormMixin, self).get_initial()
        initial = initial.copy()
        initial['cuenta'] = self.cuenta
        return initial
