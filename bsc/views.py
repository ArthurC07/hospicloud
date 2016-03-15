# -*- coding: utf-8 -*-
#
# Copyright (C) 2015 - 2016 Carlos Flores <cafg10@gmail.com>
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

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import connections
from django.db.models import Avg, Count
from django.db.models.functions import Coalesce
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView, DetailView, CreateView, UpdateView, \
    RedirectView, View
from django.views.generic.base import ContextMixin
from django.views.generic.edit import FormMixin
from mail_templated.message import EmailMessage

from bsc.forms import RespuestaForm, VotoForm, VotoFormSet, QuejaForm, \
    ArchivoNotasForm, SolucionForm, RellamarForm, SolucionRechazadaForm, \
    SolucionAceptadaForm, QuejaAseguradoraForm
from bsc.models import ScoreCard, Encuesta, Respuesta, Voto, Queja, \
    ArchivoNotas, Pregunta, Solucion, Login, Rellamar
from clinique.models import Consulta
from clinique.views import ConsultaFormMixin
from hospinet.utils.date import make_day_start, make_end_day, make_month_range
from hospinet.utils.forms import PeriodoForm
from hospinet.utils.views import PeriodoView
from users.mixins import LoginRequiredMixin, CurrentUserFormMixin


class ScoreCardListView(LoginRequiredMixin, ListView):
    """
    Shows a list with all the distinct :class:`ScoreCard` added to the database
    """
    model = ScoreCard

    def get_context_data(self, **kwargs):
        context = super(ScoreCardListView, self).get_context_data(**kwargs)

        context['loginperiodo'] = PeriodoForm(prefix='login')
        context['loginperiodo'].set_legend(
            _('Inicios de Sesi&oacute;n por Periodo')
        )
        context['loginperiodo'].set_action('login-periodo')

        return context


class ScoreCardDetailView(LoginRequiredMixin, DetailView):
    """
    Displays detailed data about a :class:`ScoreCard and all its related
    information
    """
    model = ScoreCard


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'bsc/user.html'


class EncuestaListView(LoginRequiredMixin, ListView):
    """
    Shows the main interface for the :class:`Encuesta` procedures
    """
    model = Encuesta
    queryset = Encuesta.objects.filter(
        activa=True,
    )

    def get_context_data(self, **kwargs):
        """
        Adds the needed data to create the statistics table and the chart about
        those statistics
        """
        context = super(EncuestaListView, self).get_context_data(**kwargs)

        meses = []
        now = timezone.now()

        for n in range(1, 13):
            start = now.replace(month=n, day=1)

            inicio, fin = make_month_range(start)

            consultas = Consulta.objects.atendidas(inicio, fin)

            atenciones = consultas.count()
            encuestadas = consultas.filter(encuestada=True).count()

            if atenciones == 0:
                contactabilidad = 0
            else:
                contactabilidad = encuestadas * 100 / atenciones

            satisfaccion = Voto.objects.filter(
                opcion__isnull=False,
                created__range=(inicio, fin),
                pregunta__calificable=True
            ).aggregate(average=Coalesce(Avg('opcion__valor'), 0))['average']

            meses.append(
                {
                    'inicio': inicio,
                    'fin': fin,
                    'consultas': atenciones,
                    'encuestada': encuestadas,
                    'contactabilidad': contactabilidad,
                    'satisfaccion': satisfaccion,
                }
            )

        context['meses'] = meses

        inicio_year = make_day_start(now.replace(month=1, day=1))
        final_year = make_end_day(now.replace(month=12, day=31))

        respuestas = Respuesta.objects.filter(
            created__range=(inicio_year, final_year)
        )

        context['respuestas'] = respuestas.extra(
            select={
                'month': connections[Respuesta.objects.db].ops.date_trunc_sql(
                    'month', 'created'
                )
            }
        ).values(
            'usuario__first_name',
            'usuario__last_name',
            'month',
        ).annotate(
            count=Count('id')
        ).order_by('month', '-count')

        return context


