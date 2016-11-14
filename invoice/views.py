# -*- coding: utf-8 -*-
#
# Copyright (C) 2011-2015 Carlos Flores <cafg10@gmail.com>
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

import calendar
from collections import defaultdict, OrderedDict
from datetime import datetime, time, date, timedelta
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import permission_required, login_required
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.forms.models import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.generic import CreateView, UpdateView, TemplateView, \
    DetailView, ListView, RedirectView, DeleteView, View
from django.views.generic.base import ContextMixin
from django.views.generic.dates import MonthArchiveView
from django.views.generic.edit import FormMixin, FormView
from extra_views.dates import daterange

from clinique.models import Consulta
from contracts.models import Aseguradora, MasterContract
from contracts.views import AseguradoraMixin
from emergency.models import Emergencia
from hospinet.utils.date import make_end_day, make_day_start
from hospinet.utils.forms import NumeroForm
from imaging.models import Examen
from inventory.models import ItemTemplate, TipoVenta
from invoice.forms import ReciboForm, VentaForm, PeriodoForm, \
    AdmisionFacturarForm, CorteForm, ExamenFacturarForm, InventarioForm, \
    PagoForm, PersonaForm, TurnoCajaForm, CierreTurnoForm, \
    VentaPeriodoForm, PeriodoAreaForm, PagoStatusForm, TipoPagoPeriodoForm, \
    PeriodoCiudadForm, CuentaPorCobrarForm, PagoCuentaForm, CotizacionForm, \
    CotizadoForm, ComprobanteDeduccionForm, ConceptoDeduccionForm, \
    ReembolsoForm, ReciboTipoForm, NotaCreditoForm, TurnoCajaCierreForm
from invoice.models import Recibo, Venta, Pago, TurnoCaja, CierreTurno, \
    TipoPago, StatusPago, CuentaPorCobrar, Notification, Cotizacion, Cotizado, \
    ComprobanteDeduccion, ConceptoDeduccion, PagoCuenta, NotaCredito, \
    DetalleCredito
from persona.models import Persona
from persona.views import PersonaFormMixin
from spital.forms import DepositoForm
from spital.models import Admision, Deposito
from users.mixins import LoginRequiredMixin, CurrentUserFormMixin


class InvoicePermissionMixin(LoginRequiredMixin):
    @method_decorator(permission_required('invoice.cajero'))
    def dispatch(self, *args, **kwargs):
        return super(InvoicePermissionMixin, self).dispatch(*args, **kwargs)


def create_periodo_form(context, object_name, prefix, legend, action):
    context[object_name] = PeriodoForm(prefix=prefix)
    context[object_name].set_legend(legend)
    context[object_name].set_action(action)


class IndexView(InvoicePermissionMixin, TemplateView):
    """Muestra las opciones disponibles para la aplicación"""

    template_name = 'invoice/index.html'

    def get_context_data(self, **kwargs):
        """
        Agrega todos los formularios que permiten ver los diversos reportes
        relacionados con los :class:`Recibo`
        """

        context = super(IndexView, self).get_context_data(**kwargs)
        create_periodo_form(context, 'reciboperiodoform', 'recibo',
                            'Recibos de un Periodo', 'invoice-periodo')

        create_periodo_form(context, 'recibodetailform', 'recibodetail',
                            'Detalle de Recibos de un Periodo',
                            'invoice-periodo-detail')

        create_periodo_form(context, 'productoperiodoform', 'producto',
                            'Productos Facturados en un Periodo',
                            'invoice-periodo-producto')

        create_periodo_form(context, 'emerperiodoform', 'emergencia',
                            'Emergencias de un Periodo',
                            'invoice-periodo-emergencia')

        create_periodo_form(context, 'pagoform', 'pago',
                            'Pagos por Tipo y Periodo',
                            'invoice-periodo-pago')

        create_periodo_form(context, 'estadisticasform', 'estadisticas',
                            'Estadísticas por periodo',
                            'invoice-estadisticas-periodo')

        context['tipoform'] = PeriodoCiudadForm(prefix='tipo')
        context['tipoform'].set_action('invoice-tipo')
        context['tipoform'].helper.layout.legend = _(
            'Productos por Ciudad y Periodo')

        context['estadisticasciudadform'] = PeriodoCiudadForm(
            prefix='estadisticasciudad')
        context['estadisticasciudadform'].set_action(
            'invoice-estadisticas-ciudad-periodo')
        context['estadisticasciudadform'].helper.layout.legend = _(
            'Estadísticas por Ciudad y periodo')

        context['corteform'] = CorteForm(prefix='corte')
        context['corteform'].set_action('invoice-corte')

        context['tipopagoform'] = TipoPagoPeriodoForm(prefix='tipopago')
        context['tipopagoform'].set_action('periodo-tipopago')

        context['inventarioform'] = InventarioForm(prefix='inventario')
        context['inventarioform'].set_action('invoice-inventario')
        context['cotizaciones'] = Cotizacion.objects.filter(
            facturada=False
        ).select_related(
            'usuario', 'persona', 'usuario__profile', 'ciudad'
        ).all()

        context['examenes'] = Examen.objects.filter(
            facturado=False, pendiente=False
        ).order_by('-id')

        context['admisiones'] = Admision.objects.filter(facturada=False)
        context['emergencias'] = Emergencia.objects.filter(
            facturada=False
        ).order_by('id')
        context['consultas'] = Consulta.objects.filter(
            facturada=False,
            activa=False,
            tipo__facturable=True,
            consultorio__localidad__ciudad=self.request.user.profile.ciudad
        ).select_related('persona', 'consultorio__usuario', 'consultorio')

        context['turnos'] = TurnoCaja.objects.filter(
            usuario=self.request.user,
            finalizado=False
        ).all()

        if context['turnos'].count() != 0:
            context['turno'] = True

        context['status'] = StatusPago.objects.filter(reportable=True).all()

        context['pendientes'] = Recibo.objects.filter(
            cerrado=False
        ).select_related(
            'tipo_de_venta',
            'cliente',
            'ciudad',
            'cajero__profile__ciudad',
            'legal_data',
        ).prefetch_related(
            'ventas',
            'ventas__item',
            'pagos',
            'pagos__aseguradora',
            'pagos__tipo'
        ).all()

        context['ventaperiodoform'] = VentaPeriodoForm(prefix='venta')
        context['ventaperiodoform'].set_action('periodo-venta')

        context['ventaareaperiodoform'] = PeriodoAreaForm(prefix='venta-area')
        context['ventaareaperiodoform'].set_action('periodo-venta-area')

        context['ciudadform'] = PeriodoCiudadForm(prefix='ciudad-periodo')
        context['ciudadform'].set_action('periodo-ciudad')

        context['turnoform'] = PeriodoCiudadForm(prefix='turno-periodo')
        context['turnoform'].set_action('turno-periodo')
        context['turnoform'].helper.layout.legend = _('Resumen de Turnos')

        context['numero_form'] = NumeroForm()
        context['numero_form'].set_legend(_('Buscar Recibo por Número'))
        context['numero_form'].helper.form_method = 'get'
        context['numero_form'].set_action('invoice-numero')

        return context


class EstadisticasView(LoginRequiredMixin, TemplateView):
    """Makes the calculations about the income generated by the invoicing
    results"""
    template_name = 'invoice/estadisticas.html'

    def get_context_data(self, **kwargs):
        context = super(EstadisticasView, self).get_context_data(**kwargs)
        recibos = Recibo.objects.all()

        now = timezone.now()
        context['pagos'] = OrderedDict()
        context['months'] = []
        context['recibos'] = []
        context['tipos'] = {}
        context['meses'] = OrderedDict()

        fin = make_end_day(now.replace(month=12, day=31))
        inicio = make_day_start(now.replace(month=1, day=1))

        for tipo in TipoPago.objects.all():
            context['pagos'][tipo] = OrderedDict()

            pagado = tipo.pagos.filter(
                recibo__created__range=(inicio, fin)
            ).aggregate(total=Sum('monto'))['total']
            if pagado is None:
                pagado = Decimal()

            context['tipos'][tipo] = pagado

        for n in range(1, 13):
            inicio = make_day_start(now.replace(month=n, day=1))
            fin = make_end_day(
                now.replace(month=n, day=calendar.monthrange(now.year, n)[1])
            )

            total = recibos.filter(
                created__range=(inicio, fin)
            ).aggregate(total=Coalesce(Sum('valor'), Decimal()))['total']

            context['meses'][inicio] = []
            context['recibos'].append(total)

            for tipo in TipoPago.objects.all():
                pagado = tipo.pagos.filter(
                    recibo__created__range=(inicio, fin)
                ).aggregate(total=Coalesce(Sum('monto'), Decimal()))['total']
                context['meses'][inicio].append((tipo, pagado))

            for tipo in context['pagos']:
                pagado = tipo.pagos.filter(
                    recibo__created__range=(inicio, fin)
                ).aggregate(total=Coalesce(Sum('monto'), Decimal()))['total']
                context['pagos'][tipo][inicio] = pagado
            context['months'].append(inicio)

        return context


