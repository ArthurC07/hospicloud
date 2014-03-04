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

from datetime import datetime, time
from django.contrib.auth.decorators import permission_required

from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views.generic import (CreateView, ListView, TemplateView,
                                  DeleteView,
                                  DetailView, RedirectView, UpdateView)
from django.contrib import messages
from crispy_forms.layout import Fieldset

from persona.models import Persona
from persona.views import PersonaCreateView
from spital.forms import (AdmisionForm, HabitacionForm, PreAdmisionForm,
                          IngresarForm, DepositoForm)
from spital.models import Admision, Habitacion, PreAdmision, Deposito
from nightingale.models import Cargo
from emergency.models import Emergencia
from persona.forms import PersonaForm, PersonaSearchForm
from users.mixins import LoginRequiredMixin
from invoice.forms import PeriodoForm


class AdmisionPermissionMixin(LoginRequiredMixin):
    @method_decorator(permission_required('spital.admision'))
    def dispatch(self, *args, **kwargs):
        return super(AdmisionPermissionMixin, self).dispatch(*args, **kwargs)


class AdmisionIndexView(ListView, AdmisionPermissionMixin):
    """Muestra la pagina principal de el Centro de :class:`Admisiones`"""

    context_object_name = 'admisiones'
    queryset = Admision.objects.filter(~Q(estado='H') & ~Q(estado='C')
                                       & ~Q(estado='I'))
    template_name = 'admision/index.html'

    def get_context_data(self, **kwargs):

        """Realiza los calculos para mostrar el gráfico de tiempo de espera
        de las :class:`Admision`es"""

        context = super(AdmisionIndexView, self).get_context_data(**kwargs)

        context['preadmisiones'] = PreAdmision.objects.filter(completada=False)
        context['admision_periodo'] = PeriodoForm(prefix='admisiones')
        context[
            'admision_periodo'].helper.form_action = 'estadisticas-hospitalizacion'
        context['admision_periodo'].helper.layout = Fieldset(
            u'Admisiones por Periodo',
            *context['admision_periodo'].field_names)
        return context


class AdmisionFormMixin(CreateView):
    def dispatch(self, *args, **kwargs):
        """Obtiene la :class:`Admision` desde la url"""

        self.admision = get_object_or_404(Admision, pk=kwargs['admision'])
        return super(AdmisionFormMixin, self).dispatch(*args, **kwargs)

    def get_initial(self):
        """Agrega la :class:`Admision` a los campos del formulario"""

        initial = super(AdmisionFormMixin, self).get_initial()
        initial = initial.copy()
        initial['admision'] = self.admision.id
        return initial

    def get_context_data(self, **kwargs):
        context = super(AdmisionFormMixin, self).get_context_data(**kwargs)
        context['admision'] = self.admision
        return context


class IngresarView(TemplateView, LoginRequiredMixin):
    """Muestra una interfaz para agregar una :class:`Admision` ya sea agregando
    una :class:`Persona` nueva o admitiendo una que ya se encuentra en el
    sistema"""

    template_name = 'admision/ingresar.html'

    def get_context_data(self, **kwargs):
        """Agrega el formulario para crear una :class:`Persona` desde la misma
        página"""

        context = super(IngresarView, self).get_context_data()
        context['persona_search_form'] = PersonaSearchForm()
        context['persona_form'] = PersonaForm()
        context['persona_form'].helper.form_action = 'admision-ingresar-persona'
        return context


class PersonaAdmisionCreateView(PersonaCreateView):
    """Permite admitir una :class:`Persona` preexistente"""

    template_name = 'admision/persona_create.html'

    def get_success_url(self):
        return reverse('admision-persona-agregar', args=[self.object.id])