class EncuestaDetailView(LoginRequiredMixin, DetailView):
    """
    Shows the pending :class:`Consulta` to be polled
    """
    model = Encuesta
    context_object_name = 'encuesta'
    queryset = Encuesta.objects.prefetch_related('respuesta_set')

    def get_context_data(self, **kwargs):
        """
        Adds the :class:`Consulta`s that are not yet marked as polled and
        the :class:`Encuesta` that are still active.
        """
        context = super(EncuestaDetailView, self).get_context_data(**kwargs)

        context['consultas'] = self.object.consultas()
        context['encuestas'] = Encuesta.objects.filter(activa=True)

        return context


class EncuestaMixin(ContextMixin, View):
    """Permite obtener un :class:`Paciente` desde los argumentos en una url"""

    def dispatch(self, *args, **kwargs):
        self.encuesta = get_object_or_404(Encuesta, pk=kwargs['encuesta'])
        return super(EncuestaMixin, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(EncuestaMixin, self).get_context_data(**kwargs)

        context['encuesta'] = self.encuesta

        return context


class EncuestaFormMixin(EncuestaMixin, FormMixin):
    """Permite inicializar el paciente que se utilizará en un formulario"""

    def get_initial(self):
        initial = super(EncuestaFormMixin, self).get_initial()
        initial = initial.copy()
        initial['encuesta'] = self.encuesta
        return initial


class RespuestaCreateView(EncuestaFormMixin, ConsultaFormMixin,
                          LoginRequiredMixin, CreateView):
    model = Respuesta
    form_class = RespuestaForm

    def form_valid(self, form):
        self.object = form.save()
        self.object.persona = self.consulta.persona

        self.consulta.encuestada = True
        self.consulta.save()

        for pregunta in self.object.encuesta.pregunta_set.all():
            voto = Voto()
            voto.pregunta = pregunta
            voto.respuesta = self.object
            voto.save()

        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


class RespuestaDetailView(LoginRequiredMixin, DetailView):
    """
    Shows an interface that allows displaying all a :class:`Respuesta`
    information
    """
    model = Respuesta
    context_object_name = 'respuesta'
    queryset = Respuesta.objects.all().prefetch_related(
        'voto_set',
        'voto_set__opcion',
    )

    def get_context_data(self, **kwargs):
        context = super(RespuestaDetailView, self).get_context_data(**kwargs)

        formset = VotoFormSet(queryset=self.object.voto_set.all())
        for form in formset:
            form.fields[
                'opcion'].queryset = form.instance.pregunta.opcion_set.all()
            if not form.instance.pregunta.mostrar_sugerencia:
                form.fields['sugerencia'].widget = forms.HiddenInput()

        context['formset'] = formset
        context['helper'] = FormHelper()
        context['helper'].form_action = reverse('votos-guardar',
                                                args=[self.object.id])
        context['helper'].add_input(Submit('submit', _('Guardar')))

        context['queja'] = QuejaForm(initial={'respuesta': self.object})
        context['queja'].helper.form_id = 'queja'
        context['queja'].helper.form_action = reverse('queja-agregar',
                                                      args=[self.object.id])

        return context


def save_votes(request, respuesta):
    respuesta = get_object_or_404(Respuesta, pk=respuesta)
    if request.method == 'POST':
        formset = VotoFormSet(request.POST, respuesta.voto_set.all())
        if formset.is_valid():
            formset.save()
            respuesta.terminada = True
            respuesta.save()
        else:
            messages.info(request, _('La respuesta está incompleta'))
            return redirect(respuesta)
    else:
        messages.info(request, _('La respuesta está incompleta'))
        return redirect(respuesta)

    messages.info(request, _('Encuesta guardada!'))
    respuesta.consulta.encuestada = True
    respuesta.consulta.save()

    return redirect(respuesta.encuesta)


class RespuestaMixin(ContextMixin, View):
    """Permite obtener un :class:`Paciente` desde los argumentos en una url"""

    def dispatch(self, *args, **kwargs):
        self.respuesta = get_object_or_404(Respuesta, pk=kwargs['respuesta'])
        return super(RespuestaMixin, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(RespuestaMixin, self).get_context_data(**kwargs)

        context['respuesta'] = self.respuesta

        return context


class RespuestaFormMixin(RespuestaMixin, FormMixin):
    """Permite inicializar el paciente que se utilizará en un formulario"""

    def get_initial(self):
        initial = super(RespuestaFormMixin, self).get_initial()
        initial = initial.copy()
        initial['respuesta'] = self.respuesta
        return initial


class PreguntaMixin(ContextMixin, View):
    """Permite obtener un :class:`Paciente` desde los argumentos en una url"""

    def dispatch(self, *args, **kwargs):
        self.pregunta = get_object_or_404(Pregunta, pk=kwargs['pregunta'])
        return super(PreguntaMixin, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PreguntaMixin, self).get_context_data(**kwargs)

        context['pregunta'] = self.pregunta

        return context


class PreguntaFormMixin(PreguntaMixin, FormMixin):
    """Permite inicializar el paciente que se utilizará en un formulario"""

    def get_initial(self):
        initial = super(PreguntaFormMixin, self).get_initial()
        initial = initial.copy()
        initial['pregunta'] = self.pregunta
        return initial


class VotoUpdateView(LoginRequiredMixin, UpdateView):
    model = Voto
    form_class = VotoForm

    def get_form(self, form_class=None):
        form = super(VotoUpdateView, self).get_form(form_class)

        if self.object is not None:
            form.fields[
                'opcion'].queryset = self.object.pregunta.opcion_set.all()

        return form


class RespuestaRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self, **kwargs):
        encuesta = get_object_or_404(Encuesta, pk=kwargs['encuesta'])
        consulta = get_object_or_404(Consulta, pk=kwargs['consulta'])

        respuesta = Respuesta()
        respuesta.consulta = consulta
        respuesta.encuesta = encuesta
        respuesta.persona = consulta.persona
        respuesta.usuario = self.request.user
        consulta.encuestada = True
        consulta.save()
        respuesta.save()

        for pregunta in encuesta.pregunta_set.all():
            voto = Voto()
            voto.pregunta = pregunta
            voto.respuesta = respuesta
            voto.save()

        return respuesta.get_absolute_url()


class ConsultaEncuestadaRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self, **kwargs):
        encuesta = get_object_or_404(Encuesta, pk=kwargs['encuesta'])
        consulta = get_object_or_404(Consulta, pk=kwargs['consulta'])

        consulta.encuestada = True
        consulta.no_desea_encuesta = True
        consulta.save()

        return encuesta.get_absolute_url()


class ConsultaNoEncuestadaRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self, **kwargs):
        encuesta = get_object_or_404(Encuesta, pk=kwargs['encuesta'])
        consulta = get_object_or_404(Consulta, pk=kwargs['consulta'])

        consulta.encuestada = True
        consulta.save()

        return encuesta.get_absolute_url()


class QuejaCreateView(LoginRequiredMixin, CreateView, RespuestaFormMixin):
    """
    Enables the user to create :class:`Queja` instances
    """
    model = Queja
    form_class = QuejaForm

    def get_success_url(self):
        return self.object.respuesta.get_absolute_url()


class QuejaAseguradoraCreateView(LoginRequiredMixin, CreateView):
    """
    Allows the user to create :class:`Queja` associated to a
    :class:`Aseguradora`
    """
    model = Queja
    form_class = QuejaAseguradoraForm


class QuejaDetailView(LoginRequiredMixin, DetailView):
    model = Queja
    queryset = Queja.objects.prefetch_related(
        'solucion_set',
    )


class QuejaListView(LoginRequiredMixin, ListView):
    model = Queja
    queryset = Queja.objects.filter(resuelta=False).select_related(
        'respuesta',
        'respuesta__persona',
        'respuesta__consulta',
        'respuesta__consulta__poliza',
        'respuesta__consulta__contrato',
        'respuesta__consulta__persona',
        'respuesta__consulta__poliza__aseguradora',
        'respuesta__consulta__consultorio__usuario',
    ).prefetch_related(
        'solucion_set',
        'respuesta__consulta__persona__beneficiarios',
        'respuesta__consulta__persona__beneficiarios',
        'respuesta__consulta__persona__beneficiarios__contrato',
        'respuesta__consulta__persona__beneficiarios__contrato__persona',
        'respuesta__consulta__consultorio__secretaria',
        'respuesta__consulta__consultorio__usuario__profile',
        'respuesta__consulta__consultorio__usuario__profile__ciudad',
    ).exclude(
        solucion__aceptada=True
    )
    context_object_name = 'quejas'

    def get_context_data(self, **kwargs):
        """
        Adds rejection and aceptance forms to the template
        """
        context = super(QuejaListView, self).get_context_data(**kwargs)
        context['encuestas'] = Encuesta.objects.filter(activa=True)
        return context