class EstadisticasPeriodoView(LoginRequiredMixin, TemplateView):
    """Obtiene los :class:`Recibo` de un periodo determinado en base
    a un formulario que las clases derivadas deben proporcionar como
    self.form"""
    template_name = 'invoice/estadisticas_periodo.html'

    def dispatch(self, request, *args, **kwargs):
        """Efectua la consulta de los :class:`Recibo` de acuerdo a los
        datos ingresados en el formulario"""

        self.form = PeriodoForm(request.GET, prefix='estadisticas')

        if self.form.is_valid():
            self.inicio = self.form.cleaned_data['inicio']
            self.fin = self.form.cleaned_data['fin']

        return super(EstadisticasPeriodoView, self).dispatch(request, *args,
                                                             **kwargs)

    def get_context_data(self, **kwargs):
        context = super(EstadisticasPeriodoView, self).get_context_data(
            **kwargs)

        context['pagos'] = []

        total = Recibo.objects.annotate(sold=Coalesce(
            Sum('ventas__total'), Decimal())
        ).filter(
            created__range=(self.inicio, self.fin)
        ).aggregate(total=Coalesce(Sum('sold'), Decimal()))['total']

        ventas = Venta.objects.filter(
            recibo__created__range=(self.inicio, self.fin))
        context['ventas'] = ventas.values('item__descripcion').annotate(
            monto=Coalesce(Sum('monto'), Decimal()),
            cantidad=Coalesce(Sum('cantidad'), Decimal())
        ).order_by('-monto')[:20]

        context['recibos'] = total

        for tipo in TipoPago.objects.all():
            pagado = tipo.pagos.filter(
                recibo__created__range=(self.inicio, self.fin)
            ).aggregate(total=Coalesce(Sum('monto'), Decimal()))['total']
            context['pagos'].append((tipo, pagado))

        context['inicio'] = self.inicio
        context['fin'] = self.fin
        return context


class EstadisticasPeriodoCiudadView(LoginRequiredMixin, TemplateView):
    """Obtiene los :class:`Recibo` de un periodo determinado en base
    a un formulario que las clases derivadas deben proporcionar como
    self.form"""
    template_name = 'invoice/estadisticas_ciudad_periodo.html'

    def dispatch(self, request, *args, **kwargs):
        """Efectua la consulta de los :class:`Recibo` de acuerdo a los
        datos ingresados en el formulario"""

        self.form = PeriodoCiudadForm(request.GET, prefix='estadisticasciudad')

        if self.form.is_valid():
            self.inicio = self.form.cleaned_data['inicio']
            self.fin = self.form.cleaned_data['fin']
            self.ciudad = self.form.cleaned_data['ciudad']

        return super(EstadisticasPeriodoCiudadView, self).dispatch(request,
                                                                   *args,
                                                                   **kwargs)

    def get_context_data(self, **kwargs):
        context = super(EstadisticasPeriodoCiudadView, self).get_context_data(
            **kwargs)

        context['pagos'] = []

        total = Recibo.objects.annotate(sold=Coalesce(
            Sum('ventas__total'), Decimal())
        ).filter(
            created__range=(self.inicio, self.fin), ciudad=self.ciudad
        ).aggregate(total=Coalesce(Sum('sold'), Decimal()))['total']

        ventas = Venta.objects.filter(
            recibo__created__range=(self.inicio, self.fin),
            recibo__ciudad=self.ciudad
        )
        context['ventas'] = ventas.values('item__descripcion').annotate(
            monto=Coalesce(Sum('monto'), Decimal()),
            cantidad=Coalesce(Sum('cantidad'), Decimal())
        ).order_by('-monto')[:500]

        context['recibos'] = total

        for tipo in TipoPago.objects.all():
            pagado = tipo.pagos.filter(
                recibo__created__range=(self.inicio, self.fin),
                recibo__ciudad=self.ciudad
            ).aggregate(total=Coalesce(Sum('monto'), Decimal()))['total']
            context['pagos'].append((tipo, pagado))

        context['inicio'] = self.inicio
        context['fin'] = self.fin
        return context


class ReciboPersonaCreateView(LoginRequiredMixin, CreateView, PersonaFormMixin):
    """Permite crear un :class:`Recibo` utilizando una :class:`Persona`
    existente en la aplicación
    """

    model = Recibo
    form_class = ReciboForm
    template_name = 'invoice/recibo_persona_create.html'

    def get_initial(self):
        """Agrega el :class:`User` actual a los campos del formulario
        """

        initial = super(ReciboPersonaCreateView, self).get_initial()
        initial = initial.copy()
        initial['cliente'] = self.persona
        initial['cajero'] = self.request.user.id
        return initial


class ReciboCreateView(LoginRequiredMixin, CreateView):
    """Permite crear un :class:`Recibo` al mismo tiempo que se crea una
    :class:`Persona`, utiliza un formulario simplificado que requiere
    unicamente indicar el nombre y apellidos del cliente, que aún así son
    opcionales.
    """
    model = Recibo

    def dispatch(self, request, *args, **kwargs):

        self.persona = Persona()
        self.ReciboFormset = inlineformset_factory(Persona, Recibo,
                                                   form=ReciboForm,
                                                   fk_name='cliente', extra=1)
        return super(ReciboCreateView, self).dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):

        self.persona_form = PersonaForm(instance=self.persona, prefix='persona')
        self.persona_form.helper.form_tag = False
        formset = self.ReciboFormset(
            instance=self.persona,
            prefix='recibo',
            initial=[{'cajero': self.request.user}]
        )
        return formset

    def get_context_data(self, **kwargs):

        context = super(ReciboCreateView, self).get_context_data(**kwargs)
        context['persona_form'] = self.persona_form
        return context

    def post(self, request, *args, **kwargs):
        self.form = PersonaForm(request.POST, request.FILES,
                                instance=self.persona,
                                prefix='persona')
        self.formset = self.ReciboFormset(request.POST, request.FILES,
                                          instance=self.persona,
                                          prefix='recibo')

        if self.form.is_valid() and self.formset.is_valid():
            self.form.save()
            instances = self.formset.save()
            for instance in instances:
                self.recibo = instance
                self.recibo.cajero = self.request.user
                self.recibo.ciudad = self.recibo.cajero.profile.ciudad
                self.recibo.save()

            return self.form_valid(self.formset)
        else:
            return self.form_invalid(self.formset)

    def get_success_url(self):

        return self.recibo.get_absolute_url()


class ReciboTipoFormUpdateView(LoginRequiredMixin, UpdateView):
    """
    Allows changing the :class:`TipoVenta` of a :class:`Recibo`
    """
    model = Recibo
    form_class = ReciboTipoForm
    template_name = 'invoice/recibo_cambio_form.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)

        self.object.save()

        [v.save() for v in self.object.ventas.all()]

        return HttpResponseRedirect(self.object.get_absolute_url())


class ReciboDetailView(LoginRequiredMixin, DetailView):
    """Muestra los detalles del :class:`Recibo` para agregar :class:`Producto`s
    ir a la vista de impresión y realizar otras tareas relacionadas con
    facturación
    """

    model = Recibo
    object_context_name = 'recibo'
    template_name = 'invoice/recibo_detail.html'

    def get_context_data(self, **kwargs):
        """Agrega el formulario de :class:`Venta` para agregar
        :class:`Producto`s"""

        context = super(ReciboDetailView, self).get_context_data(**kwargs)
        context['form'] = VentaForm(initial={'recibo': self.object})
        context['form'].helper.form_action = reverse('venta-add',
                                                     args=[self.object.id])

        context['pago_form'] = PagoForm(initial={'recibo': self.object.id})
        context['pago_form'].helper.form_action = reverse('pago-add',
                                                          args=[self.object.id])

        context['reembolso_form'] = ReembolsoForm(
            initial={'recibo': self.object.id}
        )
        context['reembolso_form'].helper.form_action = reverse('reembolso-add')

        return context


class ReciboNumeroListView(LoginRequiredMixin, ListView):
    """
    Shows :class:`Recibo` whose correlativo matches the number from a
    :class:`NumeroForm`
    """
    context_object_name = 'recibos'

    def get_queryset(self):
        form = NumeroForm(self.request.GET)

        if form.is_valid():
            return Recibo.objects.filter(
                correlativo=form.cleaned_data['numero']
            )

        return Recibo.objects.select_related(
            'tipo_de_venta',
            'cliente',
            'ciudad',
            'cajero__profile__ciudad',
        ).prefetch_related(
            'ventas',
            'ventas__item',
            'pagos',
            'pagos__aseguradora',
            'pagos__tipo'
        ).all()


