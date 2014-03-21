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
from collections import defaultdict
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import (DetailView, CreateView, View,
                                  ListView, UpdateView)
from django.views.generic.detail import SingleObjectMixin
from django.shortcuts import get_object_or_404
from django.views.generic.edit import FormMixin
from guardian.decorators import permission_required

from clinique.forms import (PacienteForm, CitaForm, EvaluacionForm,
                            ConsultaForm, SeguimientoForm, LecturaSignosForm,
                            DiagnosticoClinicoForm, ConsultorioForm,
                            CitaPersonaForm, CargoForm, OrdenMedicaForm,
                            NotaEnfermeriaForm)
from clinique.models import (Paciente, Cita, Consulta, Evaluacion,
                             Seguimiento, LecturaSignos, Consultorio,
                             DiagnosticoClinico, Cargo, OrdenMedica,
                             NotaEnfermeria)
from persona.forms import PersonaSearchForm, FisicoForm, AntecedenteForm, \
    AntecedenteFamiliarForm, AntecedenteObstetricoForm, \
    AntecedenteQuirurgicoForm, EstiloVidaForm, PersonaForm
from persona.models import Fisico, Antecedente, AntecedenteFamiliar, \
    AntecedenteObstetrico, AntecedenteQuirurgico, EstiloVida, Persona
from persona.views import PersonaFormMixin
from users.mixins import LoginRequiredMixin, CurrentUserFormMixin


class ConsultorioPermissionMixin(LoginRequiredMixin):
    @method_decorator(permission_required('clinique.consultorio'))
    def dispatch(self, *args, **kwargs):
        return super(ConsultorioPermissionMixin, self).dispatch(*args, **kwargs)


class ConsultorioIndexView(ListView, ConsultorioPermissionMixin):
    template_name = 'clinique/index.html'
    paginate_by = 20
    context_object_name = 'pacientes'

    def get_queryset(self):
        return Paciente.objects.filter(
            consultorio__usuario=self.request.user).all()

    def get_context_data(self, **kwargs):
        context = super(ConsultorioIndexView, self).get_context_data(**kwargs)

        if self.request.user.is_staff:
            context['consultorios'] = Consultorio.objects.all()

        return context


class ConsultorioDetailView(SingleObjectMixin, ListView, LoginRequiredMixin):
    paginate_by = 20
    template_name = 'clinique/consultorio_detail.html'

    def get_context_data(self, **kwargs):
        kwargs['consultorio'] = self.object
        kwargs['buscar'] = PersonaSearchForm()
        kwargs['buscar'].helper.form_action = 'persona-search'
        return super(ConsultorioDetailView, self).get_context_data(**kwargs)

    def get_queryset(self):
        self.object = self.get_object(Consultorio.objects.all())
        return self.object.pacientes.all()


class ConsultorioCreateView(CurrentUserFormMixin, CreateView):
    model = Consultorio
    form_class = ConsultorioForm


class ConsultorioMixin(View):
    def dispatch(self, *args, **kwargs):
        self.consultorio = get_object_or_404(Consultorio,
                                             pk=kwargs['consultorio'])
        return super(ConsultorioMixin, self).dispatch(*args, **kwargs)


class ConsultorioFormMixin(ConsultorioMixin):
    def get_initial(self):
        initial = super(ConsultorioFormMixin, self).get_initial()
        initial = initial.copy()
        initial['consultorio'] = self.consultorio.id
        return initial


class PacienteCreateView(CreateView, PersonaFormMixin, ConsultorioFormMixin,
                         LoginRequiredMixin):
    """Permite agregar una :class:`Persona` como un :class:`Paciente` de un
    doctor que tiene un :class:`User` en el sistema"""

    model = Paciente
    form_class = PacienteForm


class PacienteDetailView(DetailView, LoginRequiredMixin):
    """Permite ver los datos del :class"`Paciente` en la interfaz gráfica"""

    model = Paciente
    context_object_name = 'paciente'


class PacienteMixin(View):
    """Permite obtener un :class:`Paciente` desde los argumentos en una url"""

    def dispatch(self, *args, **kwargs):
        self.paciente = get_object_or_404(Paciente, pk=kwargs['paciente'])
        return super(PacienteMixin, self).dispatch(*args, **kwargs)


class PacienteFormMixin(FormMixin, PacienteMixin):
    """Permite inicializar el paciente que se utilizará en un formulario"""

    def get_initial(self):
        initial = super(PacienteFormMixin, self).get_initial()
        initial = initial.copy()
        initial['paciente'] = self.paciente
        return initial


class CitaCreateView(CreateView, LoginRequiredMixin):
    model = Cita
    form_class = CitaForm


class CitaPersonaCreateView(CreateView, PersonaFormMixin, LoginRequiredMixin):
    model = Cita
    form_class = CitaPersonaForm


class CitaListView(ConsultorioMixin, ListView, LoginRequiredMixin):
    model = Cita
    context_object_name = 'citas'

    def get_queryset(self):
        self.citas = Cita.objects.filter(consultorio=self.consultorio,
                                         fecha__gte=timezone.now())

        return self.citas.all()

    def get_context_data(self, **kwargs):
        context = super(CitaListView, self).get_context_data(**kwargs)
        context['consultorio'] = self.consultorio

        fechas = defaultdict(list)

        for cita in self.citas.all():
            fechas[cita.fecha.date()].append(cita)

        context['fechas'] = fechas.iteritems()
        return context


