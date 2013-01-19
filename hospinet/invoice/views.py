# -*- coding: utf-8 -*-
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
        context['periodoform'] = PeriodoForm()

        return context

class ReporteView(TemplateView, LoginRequiredView):

    model = Recibo
    object_context_name = 'recibos'
    template_name = 'invoice/recibo_list.html'
    
    def get_context_data(self, **kwargs):
        
        """Agrega el formulario de :class:`Recibo`"""
        
        context = super(ReporteView, self).get_context_data(**kwargs)
        form = PeriodoForm(self.request.GET)
        if not form.is_valid():
            redirect('invoice-index')

        inicio = form.cleaned_data['inicio']
        fin = form.cleaned_data['fin']
        recibos = Recibo.objects.filter(created__gte=inicio, created__lte=fin)
        
        context['recibos'] = recibos
        return context
