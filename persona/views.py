# -*- coding: utf-8 -*-
"""
Contiene diversas vistas que permiten la presentación y manipulación de datos
en la aplicación.
"""
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, DetailView, UpdateView
from mixins import LoginRequiredView
from persona.forms import (PersonaForm, FisicoForm, EstiloVidaForm,
    AntecedenteForm, AntecedenteFamiliarForm, AntecedenteObstetricoForm,
    AntecedenteQuirurgicoForm)
from persona.models import (Persona, Fisico, EstiloVida, Antecedente,
    AntecedenteFamiliar, AntecedenteObstetrico, AntecedenteQuirurgico)

class PersonaDetailView(DetailView, LoginRequiredView):
    
    """Permite mostrar los datos de una :class:`Persona`"""
    
    context_object_name = 'persona'
    model = Persona
    template_name = 'persona/persona_detail.djhtml'

class PersonaCreateView(CreateView, LoginRequiredView):
    
    """Permite ingresar :class:`Persona`s a la aplicación""" 
    
    form_class = PersonaForm
    template_name = 'persona/nuevo.djhtml'
    
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

class PersonaUpdateView(UpdateView, LoginRequiredView):
    
    """Permite actualizar los datos de una :class:`Persona`"""
    
    model = Persona
    form_class = PersonaForm
    template_name = 'persona/persona_update.djhtml'

class FisicoUpdateView(UpdateView, LoginRequiredView):
    
    """
    Permite actualizar los datos del :class:`Fisico` de una :class:`Persona`
    """
    
    model = Fisico
    form_class = FisicoForm
    template_name = 'persona/fisico_update.djhtml'

class EstiloVidaUpdateView(UpdateView, LoginRequiredView):
    
    """
    Permite actualizar los datos del :class:`EstiloVida` de una :class:`Persona`
    """
    
    model = EstiloVida
    form_class = EstiloVidaForm
    template_name = 'persona/estilo_vida_update.djhtml'

class AntecedenteUpdateView(UpdateView, LoginRequiredView):
    
    model = Antecedente
    form_class = AntecedenteForm
    template_name = 'persona/antecedente_update.djhtml'

class AntecedenteFamiliarUpdateView(UpdateView, LoginRequiredView):
    
    model = AntecedenteFamiliar
    form_class = AntecedenteFamiliarForm
    template_name = 'persona/antecedente_familiar_update.djhtml'

class AntecedenteObstetricoUpdateView(UpdateView, LoginRequiredView):
    
    model = AntecedenteObstetrico
    form_class = AntecedenteObstetricoForm
    template_name = 'persona/antecedente_obstetrico_update.djhtml'

class AntecedenteQuirurgicoCreateView(CreateView, LoginRequiredView):
    
    model = AntecedenteQuirurgico
    form_class = AntecedenteQuirurgicoForm
    template_name = 'persona/antecedente_quirurgico_create.djhtml'

class AntecedenteQuirurgicoUpdateView(UpdateView, LoginRequiredView):
    
    model = AntecedenteQuirurgico
    form_class = AntecedenteQuirurgicoForm
    template_name = 'persona/antecedente_quirurgico_update.djhtml'