class PersonaFiadorCreateView(PersonaCreateView):
    """Permite ingresar una :class:`Persona` al sistema que servira como
    :class:`Fiador` a una :class:`Admision`"""

    template_name = 'admision/admision_fiador.html'

    def dispatch(self, *args, **kwargs):
        """Carga la :class:`Admision` desde la fuente de datos"""

        self.admision = get_object_or_404(Admision, pk=kwargs['admision'])
        return super(PersonaFiadorCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        """Agrega la :class:`Persona` a la lista de fiadores de la
        :class:`Admision`"""

        self.object = form.save()
        self.admision.fiadores.add(self.object)
        self.admision.save()
        messages.info(self.request, u"Agregado un Fiador!")

        return HttpResponseRedirect(self.admision.get_absolute_url())

    def get_context_data(self, **kwargs):
        context = super(PersonaFiadorCreateView, self).get_context_data(
            **kwargs)
        context['admision'] = self.admision
        return context


class PersonaReferenciaCreateView(PersonaCreateView):
    """Permite agregar una :class:`Persona` como referencia a una
    :class:`Admision`"""

    template_name = 'admision/admision_referencia.html'

    def dispatch(self, *args, **kwargs):
        """Carga la :class:`Admision` desde la fuente de datos"""

        self.admision = get_object_or_404(Admision, pk=kwargs['admision'])
        return super(PersonaReferenciaCreateView, self).dispatch(*args,
                                                                 **kwargs)

    def form_valid(self, form):
        """Agrega la :class:`Persona` a la lista de referencias de la
        :class:`Admision`"""

        self.object = form.save()
        self.admision.referencias.add(self.object)
        self.admision.save()
        messages.info(self.request, u"Agregada Referencia!")

        return HttpResponseRedirect(self.admision.get_absolute_url())

    def get_context_data(self, **kwargs):
        context = super(PersonaReferenciaCreateView, self).get_context_data(
            **kwargs)
        context['admision'] = self.admision
        return context


class ReferenciaAgregarView(RedirectView, LoginRequiredMixin):
    """Permite agregar una :class:`Persona` como referencia de una
    :class:`Admision`"""

    url = '/admision/referencia/agregar'

    def get_redirect_url(self, **kwargs):
        admision = get_object_or_404(Admision, pk=kwargs['admision'])
        persona = get_object_or_404(Persona, pk=kwargs['persona'])
        admision.referencias.add(persona)
        admision.save()
        return reverse('admision-view-id', args=[admision.id])


class FiadorAgregarView(RedirectView, LoginRequiredMixin):
    """Permite agregar una :class:`Persona` como fiador de una
    :class:`Admision`"""

    url = '/admision/fiador/agregar'

    def get_redirect_url(self, **kwargs):
        admision = get_object_or_404(Admision, pk=kwargs['admision'])
        persona = get_object_or_404(Persona, pk=kwargs['persona'])
        admision.fiadores.add(persona)
        admision.save()
        return reverse('admision-view-id', args=[admision.id])


class AdmisionCreateView(CreateView, LoginRequiredMixin):
    """Crea una :class:`Admision` para una :class:`Persona` ya existente en el
    sistema"""

    model = Admision
    form_class = AdmisionForm
    template_name = 'admision/admision_create.html'

    def get_form_kwargs(self):
        """Agrega el id de la :class:`Persona` a los argumentos de la sesión"""

        kwargs = super(AdmisionCreateView, self).get_form_kwargs()
        kwargs.update({'initial': {'paciente': self.persona.id}})
        return kwargs

    def dispatch(self, *args, **kwargs):
        """Carga la :class:`Persona` desde el origen de datos"""

        self.persona = get_object_or_404(Persona, pk=kwargs['persona'])
        return super(AdmisionCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        """Agrega la :class:`Persona que se esta admitiendo y el :class:`User`
        que esta realizando la :class:`Admision`"""

        self.object = form.save(commit=False)
        self.object.persona = self.persona
        self.object.admitio = self.request.user
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


class AdmisionDetailView(DetailView, LoginRequiredMixin):
    """Permite mostrar los datos de una :class:`Admision`"""

    context_object_name = 'admision'
    model = Admision
    template_name = 'admision/admision_detail.html'
    slug_field = 'uuid'


class AutorizarView(RedirectView, LoginRequiredMixin):
    """Permite marcar como autorizada una :class:`Admision`"""

    url = '/admision/autorizar'
    permanent = False

    def get_redirect_url(self, **kwargs):
        admision = get_object_or_404(Admision, pk=kwargs['pk'])
        admision.autorizar()
        messages.info(self.request, u'¡Admision Autorizada!')
        return reverse('admision-view-id', args=[admision.id])


class PagarView(RedirectView, LoginRequiredMixin):
    """Permite marcar como pagada una :class:`Admision`"""

    url = '/admision/hospitalizar'
    permanent = False

    def get_redirect_url(self, **kwargs):
        admision = get_object_or_404(Admision, pk=kwargs['pk'])
        admision.pagar()
        messages.info(self.request, u'¡Registrado el pago de la Admision!')
        return reverse('admision-view-id', args=[admision.id])


class AdmisionPeriodoView(TemplateView, LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):

        """Filtra las :class:`Admision` de acuerdo a los datos ingresados en
        el formulario"""

        self.form = PeriodoForm(request.GET, prefix='admisiones')
        if self.form.is_valid():

            inicio = self.form.cleaned_data['inicio']
            fin = self.form.cleaned_data['fin']
            self.inicio = datetime.combine(inicio, time.min)
            self.fin = datetime.combine(fin, time.max)
            self.admisiones = Admision.objects.filter(
                admision__range=(inicio, fin))

        else:

            return redirect('admision-index')

        return super(AdmisionPeriodoView, self).dispatch(request, *args,
                                                         **kwargs)

    def get_context_data(self, **kwargs):

        context = super(AdmisionPeriodoView, self).get_context_data(**kwargs)
        context['inicio'] = self.inicio
        context['fin'] = self.fin
        context['admisiones'] = self.admisiones

        return context


class HabitacionListView(ListView, LoginRequiredMixin):
    """Muestra la lista de las :class:`Habitacion`es para tener una vista
    rápida de las que se encuentran disponibles en un determinado momento"""

    context_object_name = 'habitaciones'
    queryset = Habitacion.objects
    template_name = 'admision/habitaciones.html'


class HabitacionCreateView(CreateView, LoginRequiredMixin):
    """Permite agregar una :class:`Habitacion` al :class:`Hospital`"""

    model = Habitacion
    form_class = HabitacionForm
    template_name = 'admision/habitacion_create.html'


class HabitacionDetailView(DetailView, LoginRequiredMixin):
    """Permite mostrar el estado de una :class:`Habitacion`"""

    context_object_name = 'habitacion'
    model = Habitacion
    template_name = 'admision/habitacion_detail.html'

    def get_context_data(self, **kwargs):

        """Permite paginar las admisiones que la :class:`Habitacion` ha
        recibido a lo largo del tiempo"""

        context = super(HabitacionDetailView, self).get_context_data(**kwargs)

        paginator = Paginator(self.object.admisiones, 10)
        try:
            page = int(self.request.GET.get("page", '1'))
        except ValueError:
            page = 1

        try:
            context['admisiones'] = paginator.page(page)
        except (InvalidPage, EmptyPage):
            context['admisiones'] = paginator.page(paginator.num_pages)

        return context


class HabitacionUpdateView(UpdateView, LoginRequiredMixin):
    """Permite editar los datos de una :class:`Habitacion`"""

    model = Habitacion
    form_class = HabitacionForm
    template_name = 'admision/habitacion_create.html'


class PreAdmisionCreateView(CreateView, LoginRequiredMixin):
    model = PreAdmision
    form_class = PreAdmisionForm

    def get_form_kwargs(self):
        """Agrega el id de la :class:`Persona` a los argumentos de la sesión"""

        kwargs = super(PreAdmisionCreateView, self).get_form_kwargs()
        kwargs.update({'initial': {'emergencia': self.emergencia.id}})
        return kwargs

    def dispatch(self, *args, **kwargs):
        """Carga la :class:`Persona` desde el origen de datos"""

        self.emergencia = get_object_or_404(Emergencia, pk=kwargs['emergencia'])
        return super(PreAdmisionCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        """Agrega la :class:`Persona que se esta admitiendo y el :class:`User`
        que esta realizando la :class:`Admision`"""

        self.object = form.save(commit=False)
        self.object.persona = self.emergencia.persona
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(PreAdmisionCreateView, self).get_context_data(**kwargs)

        context['emergencia'] = self.emergencia

        return context


class AdmisionPreCreateView(CreateView, LoginRequiredMixin):
    """Crea una :class:`Admision` para una :class:`Persona` ya existente en el
    sistema"""

    model = Admision
    form_class = AdmisionForm
    template_name = 'admision/admision_precreate.html'

    def get_form_kwargs(self):

        """Agrega el id de la :class:`Persona` a los argumentos de la sesión"""

        kwargs = super(AdmisionPreCreateView, self).get_form_kwargs()
        kwargs.update(
            {'initial': {'paciente': self.preadmision.emergencia.persona.id}})
        return kwargs

    def dispatch(self, *args, **kwargs):

        """Carga la :class:`Persona` desde el origen de datos"""

        self.preadmision = get_object_or_404(PreAdmision,
                                             pk=kwargs['preadmision'])
        return super(AdmisionPreCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):

        """Agrega la :class:`Persona que se esta admitiendo y el :class:`User`
        que esta realizando la :class:`Admision`"""

        self.object = form.save(commit=False)
        self.object.persona = self.preadmision.emergencia.persona
        self.object.admitio = self.request.user
        self.preadmision.completada = True
        self.object.save()
        if self.preadmision.transferir_cobros:

            for cobro in self.preadmision.emergencia.cobros.all():
                cargo = Cargo()
                cargo.admision = self.object
                cargo.cargo = cobro.cargo
                cargo.cantidad = cobro.cantidad
                cargo.save()

        self.preadmision.save()

        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):

        """Realiza los calculos para mostrar el gráfico de tiempo de espera
        de las :class:`Admision`es"""

        context = super(AdmisionPreCreateView, self).get_context_data(**kwargs)

        context['preadmision'] = self.preadmision

        return context


class PreAdmisionDeleteView(DeleteView, LoginRequiredMixin):
    model = PreAdmision

    def get_success_url(self):

        return reverse('admision-index')


class HospitalizarView(UpdateView, LoginRequiredMixin):
    """Permite actualizar los datos de ingreso en la central de enfermeria"""

    model = Admision
    form_class = IngresarForm
    template_name = 'enfermeria/ingresar.html'

    def get_success_url(self):
        self.object.hospitalizar()
        self.object.ingresar()
        messages.info(self.request, u'¡Admision Enviada a Enfermeria!')
        return reverse('nightingale-view-id', args=[self.object.id])


class AdmisionDeleteView(DeleteView, LoginRequiredMixin):
    model = Admision

    def get_success_url(self):
        return reverse('admision-index')


class DepositoCreateView(AdmisionFormMixin):
    model = Deposito
    form_class = DepositoForm


class DepositoUpdateView(UpdateView, LoginRequiredMixin):
    model = Deposito
    form_class = DepositoForm