class QuejaMixin(ContextMixin, View):
    def dispatch(self, *args, **kwargs):
        self.queja = get_object_or_404(Queja, pk=kwargs['queja'])
        return super(QuejaMixin, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(QuejaMixin, self).get_context_data(**kwargs)

        context['queja'] = self.queja

        return context


class QuejaFormMixin(QuejaMixin, FormMixin):
    """
    Permite inicializar el paciente que se utilizará en un formulario
    """

    def get_initial(self):
        initial = super(QuejaFormMixin, self).get_initial()
        initial = initial.copy()
        initial['queja'] = self.queja
        return initial


class SolucionCreateView(QuejaFormMixin, CurrentUserFormMixin, CreateView,
                         LoginRequiredMixin):
    model = Solucion
    form_class = SolucionForm


class SolucionListCreateView(SolucionCreateView):
    """
    Redirects users to :class:`Queja`'s list page
    """

    def get_success_url(self):
        """
        Returns the url of the :class:`Queja` list
        """
        return reverse('quejas')


class SolucionListView(LoginRequiredMixin, ListView):
    """
    Shows a :class:`Solucion` list that filters out all rejected and accepted.
    """
    model = Solucion
    queryset = Solucion.objects.select_related(
        'queja',
        'usuario',
        'queja__respuesta',
        'queja__departamento',
        'queja__respuesta__persona',
        'queja__respuesta__consulta',
        'queja__respuesta__consulta__poliza',
        'queja__respuesta__consulta__persona',
        'queja__respuesta__consulta__contrato',
        'queja__respuesta__consulta__contrato__master',
        'queja__respuesta__consulta__poliza__aseguradora',
        'queja__respuesta__consulta__consultorio__usuario',
    ).prefetch_related(
        'queja__solucion_set',
        'queja__respuesta__consulta__poliza__contratos',
        'queja__respuesta__consulta__persona__beneficiarios',
        'queja__respuesta__consulta__consultorio__secretaria',
        'queja__respuesta__consulta__consultorio__usuario__profile',
        'queja__respuesta__consulta__consultorio__usuario__profile__ciudad',
    ).filter(
        aceptada=False,
        rechazada=False,
    )

    def get_context_data(self, **kwargs):
        """
        Adds rejection and aceptance forms to the template
        """
        context = super(SolucionListView, self).get_context_data(**kwargs)
        context['form'] = SolucionAceptadaForm()
        rechazada_form = SolucionRechazadaForm()
        context['rechazada'] = rechazada_form
        rechazada_form.helper.form_tag = False
        rechazada_form.helper.label_class = ''
        rechazada_form.helper.field_class = ''
        rechazada_form.helper.form_class = ''

        context['encuestas'] = Encuesta.objects.filter(activa=True)
        return context


class SolucionUpdateView(LoginRequiredMixin, UpdateView):
    """
    Allows updating :class:`Solucion` from the UI
    """
    model = Solucion


class SolucionAceptarUpdateView(SolucionUpdateView):
    """
    Updates a :class:`Solucion` to be acepted.
    """
    form_class = SolucionAceptadaForm

    def get_success_url(self):
        """
        Returns the address of the :class:`Solucion` list.
        """
        return reverse('solucion-list')


class SolucionRechazarUpdateView(SolucionUpdateView):
    """
    Updates a class:`Solucion` to be rejected
    """
    form_class = SolucionRechazadaForm

    def get_success_url(self):
        """
        Returns the address of the :class:`Solucion` list.
        """
        return reverse('solucion-list')


class SolucionEmailPreView(LoginRequiredMixin, DetailView):
    """
    Previews the email before the user can send it.
    """
    model = Solucion
    template_name = 'bsc/solucion_email.html'
    queryset = Solucion.objects.select_related(
        'queja__respuesta__consulta',
        'queja__respuesta__consulta__persona',
        'queja__respuesta__consulta__poliza',
        'queja__respuesta__consulta__poliza__aseguradora',
        'queja__respuesta__consulta__contrato',
        'queja__respuesta__consulta__espera',
    ).prefetch_related(
        'queja__respuesta__consulta__ordenes_medicas',
    )

    def get_context_data(self, **kwargs):
        context = super(SolucionEmailPreView, self).get_context_data(**kwargs)
        context['preview'] = True
        context['persona'] = self.object.queja.respuesta.consulta.persona

        return context


class SolucionEmailView(LoginRequiredMixin, RedirectView):
    """
    Sends a notification email to the :class:`Persona` that made the complaint
    """
    permanent = False

    def get_redirect_url(self, **kwargs):
        solucion = get_object_or_404(Solucion, pk=kwargs['solucion'])

        if solucion.queja.respuesta.persona.email:
            message = EmailMessage(
                str('bsc/solucion_email.tpl'),
                {
                    'persona': solucion.queja.respuesta.persona,
                    'fecha': timezone.now().date(),
                },
                to=[solucion.queja.respuesta.consulta.persona.email,
                    'sac@epsmedical.com'],
                from_email=settings.EMAIL_HOST_USER
            )
            message.send()

        return reverse('solucion-list')


class SolucionAseguradoraEmailPreView(SolucionEmailPreView):
    """
    Shows a preview of the email that will be sent to
    """
    template_name = 'bsc/solucion_aseguradora_email.html'

    def get_context_data(self, **kwargs):
        context = super(SolucionAseguradoraEmailPreView, self).get_context_data(
            **kwargs)
        consulta = self.object.queja.respuesta.consulta
        context['consulta'] = consulta
        if consulta.poliza:
            context['aseguradora'] = consulta.poliza.aseguradora

        return context


class SolucionAseguradoraEmailView(LoginRequiredMixin, RedirectView):
    """
    Sends a notification email to the :class:`Persona` that made the complaint
    """
    permanent = False

    def get_redirect_url(self, **kwargs):
        solucion = get_object_or_404(Solucion, pk=kwargs['solucion'])

        consulta = solucion.queja.respuesta.consulta
        email = consulta.poliza.aseguradora.cardex.email

        if email:
            message = EmailMessage(
                str('bsc/solucion_aseguradora_email.tpl'),
                {
                    'consulta': consulta,
                    'aseguradora': consulta.poliza.aseguradora,
                    'fecha': timezone.now().date(),
                },
                to=[email, 'sac@epsmedical.com'],
                from_email=settings.EMAIL_HOST_USER
            )
            message.send()

        return reverse('solucion-list')


class ArchivoNotasCreateView(LoginRequiredMixin, CreateView):
    model = ArchivoNotas
    form_class = ArchivoNotasForm


class ArchivoNotasDetailView(LoginRequiredMixin, DetailView):
    model = ArchivoNotas
    context_object_name = 'archivonotas'


class ArchivoNotasProcesarView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self, **kwargs):
        archivonotas = get_object_or_404(ArchivoNotas, pk=kwargs['pk'])
        archivonotas.procesar()

        messages.info(self.request, _('¡Archivo Importado Exitosamente!'))
        return archivonotas.get_absolute_url()


class LoginPeriodoView(PeriodoView, LoginRequiredMixin):
    prefix = 'login'
    redirect_on_invalid = 'scorecard-index'
    model = Login
    template_name = 'bsc/login_list.html'

    def get_context_data(self, **kwargs):
        context = super(LoginPeriodoView, self).get_context_data(**kwargs)
        context['object_list'] = Login.objects.filter(
            created__range=(self.inicio, self.fin)
        ).order_by('user', 'created')

        return context


class RellamarCreateView(LoginRequiredMixin, EncuestaFormMixin,
                         ConsultaFormMixin, CreateView):
    """
    Creates a :class:`Rellamar` from the UI
    """
    model = Rellamar
    form_class = RellamarForm
