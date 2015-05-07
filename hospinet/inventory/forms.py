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
from select2.fields import ModelChoiceField

from persona.forms import FieldSetModelFormMixin, FieldSetFormMixin, DateTimeWidget, FutureDateWidget
from inventory.models import (ItemTemplate, Inventario, Item, Compra, ItemType,
                              Requisicion, ItemRequisicion, Transferencia,
                              Transferido, ItemComprado, Historial, Proveedor)
from users.mixins import HiddenUserForm


class ItemTemplateForm(FieldSetModelFormMixin):
    class Meta:
        model = ItemTemplate
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ItemTemplateForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Formulario de Producto',
                                      *self.field_names)


class InventarioForm(FieldSetModelFormMixin):
    class Meta:
        model = Inventario
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(InventarioForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Formulario de Bódega de Inventario',
                                      *self.field_names)


class ItemForm(FieldSetModelFormMixin):
    class Meta:
        model = Item
        fields = ("inventario", "plantilla", "cantidad", 'vencimiento')

    plantilla = ModelChoiceField(name="", model="", label="Item",
                                 queryset=ItemTemplate.objects.filter(
                                     activo=True).order_by('descripcion').all())

    vencimiento = forms.DateTimeField(widget=FutureDateWidget())

    def __init__(self, *args, **kwargs):
        super(ItemForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Formulario de Item Inventariado',
                                      *self.field_names)


class CompraForm(FieldSetModelFormMixin):
    class Meta:
        model = Compra
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CompraForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Formulario de Compra',
                                      *self.field_names)


class ItemTypeForm(FieldSetModelFormMixin):
    class Meta:
        model = ItemType
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ItemTypeForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Formulario de Tipos de Producto',
                                      *self.field_names)


class RequisicionForm(HiddenUserForm):
    class Meta:
        model = Requisicion
        exclude = ('entregada', 'aprobada')

    def __init__(self, *args, **kwargs):
        super(RequisicionForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Formulario de Requisición',
                                      *self.field_names)


class RequisicionCompletarForm(forms.ModelForm):
    class Meta:
        model = Requisicion
        fields = ('entregada',)

    def __init__(self, *args, **kwargs):
        super(RequisicionCompletarForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.html5_required = True
        self.field_names = self.fields.keys()
        self.helper.add_input(Submit('submit', 'Aplicar'))
        self.helper.layout = Fieldset(u'¿Completar la Requisición Ahora?',
                                      *self.field_names)


class ItemRequisicionForm(FieldSetModelFormMixin):
    class Meta:
        model = ItemRequisicion
        exclude = ('entregada', 'pendiente')

    item = ModelChoiceField(name="", model="",
                            queryset=ItemTemplate.objects.filter(
                                activo=True).order_by('descripcion').all())

    def __init__(self, *args, **kwargs):
        super(ItemRequisicionForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Formulario de Requisición de Producto',
                                      *self.field_names)


class TransferenciaForm(HiddenUserForm):
    class Meta:
        model = Transferencia
        exclude = ('aplicada',)

    def __init__(self, *args, **kwargs):
        super(TransferenciaForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(
            u'Formulario de Transferencia de Inventario',
            *self.field_names)


class TransferirForm(FieldSetModelFormMixin):
    class Meta:
        model = Transferencia
        fields = ('aplicada',)
        item = ModelChoiceField(name="", model="",
                                queryset=Requisicion.objects.filter(
                                    entregada=False).all())

    def __init__(self, *args, **kwargs):
        super(TransferirForm, self).__init__(*args, **kwargs)
        self.helper.add_input(Submit('submit', 'Aplicar'))
        self.helper.layout = Fieldset(u'¿Aplicar la Transferencia Ahora?',
                                      *self.field_names)


class TransferidoForm(FieldSetModelFormMixin):
    class Meta:
        model = Transferido
        exclude = ('aplicada',)

    item = ModelChoiceField(name="", model="",
                            queryset=ItemTemplate.objects.filter(
                                activo=True).order_by('descripcion').all())

    def __init__(self, *args, **kwargs):
        super(TransferidoForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Agregar Producto a Transferir',
                                      *self.field_names)


class HistorialForm(FieldSetModelFormMixin):
    class Meta:
        model = Historial
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(HistorialForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Crear Historial de Inventario',
                                      *self.field_names)


class ItemCompradoForm(FieldSetModelFormMixin):
    class Meta:
        model = ItemComprado
        exclude = ('ingresado',)

    item = ModelChoiceField(name="", model="",
                            queryset=ItemTemplate.objects.filter(
                                activo=True).order_by('descripcion').all())

    def __init__(self, *args, **kwargs):
        super(ItemCompradoForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Agregar Producto Comprado',
                                      *self.field_names)


class ItemTemplateSearchForm(FieldSetFormMixin):
    query = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(ItemTemplateSearchForm, self).__init__(*args, **kwargs)
        self.helper.add_input(Submit('submit', 'Buscar'))
        self.helper.layout = Fieldset(u'Buscar Producto', *self.field_names)


class ProveedorForm(FieldSetModelFormMixin):
    class Meta:
        model = Proveedor
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ProveedorForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Formulario de Proveedor',
                                      *self.field_names)
