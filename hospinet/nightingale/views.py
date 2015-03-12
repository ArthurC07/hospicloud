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
from django.core.urlresolvers import reverse
from django.db.models.query_utils import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import (ListView, UpdateView, DetailView, CreateView,
                                  RedirectView, DeleteView, FormView)
from django.contrib import messages
from django.utils import timezone
from guardian.decorators import permission_required

from inventory.models import ItemTemplate
from nightingale.forms import (CargoForm, EvolucionForm, GlicemiaForm,
                               HonorarioForm, PreCargoForm,
                               InsulinaForm, GlucosuriaForm, IngestaForm,
                               ExcretaForm, NotaEnfermeriaForm,
                               OrdenMedicaForm, SignoVitalForm,
                               MedicamentoForm, DosisForm, DevolucionForm,
                               SumarioForm, DosificarForm,
                               MedicamentoUpdateForm, OxigenoTerapiaForm)
from nightingale.models import (Cargo, Evolucion, Glicemia, Insulina, Honorario,
                                Glucosuria, Ingesta, Excreta, NotaEnfermeria,
                                OrdenMedica, SignoVital,
                                Medicamento, Dosis, Devolucion, Sumario,
                                OxigenoTerapia)
from spital.models import Admision
# from spital.views import AdmisionFormMixin
from users.mixins import LoginRequiredMixin, CurrentUserFormMixin


class EnfermeriaPermissionMixin(LoginRequiredMixin):
    @method_decorator(permission_required('nightingale.enfermeria'))
    def dispatch(self, *args, **kwargs):
        return super(EnfermeriaPermissionMixin, self).dispatch(*args, **kwargs)


class NightingaleIndexView(ListView, EnfermeriaPermissionMixin):
    """Permite ingresar al lobby de Admisiones que estan siendo atendidas en
    una institucion hospitalaria"""

    queryset = Admision.objects.filter(Q(estado='H'))
    context_object_name = 'admitidos'
    template_name = 'enfermeria/index.html'

    def get_context_data(self, **kwargs):

        context = super(NightingaleIndexView, self).get_context_data(**kwargs)

        admisiones = self.queryset.all()
        context['hospitalizados'] = Admision.objects.filter(Q(estado='I'))
        if self.queryset.count() == 0:
            context['promedio'] = 0
        else:
            context['promedio'] = sum(a.tiempo_hospitalizacion()
                                      for a in
                                      admisiones) / self.queryset.count()

        context['puntos'] = '[0 , 0],' + u','.join('[{0}, {1}]'.format(n + 1,
                                                                       admisiones[
                                                                           n]
                                                                       .tiempo_hospitalizacion())
                                                   for n in
                                                   range(self.queryset.count()))

        return context


class AdmisionListView(ListView, LoginRequiredMixin):
    queryset = Admision.objects.all().order_by('-momento')
    context_object_name = 'admisiones'
    template_name = 'enfermeria/admisiones.html'
    paginate_by = 20


class NotaUpdateView(UpdateView, LoginRequiredMixin):
    """Permite editar una :class:`NotaEnfermeria` en caso de ser necesario"""

    model = NotaEnfermeria
    form_class = NotaEnfermeriaForm
    template_name = 'enfermeria/nota_create.html'


class NotaCerrarView(RedirectView, LoginRequiredMixin):
    """Permite cambiar el estado de un :class:`NotaEnfermeria`"""

    permanent = False

    def get_redirect_url(self, **kwargs):
        """Obtiene la :class:`NotaEnfermeria` desde la base de datos, y la
        marca como cerrada."""

        nota = get_object_or_404(NotaEnfermeria, pk=kwargs['pk'])
        nota.cerrada = True
        nota.save()
        return reverse('enfermeria-notas', args=[nota.admision.id])


class NightingaleDetailView(DetailView, LoginRequiredMixin):
    """Permite ver los datos de una :class:`Admision` desde la interfaz de
    enfermeria
    
    Esta vista se utiliza en conjunto con varias plantillas que permite mostrar
    una diversidad de datos como ser resumenes, :class:`NotaEnfermeria`s,
    :class:`SignoVital`es, :class:`OrdenMedica`s, y todos los demas datos que
    se relacionan con una :class:`Admision` de manera directa.
    """

    model = Admision
    template_name = 'enfermeria/nightingale_detail.html'
    slug_field = 'uuid'

    def get_context_data(self, **kwargs):
        context = super(NightingaleDetailView, self).get_context_data(**kwargs)

        context['fecha'] = timezone.now()

        return context


