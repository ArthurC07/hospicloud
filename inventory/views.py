# -*- coding: utf-8 -*-
#
# Copyright (C) 2011-2016 Carlos Flores <cafg10@gmail.com>
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

from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.generic import (CreateView, DetailView, UpdateView, ListView,
                                  DeleteView, View)
from django.views.generic.base import TemplateView, ContextMixin
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormMixin

from inventory.forms import InventarioForm, ItemTemplateForm, ItemTypeForm, \
    HistorialForm, ItemForm, RequisicionForm, ItemRequisicionForm, \
    TransferenciaForm, TransferidoForm, CompraForm, TransferirForm, \
    ItemTemplateSearchForm, RequisicionCompletarForm, ItemCompradoForm, \
    ProveedorForm, CotizacionForm, ItemCotizadoform, CotizacionAutorizarForm, \
    CotizacionDenegarForm, CotizacionComprarForm
from inventory.models import Inventario, Item, ItemTemplate, Transferencia, \
    Historial, ItemComprado, Transferido, Compra, ItemType, Requisicion, \
    ItemRequisicion, ItemHistorial, Proveedor, Cotizacion, ItemCotizado
from users.mixins import LoginRequiredMixin, CurrentUserFormMixin


class InventarioPermissionMixin(LoginRequiredMixin):
    @method_decorator(permission_required('inventory.inventario'))
    def dispatch(self, *args, **kwargs):
        return super(InventarioPermissionMixin, self).dispatch(*args, **kwargs)


class IndexView(TemplateView, InventarioPermissionMixin):
    """
    Displays an entry point for :class:`Inventory`
    """
    template_name = 'inventory/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        context['inventarios'] = Inventario.objects.filter(activo=True).all()
        context['productoform'] = ItemTemplateSearchForm()
        context['productoform'].helper.form_tag = False

        context['pendientes'] = Cotizacion.objects.pendientes().select_related(
            'proveedor'
        )
        context[
            'autorizadas'] = Cotizacion.objects.autorizadas().select_related(
            'proveedor'
        )

        context['compras'] = Compra.objects.filter(transferida=False)

        denegar_form = CotizacionDenegarForm()
        context['denegar'] = denegar_form
        denegar_form.helper.form_tag = False

        autorizar_form = CotizacionAutorizarForm()
        context['autorizar'] = autorizar_form
        autorizar_form.helper.form_tag = False

        comprar_form = CotizacionComprarForm()
        context['comprar'] = comprar_form
        comprar_form.helper.form_tag = False

        return context


