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

"""
Contiene diversas vistas que permiten la presentación y manipulación de datos
en la aplicación.
"""
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, DetailView, UpdateView, ListView
from persona.forms import (PersonaForm, FisicoForm, EstiloVidaForm,
    AntecedenteForm, AntecedenteFamiliarForm, AntecedenteObstetricoForm,
    AntecedenteQuirurgicoForm)
from persona.models import (Persona, Fisico, EstiloVida, Antecedente,
    AntecedenteFamiliar, AntecedenteObstetrico, AntecedenteQuirurgico)
from django.shortcuts import get_object_or_404
from persona.mixins import LoginRequiredMixin

class PersonaIndexView(ListView, LoginRequiredMixin):
    
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
    template_name = 'persona/nuevo.html'
    
    def form_valid(self, form):
        
        """Se ejecuta si los datos del formulario son correctos
        
        En el caso que la :class:`Persona` halla sido creada correctamente, se
        agregan los datos del físico y del estilo de vida a la :class:`Persona`
        para que luego sean editados posteriormente.
        
        Adicionalmente crea un :class:`Antecedente` y un
        :class:`AntecedenteFamiliar para la misma :class:`Persona`, en caso de
        ser un paciente mujer, se crea el :class:`AntecedenteObstetrico`
        """
        
        super(PersonaCreateView, self).form_valid(form)
        fisico = Fisico(persona=self.object)
        fisico.save()
        estilo_vida = EstiloVida(persona=self.object)
        estilo_vida.save()
        antecedente = Antecedente(persona=self.object)
        antecedente.save()
        antecedente_familiar = AntecedenteFamiliar(persona=self.object)
        antecedente_familiar.save()
        
        if self.object.sexo == 'F':
            antecedente_obstetrico = AntecedenteObstetrico(persona=self.object)
            antecedente_obstetrico.save()
        
        return HttpResponseRedirect(self.get_success_url())

class PersonaUpdateView(UpdateView, LoginRequiredMixin):
    
    """Permite actualizar los datos de una :class:`Persona`"""
    
    model = Persona
    form_class = PersonaForm
    template_name = 'persona/persona_update.html'

class FisicoUpdateView(UpdateView, LoginRequiredMixin):
    
    """
    Permite actualizar los datos del :class:`Fisico` de una :class:`Persona`
    """
    
    model = Fisico
    form_class = FisicoForm
    template_name = 'persona/fisico_update.html'

class EstiloVidaUpdateView(UpdateView, LoginRequiredMixin):
    
    """Permite actualizar los datos del :class:`EstiloVida` de una
    :class:`Persona`"""
    
    model = EstiloVida
    form_class = EstiloVidaForm
    template_name = 'persona/estilo_vida_update.html'

class AntecedenteUpdateView(UpdateView, LoginRequiredMixin):
    
    """Permite actualizar los datos del :class:`Antecedente` de una
    :class:`Persona`"""
    
    model = Antecedente
    form_class = AntecedenteForm
    template_name = 'persona/antecedente_update.html'

class AntecedenteFamiliarUpdateView(UpdateView, LoginRequiredMixin):
    
    """Permite actualizar los datos del :class:`AntecedenteFamiliar` de una
    :class:`Persona`"""
    
    model = AntecedenteFamiliar
    form_class = AntecedenteFamiliarForm
    template_name = 'persona/antecedente_familiar_update.html'

class AntecedenteObstetricoUpdateView(UpdateView, LoginRequiredMixin):
    
    """Permite actualizar los datos del :class:`AntecedenteObstetrico` de una
    :class:`Persona`"""
    
    model = AntecedenteObstetrico
    form_class = AntecedenteObstetricoForm
    template_name = 'persona/antecedente_obstetrico_update.html'

class AntecedenteQuirurgicoCreateView(CreateView, LoginRequiredMixin):
    
    """Permite actualizar los datos del :class:`AntecedenteQuirurgico` de una
    :class:`Persona`"""
    
    model = AntecedenteQuirurgico
    form_class = AntecedenteQuirurgicoForm
    template_name = 'persona/antecedente_quirurgico_create.html'

    def get_context_data(self, **kwargs):
        
        context = super(AntecedenteQuirurgicoCreateView, self).get_context_data(**kwargs)
        context['persona'] = self.persona
        return context

    def dispatch(self, *args, **kwargs):
        
        """Obtiene la :class:`Persona` que se entrego como argumento en la
        url"""

        self.persona = get_object_or_404(Persona, pk=kwargs['pk'])
        return super(AntecedenteQuirurgicoCreateView, self).dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        
        """Agrega la :class:`Persona` obtenida como el valor a utilizar en el
        formulario que será llenado posteriormente"""

        kwargs = super(AntecedenteQuirurgicoCreateView, self).get_form_kwargs()
        kwargs.update({'initial':{'persona':self.persona.id}})
        return kwargs
    
    def form_valid(self, form):
        
        """Guarda el objeto generado espeficando la :class:`Admision` obtenida
        de los argumentos y el :class:`User` que esta utilizando la aplicación
        """

        self.object = form.save(commit=False)
        self.object.persona = self.persona
        self.object.save()
        
        #messages.info(self.request, u"Agregado Antecedente Quirúrgico")
        
        return HttpResponseRedirect(self.get_success_url())

class AntecedenteQuirurgicoUpdateView(UpdateView, LoginRequiredMixin):
    
    """Permite actualizar los datos del :class:`AntecedenteQuirurgico` de una
    :class:`Persona`"""
    
    model = AntecedenteQuirurgico
    form_class = AntecedenteQuirurgicoForm
    template_name = 'persona/antecedente_quirurgico_update.html'