class SignosDetailView(DetailView, LoginRequiredMixin):
    """Muestra los datos sobre los signos vitales de una :class:`Persona` en
    en una :class:`Admision`"""

    model = Admision
    template_name = 'enfermeria/signos_grafico.html'

    def get_context_data(self, **kwargs):

        """Formatea los datos para ser utilizado las graficas de signos
        vitales
        
        Actualmente se generan gráficas separadas para Pulso y Temperatura; la
        Presión Sistólica y Diastólica comparten una misma gráfica
        """

        context = super(SignosDetailView, self).get_context_data(**kwargs)
        signos = self.object.signos_vitales.extra(
            order_by=['fecha_y_hora']).all()

        context['min'] = self.object.hospitalizacion.strftime('%Y-%m-%d %H:%M')

        if self.object.signos_vitales.count() == 0:
            context['temp_promedio'] = 0
            context['pulso_promedio'] = 0
            context['presion_diastolica_promedio'] = 0
            context['presion_sistolica_promedio'] = 0
        else:
            context['temp_promedio'] = self.object.temperatura_promedio
            context['pulso_promedio'] = self.object.pulso_promedio
            context[
                'presion_diastolica_promedio'] = self.object \
                .presion_diastolica_promedio
            context[
                'presion_sistolica_promedio'] = self.object \
                .presion_sistolica_promedio
            inicio = signos[0].fecha_y_hora - timezone.timedelta(minutes=5)
            context['min'] = inicio.strftime('%Y-%m-%d %H:%M')

        context['pulso'] = u','.join("['{0}', {1}]".format(
            s.fecha_y_hora.strftime('%Y-%m-%d %H:%M'), s.pulso)
                                     for s in signos)
        context['temperatura'] = "['{0}', 37.00], ".format(context['min']) + \
                                 u','.join("['{0}', {1}]".format(
                                     s.fecha_y_hora.strftime('%Y-%m-%d %H:%M'),
                                     s.temperatura)
                                           for s in signos)

        context['presion_sistolica'] = u','.join("['{0}', {1}]".format(
            s.fecha_y_hora.strftime('%Y-%m-%d %H:%M'),
            s.presion_sistolica)
                                                 for s in signos)

        context['presion_diastolica'] = u','.join("['{0}', {1}]".format(
            s.fecha_y_hora.strftime('%Y-%m-%d %H:%M'),
            s.presion_diastolica)
                                                  for s in signos)

        return context


class ResumenDetailView(NightingaleDetailView, SignosDetailView):
    """Muestra la información de una :class:`Admision` de forma totalmente
    consolidada, para evitar grandes saltos de navegación. También permite
    imprimir adecuadamente la historia clínica de la :class:`Persona` admitida
    durante esta :class:`Admision`
    """

    model = Admision
    template_name = 'enfermeria/resumen.html'
    slug_field = 'uuid'


class AdmisionFormMixin(CreateView, CurrentUserFormMixin):
    """Permite llenar el formulario de una clase que requiera
    :class:`Admision`es de manera previa - DRY"""

    def get_context_data(self, **kwargs):
        context = super(AdmisionFormMixin, self).get_context_data(**kwargs)
        context['admision'] = self.admision
        return context

    def get_initial(self):
        """Agrega la :class:`Admision` obtenida como el valor a utilizar en el
        formulario que será llenado posteriormente"""
        initial = super(AdmisionFormMixin, self).get_initial()
        initial = initial.copy()
        initial['fecha_y_hora'] = timezone.now()
        initial['admision'] = self.admision.id
        return initial

    @method_decorator(permission_required('nightingale.enfermeria'))
    def dispatch(self, *args, **kwargs):
        """Obtiene la :class:`Admision` que se entrego como argumento en la
        url"""

        self.admision = get_object_or_404(Admision, pk=kwargs['admision'])
        return super(AdmisionFormMixin, self).dispatch(*args, **kwargs)


class CargoCreateView(AdmisionFormMixin, LoginRequiredMixin):
    """Permite crear un :class:`Cargo` a una :class:`Admision`"""

    model = Cargo
    form_class = CargoForm
    template_name = 'enfermeria/cargo_create.html'

    def form_valid(self, form):
        """Guarda el objeto generado espeficando la :class:`Admision` obtenida
        de los argumentos y el :class:`User` que esta utilizando la aplicación
        """

        self.object = form.save(commit=False)

        item = self.request.user.profile.inventario.buscar_item(
            self.object.cargo)
        item.disminuir(self.object.cantidad)

        self.object.save()

        messages.info(self.request, u"Hospitalización Actualizada")

        return HttpResponseRedirect(self.get_success_url())


class ChosenCargoCreateView(CargoCreateView, LoginRequiredMixin):
    model = Cargo
    form_class = PreCargoForm
    template_name = 'enfermeria/cargo_create.html'

    def get_initial(self):
        initial = super(ChosenCargoCreateView, self).get_initial()
        initial = initial.copy()
        initial['cargo'] = self.cargo.id
        return initial

    def dispatch(self, *args, **kwargs):
        """Obtiene la :class:`Admision` que se entrego como argumento en la
        url"""

        self.cargo = get_object_or_404(ItemTemplate, pk=kwargs['item'])
        return super(ChosenCargoCreateView, self).dispatch(*args, **kwargs)


