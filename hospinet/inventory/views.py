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
from django.contrib.auth.decorators import permission_required
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.generic import (CreateView, DetailView, UpdateView, ListView,
                                  DeleteView)
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.base import TemplateView
from django.shortcuts import get_object_or_404
from django.http.response import HttpResponseRedirect
from django.core.urlresolvers import reverse

from users.mixins import LoginRequiredMixin, CurrentUserFormMixin
from inventory.models import (Inventario, Item, ItemTemplate, Transferencia,
                              Historial, ItemComprado, Transferido, Compra,
                              ItemType, Requisicion, ItemRequisicion,
                              ItemHistorial, Proveedor)
from inventory.forms import (InventarioForm, ItemTemplateForm, ItemTypeForm,
                             HistorialForm, ItemForm, RequisicionForm,
                             ItemRequisicionForm, TransferenciaForm,
                             TransferidoForm, CompraForm, TransferirForm,
                             ItemTemplateSearchForm, RequisicionCompletarForm,
                             ItemCompradoForm, ProveedorForm)


class InventarioPermissionMixin(LoginRequiredMixin):
    @method_decorator(permission_required('inventory.inventario'))
    def dispatch(self, *args, **kwargs):
        return super(InventarioPermissionMixin, self).dispatch(*args, **kwargs)


class IndexView(TemplateView, InventarioPermissionMixin):
    template_name = 'inventory/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        context['inventarios'] = Inventario.objects.all()
        context['productoform'] = ItemTemplateSearchForm()
        context['productoform'].helper.form_tag = False

        return context


class InventarioFormMixin(CreateView):
    def dispatch(self, *args, **kwargs):
        self.inventario = get_object_or_404(Inventario, pk=kwargs['inventario'])
        return super(InventarioFormMixin, self).dispatch(*args, **kwargs)

    def get_initial(self):
        initial = super(InventarioFormMixin, self).get_initial()
        initial = initial.copy()
        initial['inventario'] = self.inventario.id
        return initial


class ItemTemplateDetailView(DetailView, LoginRequiredMixin):
    model = ItemTemplate
    context_object_name = 'item_template'


class ItemTemplateListView(ListView, LoginRequiredMixin):
    model = ItemTemplate
    context_object_name = 'item_templates'
    paginate_by = 10


class ItemTemplateCreateView(CreateView, LoginRequiredMixin):
    model = ItemTemplate
    form_class = ItemTemplateForm


class ItemTypeCreateView(CreateView, LoginRequiredMixin):
    model = ItemType
    form_class = ItemTypeForm


class ItemTemplateUpdateView(UpdateView, LoginRequiredMixin):
    model = ItemTemplate
    form_class = ItemTemplateForm


class InventarioListView(ListView, LoginRequiredMixin):
    model = Inventario
    context_object_name = 'inventarios'
    paginate_by = 10


class InventarioDetailView(SingleObjectMixin, ListView, LoginRequiredMixin):
    paginate_by = 10
    template_name = 'inventory/inventario_detail.html'

    def get_context_data(self, **kwargs):
        kwargs['inventario'] = self.object
        return super(InventarioDetailView, self).get_context_data(**kwargs)

    def get_queryset(self):
        self.object = self.get_object(Inventario.objects.all())
        return self.object.items.all()


