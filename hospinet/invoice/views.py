# -*- coding: utf-8 -*-
from invoice.models import Recibo, Producto, Venta
from invoice.forms import ReciboForm, VentaForm
from django.contrib.auth.models import User
from django.views.generic import (CreateView, UpdateView, DeleteView,
                                  TemplateView, DetailView, ListView)
from library.protected import LoginRequiredView
from django import forms

class ReciboCreateView(CreateView, LoginRequiredView):

    """Permite crear :class:`Recibo`s ingresando todos los datos del cliente"""

    model = Recibo
    form_class = ReciboForm

    def get_form_kwargs(self):
        
        """Registra el :class:`User` que esta creando el :class:`Recibo`"""

        kwargs = super(BaseCreateView, self).get_form_kwargs()
        kwargs.update({'initial':{'cajero':self.request.user.id}})
        return kwargs

class VentaCreateView(CreateView, LoginRequiredView):

    """Permite agregar :class:`Venta`s a un :class:`Recibo`"""

    model = Venta
    form_class = VentaForm

    def get_form_kwargs(self):
        
        """Agrega el :class:`Recibo` obtenida como el valor a utilizar en el
        formulario que será llenado posteriormente"""

        kwargs = super(BaseCreateView, self).get_form_kwargs()
        kwargs.update({'initial':{'recibo':self.recibo.id}})
        return kwargs
    
    def dispatch(self, *args, **kwargs):
        
        """Obtiene el :class:`Recibo` que se entrego como argumento en la
        url"""

        self.recibo = get_object_or_404(Recibo, pk=kwargs['recibo'])
        return super(BaseCreateView, self).dispatch(*args, **kwargs)

class ReciboDetailView(DetailView, LoginRequiredView):

    model = Recibo
    object_context_name = 'recibo'
    template_name = 'recibo/recibo_detail.html'

class IndexView(TemplateView, LoginRequiredView):

    template_name = 'recibo/index.html'

class Recibos(ListView, LoginRequiredView):

    model = Recibo
    object_context_name = 'recibos'
    template_name = 'recibo/recibo_list.html'