class CargoDeleteView(DeleteView, LoginRequiredMixin):
    model = Cargo

    def get_object(self, queryset=None):
        obj = super(CargoDeleteView, self).get_object(queryset)
        self.admision = obj.admision
        return obj

    def delete(self, request, *args, **kwargs):
        """
        Calls the delete() method on the fetched object and then
        redirects to the success URL.
        """
        self.object = self.get_object()

        item = self.request.user.profile.inventario.buscar_item(
            self.object.cargo)
        item.incrementar(self.object.cantidad)

        self.object.delete()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return self.admision.get_absolute_url()


class CargoUpdateView(UpdateView, LoginRequiredMixin):
    model = Cargo
    form_class = CargoForm
    template_name = 'enfermeria/cargo_create.html'


class EvolucionCreateView(AdmisionFormMixin):
    """Permite crear un :class:`Evolucion` a una :class:`Admision`"""

    model = Evolucion
    form_class = EvolucionForm
    template_name = 'enfermeria/evolucion_create.html'


class GlicemiaCreateView(AdmisionFormMixin):
    """Permite registrar un :class:`Glicemia` efectuada a una
    :class:`Persona` durante una :class:`Admision`"""

    model = Glicemia
    form_class = GlicemiaForm
    template_name = 'enfermeria/glicemia_create.html'


class InsulinaCreateView(AdmisionFormMixin):
    """Permite crear un dosis de :class:`Insulina` suministrada a una
    :class:`Persona` durante :class:`Admision`"""

    model = Insulina
    form_class = InsulinaForm
    template_name = 'enfermeria/insulina_create.html'


class GlucosuriaCreateView(AdmisionFormMixin):
    """Permite registrar un :class:`Glucosuria` de una :class:`Persona`
    durante una :class:`Admision`"""

    model = Glucosuria
    form_class = GlucosuriaForm
    template_name = 'enfermeria/glucosuria_create.html'


class IngestaCreateView(AdmisionFormMixin):
    """Permite crear un :class:`Examen` a una :class:`Persona`"""

    model = Ingesta
    form_class = IngestaForm
    template_name = 'enfermeria/ingesta_create.html'


class ExcretaCreateView(AdmisionFormMixin):
    """Permite crear un :class:`Examen` a una :class:`Persona`"""

    model = Excreta
    form_class = ExcretaForm
    template_name = 'enfermeria/excreta_create.html'


class NotaCreateView(AdmisionFormMixin):
    """Permite crear un :class:`Examen` a una :class:`Persona`"""

    model = NotaEnfermeria
    form_class = NotaEnfermeriaForm
    template_name = 'enfermeria/nota_create.html'


class OrdenCreateView(AdmisionFormMixin):
    """Permite crear un :class:`Examen` a una :class:`Persona`"""

    model = OrdenMedica
    form_class = OrdenMedicaForm
    template_name = 'enfermeria/orden_create.html'


class SignoVitalCreateView(AdmisionFormMixin):
    """Permite crear un :class:`Examen` a una :class:`Persona`"""

    model = SignoVital
    form_class = SignoVitalForm
    template_name = 'enfermeria/signo_create.html'


class MedicamentoCreateView(AdmisionFormMixin):
    """Permite preescribir un :class:`Medicamento` a una :class:`Admision`"""

    model = Medicamento
    form_class = MedicamentoForm
    template_name = 'enfermeria/medicamento_create.html'

    def get_form_kwargs(self):
        """Agrega la :class:`Admision` obtenida como el valor a utilizar en el
        formulario que será llenado posteriormente"""

        kwargs = super(AdmisionFormMixin, self).get_form_kwargs()
        kwargs.update({'initial': {'admision': self.admision.id,
                                   'inicio': timezone.now(),
                                   'usuario': self.request.user.id}})
        return kwargs