class InventarioMixin(TemplateView):
    def dispatch(self, *args, **kwargs):
        self.inventario = get_object_or_404(Inventario, pk=kwargs['inventario'])
        return super(InventarioMixin, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['inventario'] = self.inventario
        return super(InventarioMixin, self).get_context_data(**kwargs)


class InventarioCreateView(CreateView, LoginRequiredMixin):
    model = Inventario
    form_class = InventarioForm


class ItemListView(ListView, LoginRequiredMixin):
    model = Item
    context_object_name = 'items'
    paginate_by = 10


class ItemInventarioListView(ListView, LoginRequiredMixin):
    model = Item
    context_object_name = 'items'
    paginate_by = 10

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


class ItemDetailView(ListView, LoginRequiredMixin):
    model = Item
    context_object_name = 'item'


class RequisicionDetailView(SingleObjectMixin, ListView, LoginRequiredMixin):
    paginate_by = 10
    template_name = 'inventory/requisicion_detail.html'

    def get_context_data(self, **kwargs):
        kwargs['requisicion'] = self.object
        return super(RequisicionDetailView, self).get_context_data(**kwargs)

    def get_queryset(self):
        self.object = self.get_object(Requisicion.objects.all())
        return self.object.items.all()


class RequisicionListView(ListView, LoginRequiredMixin):
    model = Requisicion
    context_object_name = 'requisiciones'


class RequisicionCreateView(InventarioFormMixin, CurrentUserFormMixin):
    model = Requisicion
    form_class = RequisicionForm


class RequisicionUpdateView(UpdateView, LoginRequiredMixin):
    model = Requisicion
    form_class = RequisicionCompletarForm


class RequisicionFormMixin(CreateView):
    def dispatch(self, *args, **kwargs):
        self.requisicion = get_object_or_404(Requisicion,
                                             pk=kwargs['requisicion'])
        return super(RequisicionFormMixin, self).dispatch(*args, **kwargs)

    def get_initial(self):
        initial = super(RequisicionFormMixin, self).get_initial()
        initial = initial.copy()
        initial['requisicion'] = self.requisicion.id
        return initial

    def get_context_data(self, **kwargs):
        context = super(RequisicionFormMixin, self).get_context_data(**kwargs)
        context['requisicion'] = self.requisicion

        return context


class ItemRequisicionCreateView(RequisicionFormMixin, LoginRequiredMixin):
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


class ItemRequisicionDeleteView(DeleteView, LoginRequiredMixin):
    model = ItemRequisicion

    def get_object(self, queryset=None):
        obj = super(ItemRequisicionDeleteView, self).get_object(queryset)
        self.requisicion = obj.requisicion
        return obj

    def get_success_url(self):
        return self.requisicion.get_absolute_url()


class TransferenciaCreateView(RequisicionFormMixin, LoginRequiredMixin):
    model = Transferencia
    form_class = TransferenciaForm

    def get_initial(self):
        initial = super(TransferenciaCreateView, self).get_initial()
        initial = initial.copy()
        initial['destino'] = self.requisicion.inventario.id
        return initial


class TransferenciaDetailView(SingleObjectMixin, ListView,
                              CurrentUserFormMixin):
    paginate_by = 10
    template_name = 'inventory/transferencia_detail.html'

    def get_context_data(self, **kwargs):
        kwargs['transferencia'] = self.object
        return super(TransferenciaDetailView, self).get_context_data(**kwargs)

    def get_queryset(self):
        self.object = self.get_object(Transferencia.objects.all())
        return self.object.transferidos.all()


class TransferenciaUpdateView(UpdateView):
    model = Transferencia
    form_class = TransferirForm
    context_object_name = 'trasferencia'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.transferir()
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


class TransferenciaListView(ListView, LoginRequiredMixin):
    model = Transferencia
    context_object_name = 'transferencias'
    paginate_by = 10


class TransferidoCreateView(CreateView, LoginRequiredMixin):
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


class TransferidoListView(ListView, LoginRequiredMixin):
    model = Transferido
    context_object_name = 'transferidos'
    paginate_by = 10


class CompraCreateView(InventarioFormMixin, LoginRequiredMixin):
    model = Compra
    form_class = CompraForm


class CompraUpdateView(UpdateView, LoginRequiredMixin):
    model = Compra
    form_class = CompraForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        if self.object.ingresada:
            self.object.transferir()
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


class CompraDetailView(SingleObjectMixin, ListView, LoginRequiredMixin):
    paginate_by = 10
    template_name = 'inventory/compra_detail.html'

    def get_context_data(self, **kwargs):
        kwargs['compra'] = self.object
        return super(CompraDetailView, self).get_context_data(**kwargs)

    def get_queryset(self):
        self.object = self.get_object(Compra.objects.all())
        return self.object.items.all()


class CompraFormMixin(CreateView):
    def dispatch(self, *args, **kwargs):
        self.compra = get_object_or_404(Compra, pk=kwargs['compra'])
        return super(CompraFormMixin, self).dispatch(*args, **kwargs)

    def get_initial(self):
        initial = super(CompraFormMixin, self).get_initial()
        initial = initial.copy()
        initial['compra'] = self.compra.id
        return initial


class CompraListView(ListView, LoginRequiredMixin):
    model = Compra
    context_object_name = 'compras'


class ItemCompradoCreateView(CompraFormMixin, LoginRequiredMixin):
    model = ItemComprado
    form_class = ItemCompradoForm

    def get_context_data(self, **kwargs):
        extra_form = ItemTemplateForm()
        extra_form.helper.form_action = reverse('itemtemplate-create')
        extra_form.helper.form_id = 'add-item-form'
        kwargs['itemTemplateForm'] = extra_form
        return super(ItemCompradoCreateView, self).get_context_data(**kwargs)


class ItemTemplateSearchView(ListView, LoginRequiredMixin):
    context_object_name = 'items'
    model = ItemTemplate
    paginate_by = 10

    def get_queryset(self):
        form = ItemTemplateSearchForm(self.request.GET)

        # if not form.is_valid():
        #    redirect('admision-estadisticas')
        form.is_valid()
        print(form.errors)

        query = form.cleaned_data['query']

        queryset = ItemTemplate.objects.filter(
            Q(descripcion__icontains=query)
        )

        return queryset.all()


class HistorialDetailView(SingleObjectMixin, ListView, LoginRequiredMixin):
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


class ProveedorListView(ListView, LoginRequiredMixin):
    model = Proveedor
    context_object_name = 'proveedores'
    paginate_by = 10


class ProveedorDetailView(SingleObjectMixin, ListView, LoginRequiredMixin):
    paginate_by = 10
    template_name = 'inventory/proveedor_detail.html'

    def get_context_data(self, **kwargs):
        kwargs['inventario'] = self.object
        return super(ProveedorDetailView, self).get_context_data(**kwargs)

    def get_queryset(self):
        self.object = self.get_object(Proveedor.objects.all())
        return self.object.items.all()


class ProveedorCreateView(CreateView, LoginRequiredMixin):
    model = Proveedor
    form_class = ProveedorForm


class ProveedorUpdateView(UpdateView, LoginRequiredMixin):
    model = Proveedor
    form_class = ProveedorForm