class EvaluacionCreateView(PacienteFormMixin, LoginRequiredMixin, CreateView):
    model = Evaluacion
    form_class = EvaluacionForm


class ConsultaCreateView(PacienteFormMixin, CurrentUserFormMixin, CreateView,
                         LoginRequiredMixin):
    model = Consulta
    form_class = ConsultaForm


class SeguimientoCreateView(PacienteFormMixin, CurrentUserFormMixin, CreateView,
                            LoginRequiredMixin):
    model = Seguimiento
    form_class = SeguimientoForm


class LecturaSignosCreateView(PersonaFormMixin, ConsultorioMixin,
                              LoginRequiredMixin, CreateView):
    model = LecturaSignos
    form_class = LecturaSignosForm

    def get_success_url(self):

        paciente = Paciente.objects.filter(persona=self.object.persona,
                                           consultorio=self.consultorio).first()
        if paciente is None:
            paciente = Paciente()
            paciente.persona = self.object.persona
            paciente.consultorio = self.consultorio
            paciente.save()

        return paciente.get_absolute_url()


class DiagnosticoCreateView(PacienteFormMixin, LoginRequiredMixin, CreateView):
    model = DiagnosticoClinico
    form_class = DiagnosticoClinicoForm


class CliniquePersonaUpdateView(UpdateView, LoginRequiredMixin):
    model = Persona
    form_class = PersonaForm
    template_name = 'clinique/persona_update.html'

    def get_success_url(self):
        return reverse('clinique-fisico-editar', args=[self.object.id])


class CliniqueFisicoUpdateView(UpdateView, LoginRequiredMixin):
    """
    Permite actualizar los datos del :class:`Fisico` de una :class:`Persona`
    """

    model = Fisico
    form_class = FisicoForm
    template_name = 'clinique/fisico_update.html'

    def get_success_url(self):
        return reverse('clinique-antecedente-editar',
                       args=[self.object.persona.id])


class CliniqueAntecedenteUpdateView(UpdateView, LoginRequiredMixin):
    """Permite actualizar los datos del :class:`Antecedente` de una
    :class:`Persona`"""

    model = Antecedente
    form_class = AntecedenteForm
    template_name = 'clinique/antecedente_update.html'

    def get_success_url(self):
        return reverse('clinique-antecedente-familiar-editar',
                       args=[self.object.persona.id])


class CliniqueAntecedenteFamiliarUpdateView(UpdateView, LoginRequiredMixin):
    """Permite actualizar los datos del :class:`AntecedenteFamiliar` de una
    :class:`Persona`"""

    model = AntecedenteFamiliar
    form_class = AntecedenteFamiliarForm
    template_name = 'clinique/antecedente_familiar_update.html'

    def get_success_url(self):
        return reverse('clinique-estilovida-editar',
                       args=[self.object.persona.id])


class CliniqueAntecedenteObstetricoUpdateView(UpdateView, LoginRequiredMixin):
    """Permite actualizar los datos del :class:`AntecedenteObstetrico` de una
    :class:`Persona`"""

    model = AntecedenteObstetrico
    form_class = AntecedenteObstetricoForm
    template_name = 'clinique/antecedente_obstetrico_update.html'


class CliniqueAntecedenteQuirurgicoUpdateView(UpdateView, LoginRequiredMixin):
    """Permite actualizar los datos del :class:`AntecedenteQuirurgico` de una
    :class:`Persona`"""

    model = AntecedenteQuirurgico
    form_class = AntecedenteQuirurgicoForm
    template_name = 'clinique/antecedente_quirurgico_update.html'

    def get_success_url(self):
        return reverse('clinique-antecedente-editar',
                       args=[self.object.persona.id])


class CliniqueAntecedenteQuirurgicoCreateView(CreateView, PersonaFormMixin,
                                              PacienteMixin,
                                              LoginRequiredMixin):
    model = AntecedenteQuirurgico
    form_class = AntecedenteQuirurgicoForm
    template_name = 'clinique/antecedente_quirurgico_create.html'

    def get_success_url(self):
        return reverse('clinique-paciente', args=[self.paciente.id])


class CliniqueEstiloVidaUpdateView(UpdateView, LoginRequiredMixin):
    """Permite actualizar los datos del :class:`EstiloVida` de una
    :class:`Persona`"""

    model = EstiloVida
    form_class = EstiloVidaForm
    template_name = 'clinique/estilo_vida_update.html'


class CargoCreateView(PacienteFormMixin, CreateView, LoginRequiredMixin):
    model = Cargo
    form_class = CargoForm


class OrdenMedicaCreateView(PacienteFormMixin, CreateView, LoginRequiredMixin):
    model = OrdenMedica
    form_class = OrdenMedicaForm


class NotaEnfermeriaCreateView(PacienteFormMixin, CreateView,
                               CurrentUserFormMixin):
    model = NotaEnfermeria
    form_class = NotaEnfermeriaForm