class DosisCreateView(CreateView, LoginRequiredMixin):
    """Permite crear las :class:`Dosis` de un determinado :class:`Medicamento`
    que sera suministrado durante una :class:`Admision`
    
    Esto es agregado manualmente ya que la suministración de
    :class:`Medicamentos` es algo extremadamente subjetivo y varia de
    :class:`Persona` y doctor que lo indica
    """

    model = Dosis
    form_class = DosisForm
    template_name = 'enfermeria/dosis_create.html'

    def get_context_data(self, **kwargs):
        context = super(DosisCreateView, self).get_context_data(**kwargs)
        context['medicamento'] = self.medicamento
        return context

    def get_form_kwargs(self):
        """Agrega el :class:`Medicamento` obtenida como el valor a utilizar
        en el
        formulario que será llenado posteriormente"""

        kwargs = super(DosisCreateView, self).get_form_kwargs()
        kwargs.update({'initial': {'medicamento': self.medicamento.id,
                                   'fecha_y_hora': timezone.now(),
                                   'usuario': self.request.user.id,
                                   'administrador': self.request.user.id}})
        return kwargs

    def dispatch(self, *args, **kwargs):
        """Obtiene la :class:`Admision` que se entrego como argumento en la
        url"""

        self.medicamento = get_object_or_404(Medicamento,
                                             pk=kwargs['medicamento'])
        return super(DosisCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        """Guarda el objeto generado especificando el :class:`Medicamento`
        a ser administrado de los argumentos y el :class:`User` que
        esta utilizando la aplicación
        """

        self.object = form.save(commit=False)
        self.object.medicamento = self.medicamento
        self.usuario = self.request.user
        self.object.save()

        messages.info(self.request, u"Dosis recetada exitósamente")

        return HttpResponseRedirect(self.get_success_url())


class DosisSuministrarView(RedirectView, LoginRequiredMixin):
    """Permite marcar una :class:`Dosis` como ya suministrada"""

    permanent = False

    def get_redirect_url(self, **kwargs):
        """Obtiene la :class:`Dosis` desde la base de datos, la marca como
        suministrada, estampa la hora y el :class:`User` que la suministro"""

        dosis = get_object_or_404(Dosis, pk=kwargs['pk'])
        dosis.estado = kwargs['estado']
        dosis.usuario = self.request.user
        dosis.fecha_y_hora = timezone.now()
        dosis.save()
        messages.info(self.request, u'¡Dosis registrada como suministrada!')
        return reverse('nightingale-view-id',
                       args=[dosis.medicamento.admision.id])


class MedicamentoSuspenderView(RedirectView, LoginRequiredMixin):
    """Permite cambiar el estado de un :class:`Medicamento`"""

    permanent = False

    def get_redirect_url(self, **kwargs):
        """Obtiene el :class:`Medicamento` desde la base de datos, la marca como
        suministrada, estampa la hora y el :class:`User` que la suministro"""

        medicamento = get_object_or_404(Medicamento, pk=kwargs['pk'])
        medicamento.estado = kwargs['estado']
        medicamento.save()
        return reverse('nightingale-view-id', args=[medicamento.admision.id])


class DevolucionCreateView(AdmisionFormMixin):
    model = Devolucion
    form_class = DevolucionForm
    template_name = 'enfermeria/devolucion_create.html'


class SumarioCreateView(AdmisionFormMixin, CurrentUserFormMixin):
    model = Sumario
    form_class = SumarioForm
    template_name = 'enfermeria/sumario.html'


class DosificarMedicamentoView(FormView, LoginRequiredMixin):
    """Permite registrar la dosificación de un :class:`Medicamento` recetado
    al paciente, creando de manera simultanea un :class:`Cargo` que permite
    enviar el cobro a caja"""

    form_class = DosificarForm
    template_name = 'enfermeria/dosificar_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.medicamento = get_object_or_404(Medicamento,
                                             pk=kwargs['medicamento'])
        return super(DosificarMedicamentoView, self).dispatch(request, *args,
                                                              **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DosificarMedicamentoView, self).get_context_data(
            **kwargs)

        context['medicamento'] = self.medicamento

        return context

    def form_valid(self, form):
        if form.is_valid():
            hora = form.cleaned_data['hora']
            self.medicamento.suministrar(hora, self.request.user)

        return super(DosificarMedicamentoView, self).form_valid(form)

    def get_success_url(self):
        return reverse('enfermeria-cargos', args=[self.medicamento.admision.id])


class MedicamentoUpdateView(UpdateView, LoginRequiredMixin):
    model = Medicamento
    form_class = MedicamentoUpdateForm
    context_object_name = 'medicamento'


class OxigenoTerapiaCreateView(AdmisionFormMixin, CurrentUserFormMixin):
    model = OxigenoTerapia
    form_class = OxigenoTerapiaForm


class OxigenoTerapiaUpdateView(UpdateView, LoginRequiredMixin):
    model = OxigenoTerapia
    form_class = OxigenoTerapiaForm
    context_object_name = 'oxigeno_terapia'


class HonorarioCreateView(AdmisionFormMixin, CurrentUserFormMixin):
    model = Honorario
    form_class = HonorarioForm


class HonorarioUpdateView(UpdateView, LoginRequiredMixin):
    model = Honorario
    form_class = HonorarioForm
    context_object_name = 'honorario'


class HonorarioDeleteView(DeleteView, LoginRequiredMixin):
    model = Honorario
