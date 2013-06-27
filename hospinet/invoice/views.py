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
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from emergency.models import Emergencia
from invoice.models import Recibo, Venta
from invoice.forms import (ReciboForm, VentaForm, PeriodoForm,
                           EmergenciaFacturarForm, AdmisionFacturarForm,
    CorteForm)
from django.views.generic import (CreateView, UpdateView, TemplateView,
                                  DetailView, ListView, RedirectView)
from persona.models import Persona
from imaging.models import Examen
from spital.models import Admision
from datetime import datetime, time
from collections import defaultdict
from decimal import Decimal
from users.mixins import LoginRequiredMixin
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.models import User
from django.views.generic.edit import FormMixin, FormView
from django.views.generic.dates import DayArchiveView

class ReciboPersonaCreateView(CreateView, LoginRequiredMixin):
    
    """Permite crear un :class:`Recibo` utilizando una :class:`Persona`
    existente en la aplicación"""
    
    model = Recibo
    form_class = ReciboForm
    template_name = 'invoice/recibo_create.html'
    
    def get_form_kwargs(self):
        
        """Registra el :class:`User` que esta creando el :class:`Recibo`"""
        
        kwargs = super(ReciboPersonaCreateView, self).get_form_kwargs()
        kwargs.update({'initial':{'cajero':self.request.user.id,
                                  'cliente':self.persona.id}})
        return kwargs
    
    def dispatch(self, *args, **kwargs):
        
        """Obtiene el :class:`Recibo` que se entrego como argumento en la
        url"""
        
        self.persona = get_object_or_404(Persona, pk=kwargs['persona'])
        return super(ReciboPersonaCreateView, self).dispatch(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        
        context = super(ReciboPersonaCreateView, self).get_context_data(**kwargs)
        context['persona'] = self.persona
        return context

class ReciboExamenCreateView(CreateView, LoginRequiredMixin):
    
    """Permite crear un :class:`Recibo` utilizando una :class:`Persona`
    existente en la aplicación"""
    
    model = Recibo
    form_class = ReciboForm
    template_name = 'invoice/recibo_create.html'
    
    def get_form_kwargs(self):
        
        """Registra el :class:`User` que esta creando el :class:`Recibo`"""
        
        kwargs = super(ReciboExamenCreateView, self).get_form_kwargs()
        kwargs.update({'initial':{'cajero':self.request.user.id,
                                  'cliente':self.examen.persona.id,
                                  'remite':self.examen.remitio}})
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

class VentaCreateView(CreateView, LoginRequiredMixin):
    
    """Permite agregar :class:`Venta`s a un :class:`Recibo`"""
    
    model = Venta
    form_class = VentaForm
    
    def get_form_kwargs(self):
        
        """Agrega el :class:`Recibo` obtenida como el valor a utilizar en el
        formulario que será llenado posteriormente"""
        
        kwargs = super(VentaCreateView, self).get_form_kwargs()
        kwargs.update({'initial':{'recibo':self.recibo.id}})
        return kwargs
    
    def dispatch(self, *args, **kwargs):
        
        """Obtiene el :class:`Recibo` que se entrego como argumento en la
        url"""
        
        self.recibo = get_object_or_404(Recibo, pk=kwargs['recibo'])
        return super(VentaCreateView, self).dispatch(*args, **kwargs)
    
    def form_valid(self, form):
        
        """Guarda el objeto generado espeficando precio obtenido directamente
        del :class:`Producto`"""
        
        self.object = form.save(commit=False)
        self.object.precio = self.object.producto.precio
        self.object.impuesto = self.object.producto.impuesto * self.object.monto()
        self.object.save()
        
        # messages.info(self.request, u"Agregada una Venta al Recibo!")
        
        return HttpResponseRedirect(self.get_success_url())

class ReciboDetailView(DetailView, LoginRequiredMixin):
    
    """Muestra los detalles del :class:`Recibo` para agregar :class:`Producto`s
    ir a la vista de impresión y realizar otras tareas relacionadas con
    facturación"""
    
    model = Recibo
    object_context_name = 'recibo'
    template_name = 'invoice/recibo_detail.html'
    
    def get_context_data(self, **kwargs):
        
        """Agrega el formulario de :class:`Venta` para agregar
        :class:`Producto`s"""
        
        context = super(ReciboDetailView, self).get_context_data(**kwargs)
        context['form'] = VentaForm(initial={'recibo':context['recibo'].id})
        context['form'].helper.form_action = reverse('venta-add', args=[context['recibo'].id])
        
        return context

class ReciboAnularView(RedirectView, LoginRequiredMixin):
    
    """Marca un :class:`Recibo` como anulado para que la facturación del mismo
    no se vea reflejado en los cortes de caja"""
    
    permanent = False
    
    def get_redirect_url(self, **kwargs):
        
        recibo = get_object_or_404(Recibo, pk=kwargs['pk'])
        recibo.anular()
        messages.info(self.request, u'¡El recibo ha sido marcado como anulado!')
        return reverse('invoice-view-id', args=[recibo.id])

class ReciboCerrarView(RedirectView, LoginRequiredMixin):
    
    """Marca un :class:`Recibo` como anulado para que la facturación del mismo
    no se vea reflejado en los cortes de caja"""
    
    permanent = False
    
    def get_redirect_url(self, **kwargs):
        
        recibo = get_object_or_404(Recibo, pk=kwargs['pk'])
        recibo.cerrar()
        messages.info(self.request, u'¡El recibo ha sido cerrado!')
        return reverse('invoice-view-id', args=[recibo.id])

class IndexView(TemplateView, LoginRequiredMixin):
    
    """Muestra las opciones disponibles para la aplicación"""
    
    template_name = 'invoice/index.html'
    
    def get_context_data(self, **kwargs):
        
        """Agrega el formulario de :class:`Recibo`"""
        
        context = super(IndexView, self).get_context_data(**kwargs)
        context['reciboperiodoform'] = PeriodoForm(prefix='recibo')
        context['reciboperiodoform'].set_legend(u'Recibos de un Periodo')
        context['reciboperiodoform'].set_action('invoice-periodo')
        
        context['productoperiodoform'] = PeriodoForm(prefix='producto')
        context['productoperiodoform'].set_legend(u'Productos Facturados en un Periodo')
        context['productoperiodoform'].set_action('invoice-periodo-producto')
        
        context['remiteperiodoform'] = PeriodoForm(prefix='remite')
        context['remiteperiodoform'].set_legend(u'Referencias de un Periodo')
        context['remiteperiodoform'].set_action('invoice-periodo-remite')
        
        context['radperiodoform'] = PeriodoForm(prefix='rad')
        context['radperiodoform'].set_legend(u'Comisiones de un Periodo')
        context['radperiodoform'].set_action('invoice-periodo-radiologo')
        
        context['emerperiodoform'] = PeriodoForm(prefix='emergencia')
        context['emerperiodoform'].set_legend(u'Emergencias de un Periodo')
        context['emerperiodoform'].set_action('invoice-periodo-emergencia')
        
        context['corteform'] = CorteForm(prefix='corte')
        context['corteform'].set_action('invoice-corte')
        
        return context

class ReciboPeriodoView(TemplateView):
    
    """Obtiene los :class:`Recibo` de un periodo determinado en base
    a un formulario que las clases derivadas deben proporcionar como
    self.form"""
    
    def dispatch(self, request, *args, **kwargs):
        
        """Efectua la consulta de los :class:`Recibo` de acuerdo a los
        datos ingresados en el formulario"""
        
        if self.form.is_valid():
            
            self.inicio = self.form.cleaned_data['inicio']
            self.fin = datetime.combine(self.form.cleaned_data['fin'], time.max)
            self.recibos = Recibo.objects.filter(
                created__gte=self.inicio,
                created__lte=self.fin
            )
        
        return super(ReciboPeriodoView, self).dispatch(request, *args, **kwargs)

class ReporteReciboView(ReciboPeriodoView, LoginRequiredMixin):
    
    """Muestra los ingresos captados mediante :class:`Recibo`s que se captaron
    durante el periodo especificado"""
    
    template_name = 'invoice/recibo_list.html'
    
    def dispatch(self, request, *args, **kwargs):
        
        """Agrega el formulario"""
        
        self.form = PeriodoForm(request.GET, prefix='recibo')
        
        return super(ReporteReciboView, self).dispatch(request, *args,
                                                       **kwargs)
    
    def get_context_data(self, **kwargs):
        
        """Agrega el formulario de :class:`Recibo`"""
        
        context = super(ReporteReciboView, self).get_context_data(**kwargs)
        
        context['recibos'] = self.recibos
        context['inicio'] = self.inicio
        context['fin'] = self.fin
        context['total'] = sum(r.total() for r in self.recibos.all())
        
        return context

class ReporteProductoView(ReciboPeriodoView, LoginRequiredMixin):
    
    """Muestra los ingresos captados mediante :class:`Recibo`s, distribuyendo
    los mismos de acuerdo al :class:`Producto` que se facturó, tomando en
    cuenta el periodo especificado"""
    
    template_name = 'invoice/producto_list.html'
    
    def dispatch(self, request, *args, **kwargs):
        
        """Agrega el formulario"""
        
        self.form = PeriodoForm(request.GET, prefix='producto')
        
        return super(ReporteProductoView, self).dispatch(request, *args,
                                                         **kwargs)
    
    def get_context_data(self, **kwargs):
        
        """Agrega el formulario de :class:`Recibo`"""
        
        context = super(ReporteProductoView, self).get_context_data(**kwargs)
        
        context['cantidad'] = 0
        productos = defaultdict(lambda: defaultdict(Decimal))
        
        for recibo in self.recibos.all():
            
            for venta in recibo.ventas.all():
                
                productos[venta.item]['monto'] += venta.monto()
                productos[venta.item]['cantidad'] += 1
                
                context['cantidad'] += 1
                
        context['recibos'] = self.recibos
        context['productos'] = productos.items()
        context['impuesto'] = sum(r.impuesto() for r in self.recibos.all())
        context['inicio'] = self.inicio
        context['fin'] = self.fin
        return context

class ReciboRemiteView(ReciboPeriodoView, LoginRequiredMixin):
    
    """Muestra los ingresos captados mediante :class:`Recibo`s, distribuyendo
    los mismos de acuerdo al :class:`Producto` que se facturó, tomando en
    cuenta el periodo especificado"""
    
    template_name = 'invoice/remite_list.html'
    
    def dispatch(self, request, *args, **kwargs):
        
        """Agrega el formulario"""
        
        self.form = PeriodoForm(request.GET, prefix='remite')
        
        return super(ReciboRemiteView, self).dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        
        """Agrega el formulario de :class:`Recibo`"""
        
        context = super(ReciboRemiteView, self).get_context_data(**kwargs)
        
        context['cantidad'] = Decimal('0')
        doctores = defaultdict(lambda: defaultdict(Decimal))
        
        for recibo in self.recibos.all():
            
            doctores[recibo.remite]['monto'] += recibo.total()
            doctores[recibo.remite]['cantidad'] += 1
            doctores[recibo.remite]['comision'] += recibo.comision_doctor()
        
        context['cantidad'] = sum(doctores[d]['comision'] for d in doctores)
        
        context['recibos'] = self.recibos
        context['inicio'] = self.inicio
        context['doctores'] = doctores.items()
        context['fin'] = self.fin
        return context

class ReciboRadView(ReciboPeriodoView, LoginRequiredMixin):
    
    """Muestra los ingresos captados mediante :class:`Recibo`s, distribuyendo
    los mismos de acuerdo al :class:`Producto` que se facturó, tomando en
    cuenta el periodo especificado"""
    
    template_name = 'invoice/radiologo_list.html'
    
    def dispatch(self, request, *args, **kwargs):
        
        """Agrega el formulario"""
        
        self.form = PeriodoForm(request.GET, prefix='rad')
        
        return super(ReciboRadView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        
        """Agrega el formulario de :class:`Recibo`"""
        
        context = super(ReciboRadView, self).get_context_data(**kwargs)
        
        context['cantidad'] = Decimal('0')
        doctores = defaultdict(lambda: defaultdict(Decimal))
        
        for recibo in self.recibos.all():
            
            doctores[recibo.radiologo]['monto'] += recibo.total()
            doctores[recibo.radiologo]['cantidad'] += 1
            doctores[recibo.radiologo]['comision'] += recibo.comision_radiologo()
        
        context['cantidad'] = sum(doctores[d]['comision'] for d in doctores)
        
        context['recibos'] = self.recibos
        context['inicio'] = self.inicio
        context['doctores'] = doctores.items()
        context['fin'] = self.fin
        return context

class EmergenciaPeriodoView(TemplateView, LoginRequiredMixin):
    
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

class EmergenciaDiaView(ListView, LoginRequiredMixin):
    
    """Muestra los materiales y medicamentos de las :class:`Emergencia`s que
    han sido atendidas durante el día"""
    
    context_object_name = 'emergencias'
    template_name = 'invoice/emergency.html'
    paginate_by = 10
    
    def get_queryset(self):
        
        return Emergencia.objects.filter(facturada=False)

class ExamenView(ListView, LoginRequiredMixin):
    
    """Muestra los materiales y medicamentos de las :class:`Emergencia`s que
    han sido atendidas durante el día"""
    
    context_object_name = 'examenes'
    template_name = 'invoice/examen_list.html'
    paginate_by = 10
    
    def get_queryset(self):
        
        return Examen.objects.filter(facturado=False)

def crear_ventas(items, recibo):
    
    """Permite convertir un :class:`dict` de :class:`ItemTemplate` y sus
    cantidades en una las :class:`Venta`s de un :class:`Recibo`"""
    
    for item in items:
        
        venta = Venta()
        venta.item = item
        venta.recibo = recibo
        venta.cantidad = items[item]
        venta.precio = item.precio_de_venta
        venta.impuesto = item.impuestos
        
        venta.save()
        recibo.ventas.add(venta)

class EmergenciaFacturarView(UpdateView, LoginRequiredMixin):
    
    """Permite crear de manera automática un :class:`Recibo` con todas sus
    :class:`Ventas` a partir de una :class:`Emergencia` que aun no se haya
    marcado como facturada"""
    
    model = Emergencia
    form_class = EmergenciaFacturarForm
    context_object_name = 'emergencia'
    template_name = 'invoice/emergency_form.html'
    
    def form_valid(self, form):
        
        self.object = form.save(commit=False)
        
        items = self.object.facturar()
        
        recibo = Recibo()
        recibo.cajero = self.request.user
        recibo.cliente = self.object.persona
        
        recibo.save()
        
        crear_ventas(items, recibo)
        
        self.object.facturado = True
        self.object.save()
        
        return HttpResponseRedirect(recibo.get_absolute_url())

class AdmisionFacturarView(UpdateView, LoginRequiredMixin):
    
    """Permite crear de manera automática un :class:`Recibo` con todas sus
    :class:`Ventas` a partir de una :class:`Admision` que aun no se haya marcado
    como facturada"""
    
    model = Admision
    context_object_name = 'admision'
    form_class = AdmisionFacturarForm
    template_name = 'invoice/admision_form.html'
    
    def form_valid(self, form):
        
        self.object = form.save(commit=False)
        
        items = self.object.facturar()
        
        recibo = Recibo()
        recibo.cajero = self.request.user
        recibo.cliente = self.object.paciente
        
        recibo.save()
        
        crear_ventas(items, recibo)
        
        self.object.save()
        
        return HttpResponseRedirect(recibo.get_absolute_url())

class AdmisionAltaView(ListView, LoginRequiredMixin):
    
    """Muestra una lista de :class:`Admisiones` que aun no han sido facturadas"""
    
    context_object_name = 'admisiones'
    template_name = 'invoice/admisiones.html'
    paginate_by = 10
    
    def get_queryset(self):
        
        """Obtiene las :class:`Admision`es que aun no han sido facturadas"""
        
        return Admision.objects.filter(facturada=False)

class CorteView(ReciboPeriodoView):
    
    template_name = 'invoice/corte.html'
    
    def get_context_data(self, **kwargs):
        
        context = super(CorteView, self).get_context_data(**kwargs)
        context['cajero'] = self.form.cleaned_data['usuario']
        context['recibos'] = self.recibos.filter(cajero=context['cajero'])
        context['inicio'] = self.inicio
        context['fin'] = self.fin
        context['total'] = sum(r.total() for r in context['recibos'].all())
        return context
    
    def dispatch(self, request, *args, **kwargs):
        
        self.form = CorteForm(request.GET, prefix='corte')
        return super(CorteView, self).dispatch(request, *args, **kwargs)