class InventarioMixin(ContextMixin, View):
    """
    Adds :class:`Inventario` to child views
    """

    def dispatch(self, *args, **kwargs):
        self.inventario = get_object_or_404(Inventario, pk=kwargs['inventario'])
        return super(InventarioMixin, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['inventario'] = self.inventario
        return super(InventarioMixin, self).get_context_data(**kwargs)


class InventarioFormMixin(FormMixin, InventarioMixin):
    """
    Adds the :class:`Inventario` to the form used in the view
    """

    def get_initial(self):
        initial = super(InventarioFormMixin, self).get_initial()
        initial = initial.copy()
        initial['inventario'] = self.inventario.id
        return initial


class ItemTemplateDetailView(LoginRequiredMixin, DetailView):
    """
    Displays the data related to a :class:`ItemTemplate`
    """
    model = ItemTemplate
    context_object_name = 'item_template'


class ItemTemplateListView(LoginRequiredMixin, ListView):
    model = ItemTemplate
    context_object_name = 'item_templates'


class ItemTemplateCreateView(LoginRequiredMixin, CreateView):
    model = ItemTemplate
    form_class = ItemTemplateForm


class ItemTypeCreateView(LoginRequiredMixin, CreateView):
    model = ItemType
    form_class = ItemTypeForm


class ItemTypeDetailView(LoginRequiredMixin, DetailView):
    model = ItemType


class ItemTypeListView(LoginRequiredMixin, ListView):
    model = ItemType


class ItemTemplateUpdateView(LoginRequiredMixin, UpdateView):
    model = ItemTemplate
    form_class = ItemTemplateForm


class InventarioListView(LoginRequiredMixin, ListView):
    model = Inventario
    context_object_name = 'inventarios'
    paginate_by = 10


class InventarioDetailView(SingleObjectMixin, LoginRequiredMixin, ListView):
    paginate_by = 10
    template_name = 'inventory/inventario_detail.html'

    def get_context_data(self, **kwargs):
        kwargs['inventario'] = self.object
        return super(InventarioDetailView, self).get_context_data(**kwargs)

    def get_queryset(self):
        self.object = self.get_object(Inventario.objects.all())
        return self.object.items()


class InventarioCreateView(LoginRequiredMixin, CreateView):
    model = Inventario
    form_class = InventarioForm


class ItemListView(LoginRequiredMixin, ListView):
    model = Item
    context_object_name = 'items'
    paginate_by = 10


class ItemInventarioListView(LoginRequiredMixin, ListView):
    model = Item
    context_object_name = 'items'

    def dispatch(self, *args, **kwargs):
        self.inventario = get_object_or_404(Inventario, pk=kwargs['inventario'])
        return super(ItemInventarioListView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['inventario'] = self.inventario
        return super(ItemInventarioListView, self).get_context_data(**kwargs)

    def get_queryset(self):
        return Item.objects.filter(inventario=self.inventario).all()


class ItemCreateView(InventarioFormMixin, LoginRequiredMixin):
    model = Item
    form_class = ItemForm

    def get_context_data(self, **kwargs):
        extra_form = ItemTemplateForm()
        extra_form.helper.form_action = reverse('itemtemplate-create')
        extra_form.helper.form_id = 'add-item-form'
        kwargs['itemTemplateForm'] = extra_form
        return super(ItemCreateView, self).get_context_data(**kwargs)


class ItemDetailView(LoginRequiredMixin, ListView):
    model = Item
    context_object_name = 'item'


class RequisicionDetailView(SingleObjectMixin, LoginRequiredMixin, ListView):
    paginate_by = 10
    template_name = 'inventory/requisicion_detail.html'

    def get_context_data(self, **kwargs):
        kwargs['requisicion'] = self.object
        return super(RequisicionDetailView, self).get_context_data(**kwargs)

    def get_queryset(self):
        self.object = self.get_object(Requisicion.objects.all())
        return self.object.items.all()


class RequisicionListView(LoginRequiredMixin, ListView):
    """
    Displays a list of :class:`Requisicion`s
    """
    model = Requisicion
    paginate_by = 10
    ordering = ['-created', ]


class RequisicionCreateView(InventarioFormMixin, CurrentUserFormMixin):
    model = Requisicion
    form_class = RequisicionForm


class RequisicionUpdateView(LoginRequiredMixin, UpdateView):
    model = Requisicion
    form_class = RequisicionCompletarForm


class RequisicionMixin(ContextMixin, View):
    """
    Adds :class:`Requisicion` to the data of a view
    """

    def dispatch(self, *args, **kwargs):
        self.requisicion = get_object_or_404(Requisicion,
                                             pk=kwargs['requisicion'])
        return super(RequisicionMixin, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(RequisicionMixin, self).get_context_data(**kwargs)
        context['requisicion'] = self.requisicion

        return context


class RequisicionFormMixin(FormMixin, RequisicionMixin):
    """
    Add the :class:`Requisicion` to a form used in the view
    """

    def get_initial(self):
        initial = super(RequisicionFormMixin, self).get_initial()
        initial = initial.copy()
        initial['requisicion'] = self.requisicion.id
        return initial


class ItemRequisicionCreateView(LoginRequiredMixin, RequisicionFormMixin,
                                CreateView):
    model = ItemRequisicion
    form_class = ItemRequisicionForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.pendiente = self.object.cantidad
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        extra_form = ItemTemplateForm()
        extra_form.helper.form_action = reverse('itemtemplate-create')
        extra_form.helper.form_id = 'add-item-form'
        kwargs['itemTemplateForm'] = extra_form
        return super(ItemRequisicionCreateView, self).get_context_data(**kwargs)


class ItemRequisicionDeleteView(LoginRequiredMixin, DeleteView):
    model = ItemRequisicion

    def get_object(self, queryset=None):
        obj = super(ItemRequisicionDeleteView, self).get_object(queryset)
        self.requisicion = obj.requisicion
        return obj

    def get_success_url(self):
        return self.requisicion.get_absolute_url()


class TransferenciaCreateView(LoginRequiredMixin, RequisicionFormMixin,
                              CreateView):
    model = Transferencia
    form_class = TransferenciaForm

    def get_initial(self):
        initial = super(TransferenciaCreateView, self).get_initial()
        initial = initial.copy()
        initial['destino'] = self.requisicion.inventario.id
        return initial


class TransferenciaDetailView(CurrentUserFormMixin, SingleObjectMixin,
                              ListView):
    paginate_by = 10
    template_name = 'inventory/transferencia_detail.html'

    def get_context_data(self, **kwargs):
        kwargs['transferencia'] = self.object
        return super(TransferenciaDetailView, self).get_context_data(**kwargs)

    def get_queryset(self):
        self.object = self.get_object(Transferencia.objects.all())
        return self.object.transferidos.all()


class TransferenciaUpdateView(LoginRequiredMixin, UpdateView):
    model = Transferencia
    form_class = TransferirForm
    context_object_name = 'trasferencia'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.transferir()
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


class TransferenciaListView(LoginRequiredMixin, ListView):
    model = Transferencia
    context_object_name = 'transferencias'
    paginate_by = 10


class TransferidoCreateView(LoginRequiredMixin, CreateView):
    model = Transferido
    form_class = TransferidoForm

    def dispatch(self, *args, **kwargs):
        self.transferencia = get_object_or_404(Transferencia,
                                               pk=kwargs['transferencia'])
        return super(TransferidoCreateView, self).dispatch(*args, **kwargs)

    def get_initial(self):
        initial = super(TransferidoCreateView, self).get_initial()
        initial = initial.copy()
        initial['transferencia'] = self.transferencia.id
        return initial


class TransferidoListView(LoginRequiredMixin, ListView):
    model = Transferido
    context_object_name = 'transferidos'
    paginate_by = 10


class ProveedorMixin(ContextMixin, View):
    """Permite obtener un :class:`Proveedor` desde los argumentos en una url"""

    def dispatch(self, *args, **kwargs):
        self.proveedor = get_object_or_404(Proveedor, pk=kwargs['proveedor'])
        return super(ProveedorMixin, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProveedorMixin, self).get_context_data(**kwargs)

        context['proveedor'] = self.proveedor

        return context


class ProveedorFormMixin(FormMixin, ProveedorMixin):
    """
    Permite inicializar el :class:`Proveedor` que se utilizará en un
    formulario
    """

    def get_initial(self):
        initial = super(ProveedorFormMixin, self).get_initial()
        initial = initial.copy()
        initial['proveedor'] = self.proveedor
        return initial


class CompraCreateView(LoginRequiredMixin, InventarioFormMixin, CreateView):
    """
    Creates a :class:`Compra`
    """
    model = Compra
    form_class = CompraForm


class CompraUpdateView(LoginRequiredMixin, UpdateView):
    model = Compra
    form_class = CompraForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        if self.object.ingresada:
            self.object.transferir()
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


class CompraDetailView(LoginRequiredMixin, SingleObjectMixin, ListView):
    paginate_by = 10
    template_name = 'inventory/compra_detail.html'

    def get_context_data(self, **kwargs):
        kwargs['compra'] = self.object
        return super(CompraDetailView, self).get_context_data(**kwargs)

    def get_queryset(self):
        self.object = self.get_object(Compra.objects.all())
        return self.object.items.all()


class CompraMixin(ContextMixin, View):
    """
    Adds a :class:`Compra` to the view
    """

    def dispatch(self, *args, **kwargs):
        self.compra = get_object_or_404(Compra, pk=kwargs['compra'])
        return super(CompraMixin, self).dispatch(*args, **kwargs)


class CompraFormMixin(FormMixin, CompraMixin):
    """
    Adds a :class:`Compra` to the form used in a view
    """

    def get_initial(self):
        initial = super(CompraFormMixin, self).get_initial()
        initial = initial.copy()
        initial['compra'] = self.compra.id
        return initial


class CompraListView(LoginRequiredMixin, ListView):
    model = Compra
    context_object_name = 'compras'


class ItemCompradoCreateView(LoginRequiredMixin, CompraFormMixin):
    model = ItemComprado
    form_class = ItemCompradoForm

    def get_context_data(self, **kwargs):
        extra_form = ItemTemplateForm()
        extra_form.helper.form_action = reverse('itemtemplate-create')
        extra_form.helper.form_id = 'add-item-form'
        kwargs['itemTemplateForm'] = extra_form
        return super(ItemCompradoCreateView, self).get_context_data(**kwargs)


class ItemTemplateSearchView(LoginRequiredMixin, ListView):
    context_object_name = 'items'
    model = ItemTemplate
    paginate_by = 10

    def get_queryset(self):
        form = ItemTemplateSearchForm(self.request.GET)
        form.is_valid()

        query = form.cleaned_data['query']

        queryset = ItemTemplate.objects.filter(
            Q(descripcion__icontains=query)
        )

        return queryset.all()


class HistorialDetailView(LoginRequiredMixin, SingleObjectMixin, ListView):
    paginate_by = 10
    template_name = 'inventory/historial_detail.html'

    def get_context_data(self, **kwargs):
        kwargs['historial'] = self.object
        return super(HistorialDetailView, self).get_context_data(**kwargs)

    def get_queryset(self):
        self.object = self.get_object(Historial.objects.all())
        return self.object.items.all()


class HistorialCreateView(InventarioFormMixin, LoginRequiredMixin):
    model = Historial
    form_class = HistorialForm

    def form_valid(self, form):
        self.object = form.save()

        for item in self.inventario.items.all():
            historico = ItemHistorial()
            historico.item = item.plantilla
            historico.historial = self.object
            historico.cantidad = item.cantidad
            historico.save()

        return HttpResponseRedirect(self.get_success_url())


class ProveedorListView(LoginRequiredMixin, ListView):
    model = Proveedor
    context_object_name = 'proveedores'
    paginate_by = 10
    ordering = ['name']


class ProveedorDetailView(LoginRequiredMixin, DetailView):
    """
    Shows a :class:`Proveedor` data in the UI
    """
    model = Proveedor
    context_object_name = 'proveedor'


class ProveedorCreateView(LoginRequiredMixin, CreateView):
    model = Proveedor
    form_class = ProveedorForm


class ProveedorUpdateView(LoginRequiredMixin, UpdateView):
    model = Proveedor
    form_class = ProveedorForm


class CotizacionCreateView(LoginRequiredMixin, CreateView):
    model = Cotizacion
    form_class = CotizacionForm


class CotizacionDetailView(LoginRequiredMixin, DetailView):
    """
    Displays the information of a :class:`Cotizacion`
    """
    model = Cotizacion
    context_object_name = 'cotizacion'

    def get_context_data(self, **kwargs):

        context = super(CotizacionDetailView, self).get_context_data(**kwargs)

        comprar_form = CotizacionComprarForm()
        context['comprar'] = comprar_form
        comprar_form.helper.form_tag = False

        return context


class CotizacionMixin(ContextMixin, View):
    """Permite obtener un :class:`Cotizacion` desde los argumentos en una url"""

    def dispatch(self, *args, **kwargs):
        self.cotizacion = get_object_or_404(Cotizacion, pk=kwargs['cotizacion'])
        return super(CotizacionMixin, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CotizacionMixin, self).get_context_data(**kwargs)

        context['cotizacion'] = self.cotizacion

        return context


class CotizacionListView(LoginRequiredMixin, ListView):
    """
    Displays a list of :class:`
    """
    model = Cotizacion
    paginate_by = 10


class CotizacionUpdateView(LoginRequiredMixin, UpdateView):
    """
    Allows the user update :class:`Cotizacion` objects
    """
    model = Cotizacion
    form_class = CotizacionForm


class CotizacionAutorizarUpdateView(CotizacionUpdateView):
    """
    Allows the user to mark a :class:`Cotizacion` as authorized
    """
    form_class = CotizacionAutorizarForm


class CotizacionDenegarUpdateView(CotizacionUpdateView):
    """
        Allows the user to mark a :class:`Cotizacion` as denied
        """
    form_class = CotizacionDenegarForm


class CotizacionComprarUpdateView(CotizacionUpdateView):
    """
    Allows the user to create a :class:`Compra` based in a :class:`Cotizacion`
    transfering all the :class:`ItemCotizado` as :class:`ItemComprado`
    """
    form_class = CotizacionComprarForm

    def form_valid(self, form):
        self.object = form.save()

        compra = Compra()
        compra.cotizacion = self.object
        compra.inventario = self.object.inventario
        compra.proveedor = self.object.proveedor

        compra.save()

        for item in self.object.itemcotizado_set.all():
            item_comprado = ItemComprado(
                compra=compra,
                item=item.item,
                precio=item.precio,
                cantidad=item.cantidad,
            )
            item_comprado.save()

        return HttpResponseRedirect(compra.get_absolute_url())


class CotizacionFormMixin(CotizacionMixin, FormMixin):
    """
    Permite inicializar el :class:`Proveedor` que se utilizará en un
    formulario
    """

    def get_initial(self):
        initial = super(CotizacionFormMixin, self).get_initial()
        initial = initial.copy()
        initial['cotizacion'] = self.cotizacion
        return initial


class ItemCotizadoCreateView(LoginRequiredMixin, CotizacionFormMixin,
                             CreateView):
    model = ItemCotizado
    form_class = ItemCotizadoform

    def get_success_url(self):
        return reverse('itemcotizado-create', args=[self.cotizacion.id])


class ItemCotizadoDeleteView(LoginRequiredMixin, DeleteView):
    """
    Removes an :class:`ItemCotizado` from a :class:`Cotizacion`
    """
    model = ItemCotizado

    def get_object(self, queryset=None):
        obj = super(ItemCotizadoDeleteView, self).get_object(queryset)
        self.cotizacion = obj.cotizacion
        return obj

    def get_success_url(self):
        return self.cotizacion.get_absolute_url()


class ItemCotizadoUpdateView(LoginRequiredMixin, UpdateView):
    """
    Changes the values of a :class:`ItemCotizado`
    """
    model = ItemCotizado
    form_class = ItemCotizadoform


class UserInventarioRequiredMixin(View):
    """
    Muestra un mensaje de error si el :class:`User` no tiene un
    :class:`Inventario` asignado en su perfil
    """

    def dispatch(self, *args, **kwargs):
        if self.request.user.profile is None:
            messages.info(self.request,
                          _("Su usuario no tiene un Inventario asociado, por "
                            "favor edite su Perfil para asociar un Inventario"))
        return super(UserInventarioRequiredMixin, self).dispatch(*args,
                                                                 **kwargs)
