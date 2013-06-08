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

from django.views.generic import (CreateView, DetailView, UpdateView, ListView)
from users.mixins import LoginRequiredMixin
from inventory.models import (Inventario, Item, ItemTemplate, Transferencia,
    Transferido, Compra, ItemType)
from django.views.generic.detail import SingleObjectMixin
from inventory.forms import (InventarioForm, ItemTemplateForm, ItemTypeForm)
from django.views.generic.base import TemplateView

class IndexView(TemplateView, LoginRequiredMixin):
    
    template_name = 'inventory/index.html'
    
    def get_context_data(self, **kwargs):
        
        context = super(IndexView, self).get_context_data(**kwargs)
        
        context['inventarios'] = Inventario.objects.all()
        
        return context

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

class InventarioCreateView(CreateView, LoginRequiredMixin):
    
    model = Inventario
    form_class = InventarioForm

class ItemListView(ListView, LoginRequiredMixin):
    
    model = Item
    context_object_name = 'items'
    paginate_by = 10

class ItemDetailView(ListView, LoginRequiredMixin):
    
    model = Item
    context_object_name = 'item'

class TransferenciaDetailView(SingleObjectMixin, ListView, LoginRequiredMixin):
    
    paginate_by = 10
    template_name = 'inventory/transferencia_detail.html'
    
    def get_context_data(self, **kwargs):
        
        kwargs['transferencia'] = self.object
        return super(TransferenciaDetailView, self).get_context_data(**kwargs)
    
    def get_queryset(self):
        
        self.object = self.get_object(Transferencia.objects.all())
        return self.object.transferidos.all()

class TransferenciaListView(ListView, LoginRequiredMixin):
    
    model = Transferencia
    context_object_name = 'transferencias'
    paginate_by = 10

class TransferidoListView(ListView, LoginRequiredMixin):
    
    model = Transferido
    context_object_name = 'transferidos'
    paginate_by = 10

class CompraDetailView(SingleObjectMixin, ListView, LoginRequiredMixin):
    
    paginate_by = 10
    template_name = 'inventory/compra_detail.html'
    
    def get_context_data(self, **kwargs):
        
        kwargs['compra'] = self.object
        return super(CompraDetailView, self).get_context_data(**kwargs)
    
    def get_queryset(self):
        
        self.object = self.get_object(Transferencia.objects.all())
        return self.object.transferidos.all()

class CompraListView(ListView, LoginRequiredMixin):
    
    model = Compra
    context_object_name = 'compras'
