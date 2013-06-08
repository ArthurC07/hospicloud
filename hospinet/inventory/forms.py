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

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Fieldset
from inventory.models import ItemTemplate, Inventario, Item, Compra, ItemType

class FieldSetFormMixin(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):

        super(FieldSetFormMixin, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.html5_required = True
        self.field_names = self.fields.keys()
        self.helper.add_input(Submit('submit', 'Guardar'))

class ItemTemplateForm(FieldSetFormMixin):
    
    class Meta:
        
        model = ItemTemplate
    
    def __init__(self, *args, **kwargs):
        
        super(ItemTemplateForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Formulario de Producto',
                                      *self.field_names)

class InventarioForm(FieldSetFormMixin):
    
    class Meta:
        
        model = Inventario
    
    def __init__(self, *args, **kwargs):
        
        super(InventarioForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Formulario de Bódega de Inventario',
                                      *self.field_names)

class ItemForm(FieldSetFormMixin):
    
    class Meta:
        
        model = Item
    
    def __init__(self, *args, **kwargs):
        
        super(ItemForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Formulario de Item Inventariado',
                                      *self.field_names)

class CompraForm(FieldSetFormMixin):
    
    class Meta:
        
        model = Compra
    
    def __init__(self, *args, **kwargs):
        
        super(ItemForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Formulario de Compra',
                                      *self.field_names)

class ItemTypeForm(FieldSetFormMixin):
    
    class Meta:
        
        model = ItemType
    
    def __init__(self, *args, **kwargs):
        
        super(ItemTypeForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Formulario de Tipos de Producto',
                                      *self.field_names)
