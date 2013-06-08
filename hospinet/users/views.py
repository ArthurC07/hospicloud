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
from django.http import HttpResponseRedirect
from django.views.generic import (CreateView, DetailView, UpdateView, ListView,
                                  TemplateView)
from persona.forms import (PersonaForm, FisicoForm, EstiloVidaForm,
    AntecedenteForm, AntecedenteFamiliarForm, AntecedenteObstetricoForm,
    AntecedenteQuirurgicoForm, PersonaSearchForm)
from persona.models import (Persona, Fisico, EstiloVida, Antecedente,
    AntecedenteFamiliar, AntecedenteObstetrico, AntecedenteQuirurgico)
from django.shortcuts import get_object_or_404, redirect
from users.mixins import LoginRequiredMixin