class ReciboPrintView(LoginRequiredMixin, DetailView):
    """
    Displays the UI to print a :class:`Recibo`
    """
    model = Recibo
    object_context_name = 'recibo'
    template_name = 'invoice/recibo_print.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        if not self.object.cerrado:
            messages.info(self.request, _('El recibo aún no ha sido cerrado'))
            return redirect(self.object.get_absolute_url())

        return super(ReciboPrintView, self).get(request, *args, **kwargs)


class ReciboAnularView(LoginRequiredMixin, RedirectView):
    """Marca un :class:`Recibo` como anulado para que la facturación del mismo
    no se vea reflejado en los cortes de caja"""

    permanent = False

    def get_redirect_url(self, **kwargs):
        recibo = get_object_or_404(Recibo, pk=kwargs['pk'])
        recibo.anular()
        messages.info(
            self.request,
            _('¡El recibo ha sido marcado como anulado!')
        )
        return recibo.get_absolute_url()


class ReciboCerrarView(LoginRequiredMixin, RedirectView):
    """Marca un :class:`Recibo` como anulado para que la facturación del mismo
    no se vea reflejado en los cortes de caja"""

    permanent = False

    def get_redirect_url(self, **kwargs):
        recibo = get_object_or_404(Recibo, pk=kwargs['pk'])
        recibo.cerrar()

        if not recibo.cerrado:
            messages.info(self.request,
                          _('¡El recibo no se puede cerrar, revise los pagos'))
        else:
            messages.info(self.request, _('¡El recibo ha sido cerrado!'))
        return recibo.get_absolute_url()


