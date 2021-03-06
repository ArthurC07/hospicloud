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

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Fieldset
from django import forms
from django.utils.translation import ugettext_lazy as _

from inventory.models import ItemTemplate, Inventario, Item, Compra, ItemType, \
    Requisicion, ItemRequisicion, Transferencia, Transferido, ItemComprado, \
    Historial, Proveedor, Cotizacion, ItemCotizado, AnomaliaCompra, \
    AnomaliaTransferencia
from persona.forms import FieldSetModelFormMixin, FieldSetFormMixin, \
    DateTimeWidget, FutureDateWidget
from users.mixins import HiddenUserForm


class ItemTemplateForm(FieldSetModelFormMixin):
    class Meta:
        model = ItemTemplate
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ItemTemplateForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(_('Formulario de Producto'),
                                      *self.field_names)


class ItemTemplateFormMixin(FieldSetModelFormMixin):
    item = forms.ModelChoiceField(
        queryset=ItemTemplate.objects.filter(activo=True).order_by(
            'descripcion')
    )


class InventarioForm(FieldSetModelFormMixin):
    class Meta:
        model = Inventario
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(InventarioForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(_('Formulario de Bódega de Inventario'),
                                      *self.field_names)


class InventarioFormMixin(FieldSetFormMixin):
    inventario = forms.ModelChoiceField(queryset=Inventario.objects.all(),
                                        widget=forms.HiddenInput())


class ItemForm(FieldSetModelFormMixin):
    class Meta:
        model = Item
        fields = ("inventario", "plantilla", "cantidad", 'vencimiento')

    plantilla = forms.ModelChoiceField(label=_("Item"),
                                       queryset=ItemTemplate.objects.filter(
                                           activo=True).order_by(
                                           'descripcion').all())

    vencimiento = forms.DateTimeField(widget=DateTimeWidget())

    def __init__(self, *args, **kwargs):
        super(ItemForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(_('Formulario de Item Inventariado'),
                                      *self.field_names)


class ItemTypeForm(FieldSetModelFormMixin):
    class Meta:
        model = ItemType
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ItemTypeForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(_('Formulario de Tipos de Producto'),
                                      *self.field_names)


class RequisicionForm(HiddenUserForm):
    class Meta:
        model = Requisicion
        exclude = ('entregada', 'aprobada')

    def __init__(self, *args, **kwargs):
        super(RequisicionForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(_('Formulario de Requisición'),
                                      *self.field_names)


class RequisicionDenegarForm(forms.ModelForm):
    """
    Creates a form that marks a :class:`Cotizacion` as authorized
    """

    class Meta:
        model = Cotizacion
        fields = ('denegada',)

    autorizada = forms.BooleanField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        if 'initial' not in kwargs:
            kwargs['initial'] = {'denegada': True}
        else:
            kwargs['initial']['denegada'] = True
        super(RequisicionDenegarForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.html5_required = True
        self.field_names = self.fields.keys()
        self.helper.add_input(
            Submit(
                'submit',
                _('Denegar Requisicion'),
                css_class='btn-success btn-block'
            ))


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
        self.helper.layout = Fieldset(_('¿Completar la Requisición Ahora?'),
                                      *self.field_names)


class RequsicionFormMixin(forms.ModelForm):
    """
    Adds a :class:`HiddenInput` widget for adding a :class:`Requisicion` to a
    form
    """
    requisicion = forms.ModelChoiceField(
        queryset=Requisicion.objects.all(),
        widget=forms.HiddenInput()
    )


class ItemRequisicionForm(ItemTemplateFormMixin, RequsicionFormMixin):
    class Meta:
        model = ItemRequisicion
        exclude = ('entregada', 'pendiente')

    def __init__(self, *args, **kwargs):
        super(ItemRequisicionForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(
            _('Formulario de Requisición de Producto'),
            *self.field_names)


class TransferenciaForm(HiddenUserForm):
    class Meta:
        model = Transferencia
        exclude = ('aplicada',)

    origen = forms.ModelChoiceField(
        queryset=Inventario.objects.filter(activo=True).all()
    )

    destino = forms.ModelChoiceField(
        queryset=Inventario.objects.filter(activo=True).all()
    )

    def __init__(self, *args, **kwargs):
        super(TransferenciaForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(
            _('Formulario de Transferencia de Inventario'),
            *self.field_names)


class TransferirForm(FieldSetModelFormMixin):
    class Meta:
        model = Transferencia
        fields = ('aplicada',)
        item = forms.ModelChoiceField(
            queryset=Requisicion.objects.filter(entregada=False).all()
        )

    def __init__(self, *args, **kwargs):
        super(TransferirForm, self).__init__(*args, **kwargs)
        self.helper.add_input(Submit('submit', 'Aplicar'))
        self.helper.layout = Fieldset(_('¿Aplicar la Transferencia Ahora?'),
                                      *self.field_names)


class TransferenciaFormMixin(FieldSetModelFormMixin):
    """
    Adds a :class:`Transferencia` hidden field to a form.
    """
    transferencia = forms.ModelChoiceField(
        queryset=Transferencia.objects.all(),
        widget=forms.HiddenInput(),
    )


class TransferidoForm(ItemTemplateFormMixin):
    class Meta:
        model = Transferido
        exclude = ('aplicada',)

    def __init__(self, *args, **kwargs):
        super(TransferidoForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(_('Agregar Producto a Transferir'),
                                      *self.field_names)


class TransferidoFormMixin(FieldSetModelFormMixin):
    """
    Adds a :class:`Transferido` hidden field to a form.
    """
    transferido = forms.ModelChoiceField(
        queryset=Transferido.objects.all(),
        widget=forms.HiddenInput(),
    )


class AnomaliaTransferenciaForm(TransferenciaFormMixin, TransferidoFormMixin):
    """
    Builds a form that will be used to create new :class:`AnomaliaTransferencia`
    objects
    """

    class Meta:
        model = AnomaliaTransferencia
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(AnomaliaTransferenciaForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(
            _('Formulario de Anomalia de Transferencia'),
            *self.field_names
        )


class HistorialForm(FieldSetModelFormMixin):
    class Meta:
        model = Historial
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(HistorialForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(_('Crear Historial de Inventario'),
                                      *self.field_names)


class ItemCompradoForm(ItemTemplateFormMixin):
    class Meta:
        model = ItemComprado
        exclude = ('ingresado',)

    compra = forms.ModelChoiceField(
        queryset=Compra.objects.all(),
        widget=forms.HiddenInput(),
    )

    def __init__(self, *args, **kwargs):
        super(ItemCompradoForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(_('Agregar Producto Comprado'),
                                      *self.field_names)


class ItemTemplateSearchForm(FieldSetFormMixin):
    query = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(ItemTemplateSearchForm, self).__init__(*args, **kwargs)
        self.helper.add_input(Submit('submit', _('Buscar')))
        self.helper.layout = Fieldset(_('Buscar Producto'), *self.field_names)


class ProveedorForm(FieldSetModelFormMixin):
    class Meta:
        model = Proveedor
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ProveedorForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(_('Formulario de Proveedor'),
                                      *self.field_names)


class ProveedorFormMixin(FieldSetModelFormMixin):
    proveedor = forms.ModelChoiceField(queryset=Proveedor.objects.all())


class CompraForm(ProveedorFormMixin, HiddenUserForm):
    """
    Describes a form that will be used to create :class:`Compra` objects
    """

    class Meta:
        model = Compra
        exclude = ('ingresada',)

    def __init__(self, *args, **kwargs):
        super(CompraForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(_('Formulario de Compra'),
                                      *self.field_names)


class CompraDocumentosForm(FieldSetModelFormMixin):
    """
    Edits a :class:`Compra` to add missing documents
    """

    class Meta:
        model = Compra
        fields = ('comprobante', 'metodo_de_pago')

    def __init__(self, *args, **kwargs):
        super(CompraDocumentosForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(_('Documentos de Compra'),
                                      *self.field_names)


class CompraIngresarForm(forms.ModelForm):
    """
    Creates a form that marks a :class:`Cotizacion` as denied
    """

    class Meta:
        model = Compra
        fields = ('ingresada', 'inventario')

    ingresada = forms.BooleanField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        if 'initial' not in kwargs:
            kwargs['initial'] = {'ingresada': True}
        else:
            kwargs['initial']['ingresada'] = True
        super(CompraIngresarForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.html5_required = True
        self.field_names = self.fields.keys()
        self.helper.add_input(
            Submit(
                'submit',
                _('Transferir Compra'),
                css_class='btn-success btn-block'
            ))


class AnomaliaCompraForm(FieldSetModelFormMixin):
    """
    Creates a form that allows registering the discrepancies of a
    :class:`Compra` on a certain :class:`ItemComprado`
    """

    class Meta:
        model = AnomaliaCompra
        fields = '__all__'

    item = forms.ModelChoiceField(
        queryset=ItemComprado.objects.select_related('item').all(),
        widget=forms.HiddenInput()
    )

    def __init__(self, *args, **kwargs):
        super(AnomaliaCompraForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(_('Formulario de Anomalias'),
                                      *self.field_names)


class CotizacionForm(HiddenUserForm, ProveedorFormMixin):
    """
    Describres a form that will be used to create :class:`Cotizacion` objects
    """

    class Meta:
        model = Cotizacion
        exclude = ('autorizada', 'denegada', 'comprada')

    vencimiento = forms.DateField(widget=FutureDateWidget())
    inventario = forms.ModelChoiceField(
        queryset=Inventario.objects.filter(
            activo=True,
            puede_comprar=True,
        ).select_related(
            'ciudad',
        )
    )

    def __init__(self, *args, **kwargs):
        super(CotizacionForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(_('Formulario de Cotizacion'),
                                      *self.field_names)


class CotizacionFormMixin(FieldSetModelFormMixin):
    cotizacion = forms.ModelChoiceField(
        queryset=Cotizacion.objects.all(),
        widget=forms.HiddenInput())


class CotizacionAutorizarForm(forms.ModelForm):
    """
    Creates a form that marks a :class:`Cotizacion` as authorized
    """

    class Meta:
        model = Cotizacion
        fields = ('autorizada',)

    autorizada = forms.BooleanField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        if 'initial' not in kwargs:
            kwargs['initial'] = {'autorizada': True}
        else:
            kwargs['initial']['autorizada'] = True
        super(CotizacionAutorizarForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.html5_required = True
        self.field_names = self.fields.keys()
        self.helper.add_input(
            Submit(
                'submit',
                _('Autorizar Compra'),
                css_class='btn-success btn-block'
            ))


class CotizacionDenegarForm(forms.ModelForm):
    """
    Creates a form that marks a :class:`Cotizacion` as denied
    """

    class Meta:
        model = Cotizacion
        fields = ('denegada',)

    denegada = forms.BooleanField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        if 'initial' not in kwargs:
            kwargs['initial'] = {'denegada': True}
        else:
            kwargs['initial']['denegada'] = True
        super(CotizacionDenegarForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.html5_required = True
        self.field_names = self.fields.keys()
        self.helper.add_input(
            Submit(
                'submit',
                _('Denegar Cotización'),
                css_class='btn-danger btn-block'
            ))


class CotizacionComprarForm(forms.ModelForm):
    """
    Creates a form that marks a :class:`Cotizacion` as denied
    """

    class Meta:
        model = Cotizacion
        fields = ('comprada',)

    comprada = forms.BooleanField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        if 'initial' not in kwargs:
            kwargs['initial'] = {'comprada': True}
        else:
            kwargs['initial']['comprada'] = True
        super(CotizacionComprarForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.html5_required = True
        self.field_names = self.fields.keys()
        self.helper.add_input(
            Submit(
                'submit',
                _('Efectuar compra'),
                css_class='btn-success btn-block'
            ))


class ItemCotizadoform(CotizacionFormMixin, ItemTemplateFormMixin):
    class Meta:
        model = ItemCotizado
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ItemCotizadoform, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(_('Formulario de Item Cotizado'),
                                      *self.field_names)
