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
from django.shortcuts import get_object_or_404, redirect
from invoice.models import Recibo, Producto, Venta
from invoice.forms import ReciboForm, VentaForm, PeriodoForm
from django.contrib.auth.models import User
from django.views.generic import (CreateView, UpdateView, DeleteView,
    TemplateView, DetailView, ListView, RedirectView)
from library.protected import LoginRequiredView
from django import forms
from persona.models import Persona
from datetime import datetime, time
from django.utils import timezone
from collections import defaultdict
from decimal import Decimal

class ReciboPersonaCreateView(CreateView, LoginRequiredView):

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

class VentaCreateView(CreateView, LoginRequiredView):
    
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
        
        #messages.info(self.request, u"Agregada una Venta al Recibo!")
        
        return HttpResponseRedirect(self.get_success_url())

class ReciboDetailView(DetailView, LoginRequiredView):

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
        
        return context

class ReciboAnularView(RedirectView, LoginRequiredView):

    """Marca un :class:`Recibo` como anulado para que la facturación del mismo
    no se vea reflejado en los cortes de caja"""
    
    permanent = False
    
    def get_redirect_url(self, **kwargs):
        
        recibo = get_object_or_404(Recibo, pk=kwargs['pk'])
        recibo.anular()
        messages.info(self.request, u'¡El recibo ha sido marcado como anulado!')
        return reverse('recibo-view', args=[recibo.id])

class IndexView(TemplateView, LoginRequiredView):
    
    """Muestra las opciones disponibles para la aplicación"""

    template_name = 'invoice/index.html'
    
    def get_context_data(self, **kwargs):
        
        """Agrega el formulario de :class:`Recibo`"""
        
        context = super(IndexView, self).get_context_data(**kwargs)
        context['reciboperiodoform'] = PeriodoForm(prefix='recibo')
        context['productoperiodoform'] = PeriodoForm(prefix='producto')
        context['remiteperiodoform'] = PeriodoForm(prefix='remite')

        return context

class ReciboPeriodoView(TemplateView):

    """Obtiene los :class:`Recibo` de un periodo determinado en base
    a un formulario que las clases derivadas deben proporcionar como
    self.form"""

    def dispatch(self, request, *args, **kwargs):

        """Efectua la consulta de los :class:`Recibo` de acuerdo a los
        datos ingresados en el formulario"""

        if self.form.is_valid():

            inicio = self.form.cleaned_data['inicio']
            fin = self.form.cleaned_data['fin']
            self.inicio = timezone.make_aware(
                                    datetime.combine(inicio, time.min),
                                    timezone.get_default_timezone())
            self.fin = timezone.make_aware(datetime.combine(fin, time.max),
                                           timezone.get_default_timezone())
            self.recibos = Recibo.objects.filter(created__range=(inicio, fin))

        else:
            
            return redirect('invoice-index')

        return super(ReciboPeriodoView, self).dispatch(request, *args, **kwargs)

class ReporteReciboView(ReciboPeriodoView, LoginRequiredView):

    """Muestra los ingresos captados mediante :class:`Recibo`s que se captaron
    durante el periodo especificado"""

    template_name = 'invoice/recibo_list.html'
    
    def dispatch(self, request, *args, **kwargs):

        """Agrega el formulario"""

        self.form = PeriodoForm(request.GET, prefix='recibo')

        return super(ReporteReciboView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        
        """Agrega el formulario de :class:`Recibo`"""
        
        context = super(ReporteReciboView, self).get_context_data(**kwargs)
        
        context['recibos'] = self.recibos
        context['inicio'] = self.inicio
        context['fin'] = self.fin
        context['total'] = sum(r.total() for r in self.recibos.all())

        return context

class ReporteProductoView(ReciboPeriodoView, LoginRequiredView):

    """Muestra los ingresos captados mediante :class:`Recibo`s, distribuyendo
    los mismos de acuerdo al :class:`Producto` que se facturó, tomando en
    cuenta el periodo especificado"""

    template_name = 'invoice/producto_list.html'
    
    def dispatch(self, request, *args, **kwargs):
        
        """Agrega el formulario"""

        self.form = PeriodoForm(request.GET, prefix='producto')

        return super(ReporteProductoView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        
        """Agrega el formulario de :class:`Recibo`"""
        
        context = super(ReporteProductoView, self).get_context_data(**kwargs)
        
        context['cantidad'] = 0
        productos = defaultdict(lambda: defaultdict(Decimal))
        
        for recibo in self.recibos.all():

            for venta in recibo.ventas.all():

                productos[venta.producto]['monto'] += venta.monto()
                productos[venta.producto]['cantidad'] += 1
                
                context['cantidad'] += 1

        context['recibos'] = self.recibos
        context['productos'] = productos.items()
        context['impuesto'] = sum(r.impuesto() for r in self.recibos.all())
        context['inicio'] = self.inicio
        context['fin'] = self.fin
        return context

class ReciboRemiteView(ReciboPeriodoView, LoginRequiredView):
    
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
        
        context['cantidad'] = 0
        doctores = defaultdict(lambda: defaultdict(Decimal))
        
        for recibo in self.recibos.all():

            doctores[recibo.remite]['monto'] += recibo.total()
            doctores[recibo.remite]['cantidad'] += 1
            doctores[recibo.remite]['comision'] =+ recibo.total() * Decimal('0.07')
            context['cantidad'] += recibo.total() * Decimal('0.07')

        context['recibos'] = self.recibos
        context['inicio'] = self.inicio
        context['doctores'] = doctores.items()
        context['fin'] = self.fin
        return context