class ReciboPeriodoView(LoginRequiredMixin, FormMixin, TemplateView):
    """Obtiene los :class:`Recibo` de un periodo determinado en base
    a un formulario que las clases derivadas deben proporcionar como
    self.form
    """
    form_class = PeriodoForm
    prefix = 'recibo'

    def dispatch(self, request, *args, **kwargs):
        """Efectua la consulta de los :class:`Recibo` de acuerdo a los
        datos ingresados en el formulario"""

        self.form = self.get_form_class()(request.GET, prefix=self.prefix)

        if self.form.is_valid():
            self.inicio = self.form.cleaned_data['inicio']
            self.fin = self.form.cleaned_data['fin']
            self.recibos = Recibo.objects.filter(
                created__gte=self.inicio,
                created__lte=self.fin,
            )
        else:
            messages.info(
                self.request,
                _('Los Datos Ingresados en el formulario no son validos')
            )
            return HttpResponseRedirect(reverse('invoice-index'))

        return super(ReciboPeriodoView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Agrega el formulario de :class:`Recibo`"""

        context = super(ReciboPeriodoView, self).get_context_data(**kwargs)

        context['recibos'] = self.recibos
        context['inicio'] = self.inicio
        context['fin'] = self.fin
        context['total'] = Venta.objects.filter(
            recibo__in=self.recibos,
            recibo__nulo=False
        ).aggregate(total=Coalesce(Sum('total'), Decimal()))['total']

        return context


class ReciboMonthArchiveView(LoginRequiredMixin, MonthArchiveView):
    """
    Shows the :class:`Recibo` created during a month
    """
    queryset = Recibo.objects.select_related(
        'cajero',
        'ciudad',
        'cliente',
        'legal_data',
        'tipo_de_venta',
        'cajero__profile__ciudad',
    ).prefetch_related(
        'ventas',
        'ventas__item',
    ).annotate(
        total_ventas=Coalesce(Sum('ventas__total'), Decimal())
    )
    date_field = 'created'
    allow_future = True


class ReciboExamenCreateView(LoginRequiredMixin, CreateView):
    """Permite crear un :class:`Recibo` utilizando una :class:`Persona`
    existente en la aplicación"""

    model = Recibo
    form_class = ReciboForm
    template_name = 'invoice/recibo_persona_create.html'

    def get_form_kwargs(self):
        """Registra el :class:`User` que esta creando el :class:`Recibo`"""

        kwargs = super(ReciboExamenCreateView, self).get_form_kwargs()
        kwargs.update({'initial': {'cajero': self.request.user.id,
                                   'cliente': self.examen.persona.id,
                                   'remite': self.examen.remitio}})
        return kwargs

    def dispatch(self, *args, **kwargs):
        """Obtiene el :class:`Recibo` que se entrego como argumento en la
        url"""

        self.examen = get_object_or_404(Examen, pk=kwargs['examen'])
        return super(ReciboExamenCreateView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ReciboExamenCreateView, self).get_context_data(**kwargs)
        context['persona'] = self.examen.persona
        return context

    def form_valid(self, form):
        self.object = form.save()

        venta = Venta()
        venta.item = self.examen.tipo_de_examen.item
        venta.recibo = self.object
        venta.cantidad = 1
        venta.precio = venta.item.precio_de_venta
        venta.impuesto = venta.item.impuestos

        venta.save()
        self.object.ventas.add(venta)
        self.examen.facturado = True
        self.examen.save()

        self.object.save()

        return HttpResponseRedirect(self.object.get_absolute_url())


class ReciboMixin(ContextMixin, View):
    """
    Adds a :class:`Recibo` to all child views
    """

    def dispatch(self, *args, **kwargs):
        self.recibo = get_object_or_404(Recibo, pk=kwargs['recibo'])
        return super(ReciboMixin, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ReciboMixin, self).get_context_data(**kwargs)
        context['recibo'] = self.recibo
        return context


class ReciboFormMixin(ReciboMixin, FormMixin):
    """Especifica una interfaz común para la creación de Entidades que requieran
    un :class:`Recibo` como parte de los campos requeridos por su formulario"""

    def get_initial(self):
        initial = super(ReciboFormMixin, self).get_initial()
        initial = initial.copy()
        initial['recibo'] = self.recibo.id
        return initial


class VentaCreateView(LoginRequiredMixin, ReciboFormMixin, CreateView):
    """Permite agregar :class:`Venta`s a un :class:`Recibo`"""

    model = Venta
    form_class = VentaForm


class VentaListView(LoginRequiredMixin, ListView):
    context_object_name = 'ventas'

    def dispatch(self, request, *args, **kwargs):
        self.form = VentaPeriodoForm(request.GET, prefix='venta')
        if self.form.is_valid():
            self.inicio = self.form.cleaned_data['inicio']
            self.fin = datetime.combine(self.form.cleaned_data['fin'], time.max)
            self.item = self.form.cleaned_data['item']

        return super(VentaListView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Venta.objects.filter(
            recibo__created__gte=self.inicio,
            recibo__created__lte=self.fin,
            recibo__nulo=False,
            item=self.item,
        ).select_related(
            'recibo',
            'recibo__legal_data',
            'recibo__cajero',
        )

    def get_context_data(self, **kwargs):
        context = super(VentaListView, self).get_context_data(**kwargs)
        context['item'] = self.item
        context['inicio'] = self.inicio
        context['fin'] = self.fin
        total = self.get_queryset().aggregate(total=Sum('total'))['total']
        if total is None:
            total = Decimal()
        context['total'] = total
        return context


class VentaDeleteView(LoginRequiredMixin, DeleteView):
    """Permite eliminar una :class:`Venta` que sea incorrecta en el
    :class:`Recibo`"""
    model = Venta

    def get_object(self, queryset=None):
        obj = super(VentaDeleteView, self).get_object(queryset)
        self.recibo = obj.recibo
        return obj

    def get_success_url(self):
        return self.recibo.get_absolute_url()


class PagoCreateView(LoginRequiredMixin, ReciboFormMixin, CreateView):
    """Permite agregar una forma de :class:`Pago` a un :class:`Recibo`

    En caso que la :class:`Persona` tenga un :class:`Contrato` vigente, el
    :class:`Pago` puede agregarse con uno de los :class:`TipoPago` que solo
    son permitidos a los asegurados.
    """
    model = Pago
    form_class = PagoForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        persona = self.object.recibo.cliente

        if self.object.tipo.solo_asegurados and persona.contratos.filter(
                vencimiento__lte=timezone.now()
        ).count() <= 0:

            messages.info(
                self.request,
                _('No se puede agregar un este tipo de pago sin contrato!')
            )
            if self.request.META['HTTP_REFERER']:
                return HttpResponseRedirect(
                    self.request.META['HTTP_REFERER'])
            else:
                return HttpResponseRedirect(reverse('invoice-index'))

        self.object.save()

        if self.object.tipo.reembolso:
            notification = Notification()
            notification.recibo = self.object.recibo
            notification.save()
            return HttpResponseRedirect(notification.get_absolute_url())

        return HttpResponseRedirect(self.get_success_url())


class PagoUpdateView(LoginRequiredMixin, UpdateView):
    """
    Allows updating a :class:`Pago`
    """
    model = Pago
    form_class = PagoStatusForm

    def get_success_url(self):
        return reverse('invoice-pago-status-index')


class PagoDeleteView(LoginRequiredMixin, DeleteView):
    """
    Deletes a :class:`Pago` instance
    """
    model = Pago

    def get_object(self, queryset=None):
        obj = super(PagoDeleteView, self).get_object(queryset)
        self.recibo = obj.recibo
        return obj

    def get_success_url(self):
        return self.recibo.get_absolute_url()


class PagoMonthArchiveView(LoginRequiredMixin, MonthArchiveView):
    """
    Shows the :class:`Pago` corresponding to a certain month
    """
    queryset = Pago.objects.select_related(
        'recibo',
        'recibo__cliente',
        'recibo__ciudad',
        'aseguradora',
    )
    date_field = 'created'
    allow_future = True


class PagoListView(LoginRequiredMixin, ListView):
    """
    Shows a list of :class:`Pago`
    """
    model = Pago
    context_object_name = 'pagos'
    paginate_by = '100'

    def get_queryset(self):
        return Pago.objects.prefetch_related(
            'recibo__cliente__contratos',
        ).select_related(
            'recibo',
            'recibo__ciudad',
            'recibo__cliente',
            'recibo__cajero__profile__ciudad',
        )

    def get_context_data(self, **kwargs):
        context = super(PagoListView, self).get_context_data(**kwargs)

        context['aseguradoras'] = self.get_queryset().values(
            'aseguradora__nombre'
        ).annotate(
            total=Coalesce(Sum('monto'), Decimal())
        ).order_by()

        context['total'] = self.get_queryset().aggregate(
            total=Coalesce(Sum('monto'), Decimal())
        )['total']

        return context


class PagoPendienteListView(PagoListView):
    """
    Shows all :class:`Pago` that have not been completed
    """

    def get_queryset(self):
        return super(PagoPendienteListView, self).get_queryset().filter(
            completado=False,
            tipo__reembolso=True,
            status__reportable=True,
        )


class PagoAseguradoraLisView(PagoListView, AseguradoraMixin):
    """
    Shows a list of :class:`Pago` that are related to a :class:`Aseguradora`
    """

    def get_queryset(self):
        return super(PagoAseguradoraLisView, self).get_queryset().filter(
            aseguradora=self.aseguradora
        )


class PagoPeriodoView(LoginRequiredMixin, TemplateView):
    """Obtiene los :class:`Recibo` de un periodo determinado en base
    a un formulario que las clases derivadas deben proporcionar como
    self.form"""
    template_name = 'invoice/pago_periodo.html'

    def dispatch(self, request, *args, **kwargs):
        """Efectua la consulta de los :class:`Recibo` de acuerdo a los
        datos ingresados en el formulario"""

        self.form = PeriodoForm(request.GET, prefix='pago')

        if self.form.is_valid():
            self.inicio = self.form.cleaned_data['inicio']
            self.fin = self.form.cleaned_data['fin']

        return super(PagoPeriodoView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PagoPeriodoView, self).get_context_data(**kwargs)
        pagos = Pago.objects.filter(
            recibo__created__range=(self.inicio, self.fin))
        context['group'] = pagos.values('tipo__nombre').annotate(
            monto=Coalesce(Sum('monto'), Decimal())
        ).order_by()
        context['pagos'] = pagos
        context['total'] = pagos.aggregate(
            total=Coalesce(Sum('monto'), Decimal())
        )

        context['inicio'] = self.inicio
        context['fin'] = self.fin
        return context


class ReporteReciboView(ReciboPeriodoView):
    """Muestra los ingresos captados mediante :class:`Recibo`s que se captaron
    durante el periodo especificado"""

    template_name = 'invoice/recibo_list.html'


class ReporteReciboDetailView(ReciboPeriodoView):
    """Muestra los ingresos captados mediante :class:`Recibo`s que se captaron
    durante el periodo especificado"""

    template_name = 'invoice/recibo_detail_list.html'
    prefix = 'recibodetail'


class ReporteTipoView(ReciboPeriodoView):
    """Muestra los ingresos captados mediante :class:`Recibo`s que se captaron
    durante el periodo especificado
    """

    template_name = 'invoice/tipo_list.html'
    prefix = 'tipo'

    def dispatch(self, request, *args, **kwargs):
        self.form = PeriodoCiudadForm(request.GET, prefix='tipo')
        if self.form.is_valid():
            self.inicio = self.form.cleaned_data['inicio']
            self.fin = self.form.cleaned_data['fin']
            self.ciudad = self.form.cleaned_data['ciudad']

        return super(ReporteTipoView, self).dispatch(request, *args,
                                                     **kwargs)

    def get_queryset(self):
        return Recibo.objects.filter(
            created__range=(self.inicio, self.fin),
            nulo=False,
            ciudad=self.ciudad
        )

    def get_context_data(self, **kwargs):

        """Agrega el formulario de :class:`Recibo`"""

        context = super(ReporteTipoView, self).get_context_data(**kwargs)

        context['cantidad'] = 0
        context['total'] = Decimal()
        categorias = defaultdict(lambda: defaultdict(Decimal))
        self.recibos = self.get_queryset()
        for recibo in self.recibos:

            for venta in recibo.ventas.all():
                monto = venta.total
                categoria = venta.item.item_type.first()

                categorias[categoria]['monto'] += monto
                categorias[categoria]['cantidad'] += 1

                context['cantidad'] += 1
                context['total'] += monto

        context['recibos'] = self.recibos
        context['categorias'] = categorias.items()
        context['inicio'] = self.inicio
        context['fin'] = self.fin
        return context


class ReporteProductoView(ReciboPeriodoView):
    """Muestra los ingresos captados mediante :class:`Recibo`s, distribuyendo
    los mismos de acuerdo al :class:`Producto` que se facturó, tomando en
    cuenta el periodo especificado"""

    template_name = 'invoice/producto_list.html'
    prefix = 'producto'

    def get_context_data(self, **kwargs):
        """Agrega el formulario de :class:`Recibo`"""

        context = super(ReporteProductoView, self).get_context_data(**kwargs)

        context['cantidad'] = 0
        context['total'] = Decimal()
        productos = defaultdict(lambda: defaultdict(Decimal))

        ventas = Venta.objects.filter(
            recibo__created__range=(self.inicio, self.fin))

        context['recibos'] = self.recibos
        context['productos'] = ventas.values('item__descripcion').annotate(
            monto=Sum('monto'), count=Sum('cantidad')
        ).order_by('-monto')

        context['impuesto'] = Venta.objects.filter(
            recibo__created__range=(self.inicio, self.fin)
        ).aggregate(tax=Sum('tax'))['tax']

        context['total'] = Venta.objects.filter(
            recibo__created__range=(self.inicio, self.fin)
        ).aggregate(total=Sum('total'))['total']

        context['inicio'] = self.inicio
        context['fin'] = self.fin
        return context


class EmergenciaPeriodoView(LoginRequiredMixin, TemplateView):
    """Muestra las opciones disponibles para la aplicación"""

    template_name = 'invoice/emergencia_list.html'

    def dispatch(self, request, *args, **kwargs):

        """Filtra las :class:`Emergencia` de acuerdo a los datos ingresados en
        el formulario"""

        self.form = PeriodoForm(request.GET, prefix='emergencia')
        if self.form.is_valid():

            self.inicio = self.form.cleaned_data['inicio']
            self.fin = datetime.combine(self.form.cleaned_data['fin'], time.max)
            self.emergencias = Emergencia.objects.filter(
                created__gte=self.inicio,
                created__lte=self.fin
            )

        else:

            return redirect('invoice-index')

        return super(EmergenciaPeriodoView, self).dispatch(request, *args,
                                                           **kwargs)

    def get_context_data(self, **kwargs):

        """Permite utilizar las :class:`Emergencia`s en la vista"""

        context = super(EmergenciaPeriodoView, self).get_context_data(**kwargs)
        context['emergencias'] = self.emergencias
        context['inicio'] = self.inicio
        context['fin'] = self.fin
        return context


class EmergenciaDiaView(LoginRequiredMixin, ListView):
    """Muestra los materiales y medicamentos de las :class:`Emergencia`s que
    han sido atendidas durante el día"""

    context_object_name = 'emergencias'
    template_name = 'invoice/emergency.html'
    paginate_by = 10

    def get_queryset(self):
        return Emergencia.objects.filter(facturada=False)


class ExamenView(LoginRequiredMixin, ListView):
    """Muestra los materiales y medicamentos de las :class:`Emergencia`s que
    han sido atendidas durante el día"""

    context_object_name = 'examenes'
    template_name = 'invoice/examen_list.html'
    paginate_by = 10

    def get_queryset(self):
        return Examen.objects.filter(facturado=False)


@login_required
def crear_ventas(items, recibo, examen=False, tecnico=False):
    """Permite convertir un :class:`dict` de :class:`ItemTemplate` y sus
    cantidades en una las :class:`Venta`s de un :class:`Recibo`

    Toma en consideración las indicaciones acerca de los cobros de comisiones
    indicados por los examenes"""

    for item in items:
        if item is None:
            continue
        venta = Venta()
        venta.item = item
        venta.recibo = recibo
        venta.cantidad = items[item]
        venta.precio = item.precio_de_venta
        venta.impuesto = item.impuestos

        venta.save()
        recibo.ventas.add(venta)


@login_required
def crear_ventas_consulta(items, precios, recibo):
    """Permite convertir un :class:`dict` de :class:`ItemTemplate` y sus
    cantidades en una las :class:`Venta`s de un :class:`Recibo`

    Toma en consideración las indicaciones acerca de los cobros de comisiones
    indicados por los examenes"""

    for item in items:
        venta = Venta()
        venta.item = item
        venta.recibo = recibo
        venta.cantidad = items[item]
        venta.precio = precios[item]
        venta.impuesto = item.impuestos

        venta.save()
        recibo.ventas.add(venta)


class EmergenciaFacturarView(LoginRequiredMixin, RedirectView):
    """
    Creates a :class:`Recibo` object from a :class:`Emergencia` instance
    """
    permanent = False

    def get_redirect_url(self, **kwargs):
        emergencia = get_object_or_404(Emergencia, pk=kwargs['pk'])

        items = emergencia.facturar()

        recibo = Recibo()
        recibo.cajero = self.request.user
        recibo.cliente = emergencia.persona

        recibo.tipo_de_venta = TipoVenta.objects.filter(
            predeterminada=True
        ).first()

        recibo.save()

        crear_ventas(items, recibo)

        emergencia.facturada = True
        emergencia.save()

        return recibo.get_absolute_url()

    @method_decorator(permission_required('invoice.cajero'))
    def dispatch(self, *args, **kwargs):
        return super(EmergenciaFacturarView, self).dispatch(*args, **kwargs)


class ConsultaFacturarView(LoginRequiredMixin, RedirectView):
    """
    Creates a :class:`Recibo` object from a :class:`Consulta` instance
    """
    permanent = False

    def get_redirect_url(self, **kwargs):

        messages.info(
            self.request,
            _('No puede facturar sin tener ciudad en su perfil!')
        )
        if self.request.user.profile.ciudad is None:
            messages.info(
                self.request,
                _('No puede facturar sin tener ciudad en su perfil!')
            )
            if self.request.META['HTTP_REFERER']:
                return self.request.META['HTTP_REFERER']
            else:
                return reverse('invoice-index')

        consulta = get_object_or_404(Consulta, pk=kwargs['pk'])

        items, precios = consulta.facturar()

        recibo = Recibo()
        recibo.cajero = self.request.user
        recibo.cliente = consulta.persona

        recibo.tipo_de_venta = TipoVenta.objects.filter(
            predeterminada=True
        ).first()

        recibo.save()

        crear_ventas_consulta(items, precios, recibo)

        consulta.facturada = True
        consulta.activa = False
        consulta.save()
        messages.info(
            self.request,
            _('¡La consulta se marcó como facturada!')
        )
        return recibo.get_absolute_url()

    @method_decorator(permission_required('invoice.cajero'))
    def dispatch(self, *args, **kwargs):
        return super(ConsultaFacturarView, self).dispatch(*args, **kwargs)


class AdmisionFacturarView(LoginRequiredMixin, UpdateView):
    """Permite crear de manera automática un :class:`Recibo` con todas sus
    :class:`Ventas` a partir de una :class:`Admision` que aun no se haya marcado
    como facturada"""

    model = Admision
    context_object_name = 'admision'
    form_class = AdmisionFacturarForm
    template_name = 'invoice/admision_form.html'

    @method_decorator(permission_required('invoice.cajero'))
    def dispatch(self, *args, **kwargs):
        return super(AdmisionFacturarView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):

        if self.request.user.profile.ciudad is None:
            messages.info(
                self.request,
                _('No puede facturar sin tener ciudad en su perfil!')
            )
            if self.request.META['HTTP_REFERER']:
                return HttpResponseRedirect(self.request.META['HTTP_REFERER'])
            else:
                return HttpResponseRedirect(reverse('invoice-index'))

        self.object = form.save(commit=False)

        items = self.object.facturar()

        recibo = Recibo()
        recibo.cajero = self.request.user
        recibo.cliente = self.object.paciente
        recibo.tipo_de_venta = self.object.tipo_de_venta

        recibo.save()

        crear_ventas(items, recibo)

        for honorario in self.object.honorarios.all():
            venta = Venta()
            venta.item = honorario.item
            venta.recibo = recibo
            venta.cantidad = 1
            venta.precio = honorario.monto
            venta.impuesto = honorario.item.impuestos
            venta.descontable = False

            venta.save()
            recibo.ventas.add(venta)

        self.object.ultimo_cobro = timezone.now()
        self.object.save()

        return HttpResponseRedirect(recibo.get_absolute_url())


class AseguradoraContractsFacturarView(LoginRequiredMixin, RedirectView):
    """
    Creates a :class:`Recibo` from the :class:`MasterContract`s that are
    associated to a single :class:`Aseguradora` instance
    """
    permanent = False

    def get_redirect_url(self, **kwargs):

        if self.request.user.profile.ciudad is None:
            messages.info(
                self.request,
                _('No puede facturar sin tener ciudad en su perfil!')
            )
            if self.request.META['HTTP_REFERER']:
                return self.request.META['HTTP_REFERER']
            else:
                return reverse('invoice-index')

        aseguradora = get_object_or_404(Aseguradora, pk=kwargs['pk'])

        if not aseguradora.cardex:
            messages.info(
                self.request,
                _('La aseguradora no tiene representante en el cardex!')
            )
            if self.request.META['HTTP_REFERER']:
                return self.request.META['HTTP_REFERER']
            else:
                return reverse('invoice-index')

        recibo = Recibo()
        recibo.cajero = self.request.user
        recibo.cliente = aseguradora.cardex
        recibo.credito = True
        recibo.tipo_de_venta = TipoVenta.objects.filter(
            predeterminada=True
        ).first()

        recibo.save()
        for master in aseguradora.master_contracts().all():
            venta = Venta()
            venta.item = master.plan.item
            venta.recibo = recibo
            venta.descripcion = _('Poliza {0}  {1}').format(
                master.poliza,
                master.contratante.nombre
            )
            venta.cantidad = master.active_contracts_count()
            venta.precio = master.plan.item.precio_de_venta
            venta.impuesto = master.plan.item.impuestos
            venta.save()

        recibo.save()

        messages.info(
            self.request,
            _('¡La consulta se marcó como facturada!')
        )

        return recibo.get_absolute_url()

    @method_decorator(permission_required('invoice.cajero'))
    def dispatch(self, *args, **kwargs):
        return super(AseguradoraContractsFacturarView, self).dispatch(*args,
                                                                      **kwargs)


class AseguradoraContractsCotizarView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self, **kwargs):

        if self.request.user.profile.ciudad is None:
            messages.info(
                self.request,
                _('No puede facturar sin tener ciudad en su perfil!')
            )
            if self.request.META['HTTP_REFERER']:
                return self.request.META['HTTP_REFERER']
            else:
                return reverse('invoice-index')

        aseguradora = get_object_or_404(Aseguradora, pk=kwargs['pk'])

        if not aseguradora.cardex:
            messages.info(
                self.request,
                _('La aseguradora no tiene representante en el cardex!')
            )
            if self.request.META['HTTP_REFERER']:
                return self.request.META['HTTP_REFERER']
            else:
                return reverse('invoice-index')

        cotizacion = Cotizacion()
        cotizacion.usuario = self.request.user
        cotizacion.persona = aseguradora.cardex
        cotizacion.credito = True
        cotizacion.tipo_de_venta = TipoVenta.objects.filter(
            predeterminada=True
        ).first()

        cotizacion.save()
        for master in aseguradora.master_contracts().filter(
                facturar_al_administrador=False).all():
            cotizado = Cotizado()
            cotizado.item = master.plan.item
            cotizado.cotizacion = cotizacion
            cotizado.descripcion = _('Poliza {0}  {1}').format(
                master.poliza,
                master.contratante.nombre
            )
            cotizado.cantidad = master.active_contracts_count()
            cotizado.precio = master.plan.item.precio_de_venta
            cotizado.impuesto = master.plan.item.impuestos
            cotizado.save()

        cotizacion.save()

        messages.info(
            self.request,
            _('¡La consulta se marcó como facturada!')
        )

        return cotizacion.get_absolute_url()

    @method_decorator(permission_required('invoice.cajero'))
    def dispatch(self, *args, **kwargs):
        return super(AseguradoraContractsCotizarView, self).dispatch(*args,
                                                                     **kwargs)


class AseguradoraListView(LoginRequiredMixin, ListView):
    """
    Shows the interface that allows making :class:`Cotizacion` from the
    :class:`MasterContract` of an :class:`Aseguradora`
    """
    model = Aseguradora
    queryset = Aseguradora.objects.prefetch_related(
        'mastercontract_set',
        'mastercontract_set__administrador',
        'mastercontract_set__plan',
        'mastercontract_set__contratante',
    )
    context_object_name = 'aseguradoras'
    template_name = 'invoice/aseguradora_list.html'

    def get_context_data(self, **kwargs):
        context = super(AseguradoraListView, self).get_context_data(**kwargs)

        context['contratos'] = MasterContract.objects.filter(
            facturar_al_administrador=True
        )

        return context


class AseguradoraMasterCotizarView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):

        if self.request.user.profile.ciudad is None:
            messages.info(
                self.request,
                _('No puede facturar sin tener ciudad en su perfil!')
            )
            if self.request.META['HTTP_REFERER']:
                return self.request.META['HTTP_REFERER']
            else:
                return reverse('invoice-index')

        aseguradora = get_object_or_404(Aseguradora, pk=kwargs['pk'])

        cotizacion = Cotizacion()
        cotizacion.usuario = self.request.user
        cotizacion.persona = aseguradora.cardex
        cotizacion.credito = True
        cotizacion.tipo_de_venta = TipoVenta.objects.filter(
            predeterminada=True
        ).first()

        cotizacion.save()
        for master in aseguradora.master_contracts().filter(
                facturar_al_administrador=False).all():
            cotizado = Cotizado()
            cotizado.item = master.plan.item
            cotizado.cotizacion = cotizacion
            cotizado.descripcion = _('Poliza {0}  {1}').format(
                master.poliza,
                master.contratante.nombre
            )
            cotizado.cantidad = 1
            cotizado.precio = master.item.precio_de_venta
            cotizado.impuesto = master.plan.item.impuestos
            cotizado.save()
            cotizacion.cotizado_set.add(cotizado)
            cotizado.save()

        cotizacion.save()

        messages.info(
            self.request,
            _('¡La consulta se marcó como facturada!')
        )
        return cotizacion.get_absolute_url()


class MasterCotizarView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):

        if self.request.user.profile.ciudad is None:
            messages.info(
                self.request,
                _('No puede facturar sin tener ciudad en su perfil!')
            )
            if self.request.META['HTTP_REFERER']:
                return self.request.META['HTTP_REFERER']
            else:
                return reverse('invoice-index')

        master = get_object_or_404(MasterContract, pk=kwargs['pk'])

        cotizacion = Cotizacion()
        cotizacion.usuario = self.request.user
        cotizacion.persona = master.administrador
        cotizacion.credito = True
        cotizacion.tipo_de_venta = TipoVenta.objects.filter(
            predeterminada=True
        ).first()

        cotizacion.save()

        cotizado = Cotizado()
        cotizado.item = master.plan.item
        cotizado.cotizacion = cotizacion
        cotizado.descripcion = _('Poliza {0}  {1}').format(
            master.poliza,
            master.contratante.nombre
        )
        cotizado.cantidad = master.active_contracts_count()
        cotizado.precio = master.plan.item.precio_de_venta
        cotizado.impuesto = master.plan.item.impuestos
        cotizado.save()

        cotizacion.save()

        messages.info(
            self.request,
            _('¡La consulta se marcó como facturada!')
        )
        return cotizacion.get_absolute_url()


class AseguradoraMasterFacturarView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self, **kwargs):

        if self.request.user.profile.ciudad is None:
            messages.info(
                self.request,
                _('No puede facturar sin tener ciudad en su perfil!')
            )
            if self.request.META['HTTP_REFERER']:
                return self.request.META['HTTP_REFERER']
            else:
                return reverse('invoice-index')

        aseguradora = get_object_or_404(Aseguradora, pk=kwargs['pk'])

        recibo = Recibo()
        recibo.cajero = self.request.user
        recibo.cliente = aseguradora.cardex
        recibo.credito = True
        recibo.tipo_de_venta = TipoVenta.objects.filter(
            predeterminada=True
        ).first()

        recibo.save()
        for master in aseguradora.master_contracts().all():
            venta = Venta()
            venta.item = master.plan.item
            venta.recibo = recibo
            venta.descripcion = _('Poliza {0}  {1}').format(
                master.poliza,
                master.contratante.nombre
            )
            venta.cantidad = 1
            venta.precio = master.item.precio_de_venta
            venta.impuesto = master.plan.item.impuestos
            venta.save()

        recibo.save()

        messages.info(
            self.request,
            _('¡La consulta se marcó como facturada!')
        )
        return recibo.get_absolute_url()

    @method_decorator(permission_required('invoice.cajero'))
    def dispatch(self, *args, **kwargs):
        return super(AseguradoraMasterFacturarView, self).dispatch(*args,
                                                                   **kwargs)


class ExamenFacturarView(LoginRequiredMixin, UpdateView):
    """Permite crear de manera automática un :class:`Recibo` con todas sus
    :class:`Ventas` a partir de una :class:`Admision` que aun no se haya marcado
    como facturada"""

    model = Examen
    context_object_name = 'examen'
    form_class = ExamenFacturarForm
    template_name = 'invoice/examen_form.html'

    @method_decorator(permission_required('invoice.cajero'))
    def dispatch(self, *args, **kwargs):
        return super(ExamenFacturarView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):

        if self.request.user.profile.ciudad is None:
            messages.info(
                self.request,
                _('No puede facturar sin tener ciudad en su perfil!')
            )
            if self.request.META['HTTP_REFERER']:
                return HttpResponseRedirect(self.request.META['HTTP_REFERER'])
            else:
                return HttpResponseRedirect(reverse('invoice-index'))

        self.object = form.save(commit=False)

        items = self.object.facturar()

        recibo = Recibo()
        recibo.cajero = self.request.user
        recibo.cliente = self.object.persona
        recibo.tipo_de_venta = self.object.tipo_de_venta
        recibo.save()

        crear_ventas(items, recibo)
        self.object.save()

        return HttpResponseRedirect(recibo.get_absolute_url())


class AdmisionAltaView(LoginRequiredMixin, ListView):
    """Muestra una lista de :class:`Admisiones` que aun no han sido
    facturadas"""

    context_object_name = 'admisiones'
    template_name = 'invoice/admisiones.html'
    paginate_by = 10

    def get_queryset(self):
        """Obtiene las :class:`Admision`es que aun no han sido facturadas"""

        return Admision.objects.filter(facturada=False)


class CorteView(ReciboPeriodoView):
    template_name = 'invoice/corte.html'
    prefix = 'corte'
    form_class = CorteForm

    def get_context_data(self, **kwargs):
        context = super(CorteView, self).get_context_data(**kwargs)
        context['cajero'] = self.form.cleaned_data['usuario']
        context['recibos'] = self.recibos.filter(cajero=context['cajero'])
        context['inicio'] = self.inicio
        context['fin'] = self.fin
        context['total'] = context['recibos'].annotate(
            sold=Coalesce(Sum('ventas__total'), Decimal())
        ).aggregate(total=Coalesce(Sum('sold'), Decimal()))['total']
        return context


class ReciboInventarioView(ReciboPeriodoView):
    template_name = 'invoice/recibo_inventario_list.html'
    prefix = 'inventario'

    def get_context_data(self, **kwargs):

        context = super(ReciboInventarioView, self).get_context_data(**kwargs)

        items = defaultdict(lambda: defaultdict(int))

        ventas = Venta.objects.filter(recibo__created__gte=self.inicio,
                                      recibo__created__lte=self.fin)

        for venta in ventas.all():
            items[venta.item]['cantidad'] += venta.cantidad

        queryset = ItemTemplate.objects.annotate(
            total=models.Sum('items__cantidad'))

        for item in queryset.all():

            if item in items:
                items[item]['inventario'] = item.total

        context['inicio'] = self.inicio
        context['items'] = items.items()
        context['fin'] = self.fin
        return context


class TurnoCajaDetailView(LoginRequiredMixin, DetailView):
    model = TurnoCaja
    context_object_name = "turno"


class TurnoCajaCreateView(CurrentUserFormMixin, CreateView):
    model = TurnoCaja
    form_class = TurnoCajaForm


class TurnoCajaUpdateView(LoginRequiredMixin, UpdateView):
    model = TurnoCaja
    form_class = TurnoCajaForm


class TurnoCajaFormMixin(LoginRequiredMixin, CreateView):
    def dispatch(self, *args, **kwargs):
        self.turno = get_object_or_404(TurnoCaja, pk=kwargs['turno'])
        return super(TurnoCajaFormMixin, self).dispatch(*args, **kwargs)

    def get_initial(self):
        initial = super(TurnoCajaFormMixin, self).get_initial()
        initial = initial.copy()
        initial['turno'] = self.turno.id
        return initial


class TurnoCajaListView(LoginRequiredMixin, ListView):
    model = TurnoCaja
    context_object_name = 'turnos'

    def get_queryset(self):
        return TurnoCaja.objects.filter(finalizado=False).all()


class CierreTurnoCreateView(TurnoCajaFormMixin):
    model = CierreTurno
    form_class = CierreTurnoForm


class CierreTurnoDeleteView(DeleteView, LoginRequiredMixin):
    """Permite eliminar un :class:`CierreTurno` que sea incorrecto en el
    :class:`TurnoCaja`"""
    model = CierreTurno

    def get_object(self, queryset=None):
        obj = super(CierreTurnoDeleteView, self).get_object(queryset)
        self.turno = obj.turno
        return obj

    def get_success_url(self):
        return self.turno.get_absolute_url()


class TurnoCierreUpdateView(LoginRequiredMixin, UpdateView):
    """
    Permite cerrar un :class:`TurnoCierre`
    """
    model = TurnoCaja
    form_class = TurnoCajaCierreForm

    def form_valid(self, form):
        self.object = form.save(commit=False)

        recibos = self.object.recibos().filter(cerrado=False).count()
        consultas = Consulta.objects.filter(
            tipo__facturable=True,
            consultorio__usuario__profile__ciudad=self.object.usuario.profile.ciudad,
            facturada=False,
            activa=False
        ).count()
        emergencias = Emergencia.objects.filter(
            facturada=False,
            usuario__profile__ciudad=self.object.usuario.profile.ciudad
        ).count()

        cerrable = True

        if recibos > 0 or consultas > 0 or emergencias > 0:
            messages.info(
                self.request,
                _('Aún hay items pendientes de facturacion')
            )
            cerrable = False

        if self.object.diferencia_total() != 0:
            messages.info(
                self.request,
                _(
                    'No se puede cerrar el turno, tiene diferencias en saldos')
            )
            cerrable = False

        if cerrable:
            self.object.finalizado = True
            self.object.fin = timezone.now()
            self.object.save()

        return HttpResponseRedirect(self.object.get_absolute_url())


class TurnoCajaPeriodoView(LoginRequiredMixin, FormMixin, TemplateView):
    """
    Obtiene los :class:`TurnoCaja` que han sido cerrados en un  periodo
    determinado
    """
    form_class = PeriodoCiudadForm
    prefix = 'turno-periodo'
    template_name = 'invoice/turno_periodo.html'

    def dispatch(self, request, *args, **kwargs):
        """Efectua la consulta de los :class:`TurnoCaja` de acuerdo a los
        datos ingresados en el formulario"""

        self.form = self.get_form_class()(request.GET, prefix=self.prefix)

        if self.form.is_valid():
            self.inicio = self.form.cleaned_data['inicio']
            self.fin = self.form.cleaned_data['fin']
            self.ciudad = self.form.cleaned_data['ciudad']
            self.recibos = Recibo.objects.filter(
                created__gte=self.inicio,
                created__lte=self.fin,
            )
            self.turnos = TurnoCaja.objects.filter(
                fin__gte=self.inicio,
                fin__lte=self.fin,
            )
        else:
            messages.info(
                self.request,
                _('Los Datos Ingresados en el formulario no son validos')
            )
            return HttpResponseRedirect(reverse('invoice-index'))

        return super(TurnoCajaPeriodoView, self).dispatch(request, *args,
                                                          **kwargs)

    def get_context_data(self, **kwargs):
        """Agrega el formulario de :class:`Recibo`"""

        context = super(TurnoCajaPeriodoView, self).get_context_data(**kwargs)
        context['turnos'] = self.turnos
        context['inicio'] = self.inicio
        context['fin'] = self.fin
        context['ciudad'] = self.ciudad
        context['total'] = Venta.objects.filter(
            recibo__in=self.recibos,
            recibo__nulo=False
        ).aggregate(total=Coalesce(Sum('total'), Decimal()))['total']
        context['dias'] = []

        tipos = TipoPago.objects.order_by('orden').filter(reportable=True).all()
        context['tipos'] = tipos

        for day in daterange(self.inicio, self.fin + timedelta(1)):
            inicio = make_day_start(day)
            fin = make_end_day(day)
            pagos = CierreTurno.objects.filter(
                turno__inicio__gte=inicio,
                turno__inicio__lte=fin,
                turno__usuario__profile__ciudad=self.ciudad
            )
            apertura = TurnoCaja.objects.filter(
                inicio__gte=inicio, inicio__lte=fin
            ).aggregate(apertura=Coalesce(Sum('apertura'), Decimal()))[
                'apertura']
            pagos_list = []
            for tipo in tipos:
                pagos_set = (tipo.nombre, pagos.filter(
                    pago=tipo
                ).aggregate(
                    monto=Coalesce(Sum('monto'), Decimal())
                )['monto'])
                pagos_list.append(pagos_set)

            total = pagos.aggregate(
                total=Coalesce(Sum('monto'), Decimal())
            )['total']
            dia = {'fecha': day, 'pagos': pagos_list, 'total': total,
                   'apertura': apertura}
            context['dias'].append(dia)

        return context


class DepositoDetailView(LoginRequiredMixin, DetailView):
    model = Deposito
    context_object_name = 'deposito'


class DepositoFacturarView(LoginRequiredMixin, UpdateView):
    model = Deposito
    form_class = DepositoForm

    def form_valid(self, form):

        if self.request.user.profile.ciudad is None:
            messages.info(
                self.request,
                _('No puede facturar sin tener ciudad en su perfil!')
            )
            if self.request.META['HTTP_REFERER']:
                return HttpResponseRedirect(self.request.META['HTTP_REFERER'])
            else:
                return HttpResponseRedirect(reverse('invoice-index'))

        self.object = form.save(commit=False)

        recibo = Recibo()
        recibo.cajero = self.request.user
        recibo.cliente = self.object.admision.paciente
        recibo.save()

        venta = Venta()
        venta.item = self.request.user.profile.ciudad.company.deposito
        venta.recibo = recibo
        venta.cantidad = 1
        venta.precio = self.object.monto
        venta.impuesto = 0
        venta.descontable = False
        venta.save()

        return HttpResponseRedirect(recibo.get_absolute_url())


class VentaAreaListView(LoginRequiredMixin, ListView):
    context_object_name = 'ventas'

    def dispatch(self, request, *args, **kwargs):
        self.form = PeriodoAreaForm(request.GET, prefix='venta-area')
        if self.form.is_valid():
            self.inicio = self.form.cleaned_data['inicio']
            self.fin = self.form.cleaned_data['fin']
            self.item_type = self.form.cleaned_data['area']

        return super(VentaAreaListView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Venta.objects.filter(
            recibo__created__gte=self.inicio,
            recibo__created__lte=self.fin,
            recibo__nulo=False,
            item__item_type=self.item_type,
        )

    def get_context_data(self, **kwargs):
        context = super(VentaAreaListView, self).get_context_data(**kwargs)
        context['item_type'] = self.item_type
        context['inicio'] = self.inicio
        context['fin'] = self.fin
        context['total'] = self.get_queryset().aggregate(
            total=Sum('total')
        )['total']
        return context


class CiudadPeriodoListView(LoginRequiredMixin, ListView):
    """
    Displays all :class:`Recibo` that have been created in a :class:`Ciudad`
    during a certain date range.
    """
    context_object_name = 'recibos'

    def dispatch(self, request, *args, **kwargs):
        self.form = PeriodoCiudadForm(request.GET, prefix='ciudad-periodo')
        if self.form.is_valid():
            self.inicio = self.form.cleaned_data['inicio']
            self.fin = self.form.cleaned_data['fin']
            self.ciudad = self.form.cleaned_data['ciudad']

        return super(CiudadPeriodoListView, self).dispatch(request, *args,
                                                           **kwargs)

    def get_queryset(self):
        return Recibo.objects.filter(
            created__range=(self.inicio, self.fin),
            nulo=False,
            ciudad=self.ciudad
        )

    def get_context_data(self, **kwargs):
        context = super(CiudadPeriodoListView, self).get_context_data(**kwargs)
        context['inicio'] = self.inicio
        context['fin'] = self.fin
        context['total'] = self.get_queryset().aggregate(
            total=Sum('ventas__total')
        )['total']
        return context


class TipoPagoPeriodoView(LoginRequiredMixin, ListView):
    context_object_name = 'pagos'

    def dispatch(self, request, *args, **kwargs):
        self.form = TipoPagoPeriodoForm(request.GET, prefix='tipopago')
        if self.form.is_valid():
            self.inicio = self.form.cleaned_data['inicio']
            self.fin = self.form.cleaned_data['fin']
            self.tipo_pago = self.form.cleaned_data['tipo']

        return super(TipoPagoPeriodoView, self).dispatch(request, *args,
                                                         **kwargs)

    def get_queryset(self):
        return Pago.objects.filter(
            recibo__created__range=(self.inicio, self.fin),
            tipo=self.tipo_pago,
        ).select_related(
            'aseguradora',
            'recibo__cliente',
            'recibo__cajero',
            'recibo__ciudad',
            'recibo__legal_data',
        ).annotate(
            valor=(
                Coalesce(
                    Sum('recibo__ventas__total'),
                    Decimal()
                )
            )
        )

    def get_context_data(self, **kwargs):
        context = super(TipoPagoPeriodoView, self).get_context_data(**kwargs)
        context['tipo'] = self.tipo_pago
        context['inicio'] = self.inicio
        context['fin'] = self.fin
        context['total'] = self.get_queryset().aggregate(
            total=Sum('monto')
        )['total']
        return context


class StatusPagoListView(LoginRequiredMixin, ListView):
    model = StatusPago
    context_object_name = 'status'

    def get_queryset(self):
        return StatusPago.objects.filter(reportable=True).all()


class CuentaPorCobrarCreateView(CreateView, CurrentUserFormMixin):
    model = CuentaPorCobrar
    form_class = CuentaPorCobrarForm


class CuentaPorCobrarDetailView(LoginRequiredMixin, DetailView):
    model = CuentaPorCobrar
    context_object_name = 'cuenta'


class CuentaPorCobrarListView(LoginRequiredMixin, ListView):
    model = CuentaPorCobrar

    def get_queryset(self):
        return CuentaPorCobrar.objects.filter(status__reportable=True)


class PagoSiguienteStatusView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self, **kwargs):
        pago = get_object_or_404(Pago, pk=kwargs['pk'])
        pago.status = pago.status.next_status
        pago.save()
        messages.info(self.request, _('¡El Pago se ha actualizado!'))

        if self.request.META['HTTP_REFERER']:
            return self.request.META['HTTP_REFERER']
        else:
            return reverse('invoice-index')


class CuentaPorCobrarSiguienteStatusRedirectView(LoginRequiredMixin,
                                                 RedirectView):
    permanent = False

    def get_redirect_url(self, **kwargs):
        cuenta = get_object_or_404(CuentaPorCobrar, pk=kwargs['pk'])
        cuenta.next_status()
        messages.info(self.request, _('¡Se Actualizó la Cuenta por Cobrar!'))

        if self.request.META['HTTP_REFERER']:
            return self.request.META['HTTP_REFERER']
        else:
            return reverse('invoice-index')


class CuentaPorCobrarAnteriorStatusRedirectView(LoginRequiredMixin,
                                                RedirectView):
    permanent = False

    def get_redirect_url(self, **kwargs):
        cuenta = get_object_or_404(CuentaPorCobrar, pk=kwargs['pk'])
        cuenta.previous_status()
        messages.info(self.request, _('¡Se Actualizó la Cuenta por Cobrar!'))

        if self.request.META['HTTP_REFERER']:
            return self.request.META['HTTP_REFERER']
        else:
            return reverse('invoice-index')


class CuentaPorCobrarMixin(ContextMixin, View):
    def dispatch(self, *args, **kwargs):
        self.cuenta = get_object_or_404(CuentaPorCobrar, pk=kwargs['cuenta'])
        return super(CuentaPorCobrarMixin, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CuentaPorCobrarMixin, self).get_context_data(**kwargs)

        context['cuenta'] = self.cuenta

        return context


class CuentaPorCobrarFormMixin(CuentaPorCobrarMixin, FormMixin):
    def get_initial(self):
        initial = super(CuentaPorCobrarFormMixin, self).get_initial()
        initial['cuenta'] = self.cuenta.id
        return initial


class PagoCuentaCreateView(LoginRequiredMixin, CuentaPorCobrarFormMixin,
                           CreateView):
    model = PagoCuenta
    form_class = PagoCuentaForm


class NotificationDetailView(LoginRequiredMixin, DetailView):
    model = Notification
    context_object_name = 'notification'


class CotizacionCreateView(CreateView, PersonaFormMixin, CurrentUserFormMixin,
                           LoginRequiredMixin):
    """Permite crear un :class:`Cotizacion` utilizando una :class:`Persona`
    existente en la aplicación
    """

    model = Cotizacion
    form_class = CotizacionForm
    template_name = 'invoice/recibo_persona_create.html'


class CotizacionDetailView(LoginRequiredMixin, DetailView):
    model = Cotizacion
    queryset = Cotizacion.objects.select_related(
        'persona',
        'tipo_de_venta'
    ).prefetch_related(
        'cotizado_set',
        'cotizado_set__item'
    )


class CotizacionMixin(ContextMixin, View):
    def dispatch(self, *args, **kwargs):
        self.cotizacion = get_object_or_404(Cotizacion, pk=kwargs['cotizacion'])
        return super(CotizacionMixin, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CotizacionMixin, self).get_context_data(**kwargs)

        context['cotizacion'] = self.cotizacion

        return context


class CotizacionFormMixin(CotizacionMixin, FormMixin):
    def get_initial(self):
        initial = super(CotizacionFormMixin, self).get_initial()
        initial['cotizacion'] = self.cotizacion.id
        return initial


class CotizadoCreateView(LoginRequiredMixin, CotizacionFormMixin, CreateView):
    model = Cotizado
    form_class = CotizadoForm


class CotizadoUpdateView(LoginRequiredMixin, UpdateView):
    model = Cotizado
    form_class = CotizadoForm


class CotizadoDeleteView(LoginRequiredMixin, DeleteView):
    model = Cotizado

    def get_object(self, queryset=None):
        obj = super(CotizadoDeleteView, self).get_object(queryset)
        self.cotizacion = obj.cotizacion
        return obj

    def get_success_url(self):
        return self.cotizacion.get_absolute_url()


class CotizacionFacturar(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        cotizacion = get_object_or_404(Cotizacion, pk=kwargs['pk'])
        recibo = cotizacion.facturar()
        messages.info(self.request, _('¡Se ha facturado la cotización!'))
        return recibo.get_absolute_url()


class ComprobanteDeduccionCreateView(LoginRequiredMixin, CreateView):
    model = ComprobanteDeduccion
    form_class = ComprobanteDeduccionForm


class ComprobanteDeduccionDetailView(LoginRequiredMixin, DetailView):
    model = ComprobanteDeduccion
    context_object_name = 'comprobante'


class ComprobanteDeduccionMixin(ContextMixin):
    """Agrega una :class:`Persona` en la vista"""

    def dispatch(self, *args, **kwargs):
        self.comprobante = get_object_or_404(ComprobanteDeduccion,
                                             pk=kwargs['comprobante'])
        return super(ComprobanteDeduccionMixin, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ComprobanteDeduccionMixin, self).get_context_data(
            **kwargs)
        context['comprobante'] = self.comprobante
        return context


class ComprobanteDeduccionFormMixin(FormMixin, ComprobanteDeduccionMixin):
    """Agrega la :class:`Persona` a los argumentos iniciales de un formulario"""

    def get_initial(self):
        initial = super(ComprobanteDeduccionFormMixin, self).get_initial()
        initial = initial.copy()
        initial['comprobante'] = self.comprobante
        return initial


class ComprobanteDeduccionListView(LoginRequiredMixin, ListView):
    """
    Shows a list of :class:`ComprobanteDeduccion` with links to their detail
    pages
    """
    model = ComprobanteDeduccion
    paginate_by = 20


class ConceptoDeduccionCreateView(LoginRequiredMixin,
                                  ComprobanteDeduccionFormMixin, CreateView):
    model = ConceptoDeduccion
    form_class = ConceptoDeduccionForm


class NotaCreditoCreateView(LoginRequiredMixin, CreateView):
    model = NotaCredito
    form_class = NotaCreditoForm


class NotaCreditoMixin(ContextMixin, View):
    """Agrega una :class:`NotaCredito` en la vista"""

    def dispatch(self, *args, **kwargs):
        self.nota_credito = get_object_or_404(ComprobanteDeduccion,
                                              pk=kwargs['nota_credito'])
        return super(NotaCreditoMixin, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(NotaCreditoMixin, self).get_context_data(
            **kwargs)
        context['nota_credito'] = self.nota_credito
        return context


class NotaCreditoFormMixin(FormMixin, NotaCreditoMixin):
    """
    Agrega la :class:`NotaCredito` a los argumentos iniciales de un formulario
    """

    def get_initial(self):
        initial = super(NotaCreditoFormMixin, self).get_initial()
        initial['nota'] = self.nota_credito
        return initial


class DetalleCreditoCreateView(LoginRequiredMixin, CreateView,
                               NotaCreditoFormMixin):
    """
    Adds a :class:`DetalleCredito` to a :class:`NotaCredito`
    """
    model = DetalleCredito


class ReembolsoCreateView(LoginRequiredMixin, FormView):
    form_class = ReembolsoForm
    template_name = 'invoice/reembolso_form.html'

    def form_valid(self, form):
        porcentaje = form.cleaned_data['porcentaje']

        pago = Pago()
        pago.tipo = form.cleaned_data['tipo_de_pago']
        pago.recibo = form.cleaned_data['recibo']
        pago.monto = pago.recibo.total() * porcentaje / 100
        pago.comprobante = _('Reembolso')
        pago.aseguradora = form.cleaned_data['aseguradora']
        pago.save()

        return HttpResponseRedirect(pago.recibo.get_absolute_url())
