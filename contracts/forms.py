# !/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2011-2014 Carlos Flores <cafg10@gmail.com>
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

from crispy_forms.layout import Fieldset, Submit
from django import forms
from django.utils import timezone
from select2.fields import ModelChoiceField

from contracts.models import (Plan, Contrato, TipoEvento, Evento, Pago,
                              Vendedor, Beneficiario, LimiteEvento, Meta,
                              Cancelacion, Precontrato, Beneficio,
                              MasterContract, ImportFile, PCD, Aseguradora)
from inventory.models import ItemTemplate
from invoice.forms import PeriodoForm
from persona.forms import (FieldSetModelFormMixin, DateTimeWidget,
                           FieldSetFormMixin, FieldSetModelFormMixinNoButton,
                           FutureDateWidget, BasePersonaForm)
from persona.models import Persona, Empleador


class PersonaForm(FieldSetModelFormMixinNoButton):
    class Meta:
        model = Persona
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(PersonaForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Datos del Titular', *self.field_names)


class PersonaPrecontratoForm(FieldSetModelFormMixin):
    class Meta:
        model = Persona
        fields = ('nombre', 'apellido', 'identificacion', 'sexo', 'celular',)

    def __init__(self, *args, **kwargs):
        super(PersonaPrecontratoForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Datos del Titular', *self.field_names)
        self.helper.form_tag = False


class PlanForm(FieldSetModelFormMixin):
    class Meta:
        model = Plan
        fields = '__all__'

    item = ModelChoiceField(name="", model="",
                            queryset=ItemTemplate.objects.filter(
                                activo=True).order_by('descripcion').all())

    def __init__(self, *args, **kwargs):
        super(PlanForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Formulario de Plan', *self.field_names)


class ContratoForm(BasePersonaForm):
    class Meta:
        model = Contrato
        exclude = ('cancelado',)

    vencimiento = forms.DateField(widget=FutureDateWidget)
    ultimo_pago = forms.DateTimeField(widget=DateTimeWidget(), required=False,
                                      initial=timezone.now)
    inicio = forms.DateField(widget=FutureDateWidget())

    def __init__(self, *args, **kwargs):
        super(ContratoForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Formulario de Contrato',
                                      *self.field_names)


class ContratoMasterForm(FieldSetFormMixin):
    persona = forms.ModelChoiceField(label="",
                                     queryset=Persona.objects.all(),
                                     widget=forms.HiddenInput())
    vencimiento = forms.DateField(widget=FutureDateWidget)
    certificado = forms.IntegerField()
    numero = forms.IntegerField()
    master = forms.ModelChoiceField(MasterContract.objects.all())

    def __init__(self, *args, **kwargs):
        del kwargs['instance']
        super(ContratoMasterForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Formulario de Contrato',
                                      *self.field_names)
        self.helper.add_input(Submit('submit', u'Guardar'))


class ContratoEmpresarialForm(FieldSetModelFormMixin):
    class Meta:
        model = Contrato
        exclude = ('cancelado',)

    vencimiento = forms.DateField(widget=FutureDateWidget)
    ultimo_pago = forms.DateTimeField(widget=DateTimeWidget(), required=False,
                                      initial=timezone.now)
    inicio = forms.DateField(widget=FutureDateWidget())

    def __init__(self, *args, **kwargs):
        super(ContratoEmpresarialForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Formulario de Contrato',
                                      *self.field_names)


class TipoEventoForm(FieldSetModelFormMixin):
    class Meta:
        model = TipoEvento
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(TipoEventoForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Formulario de Tipo de Evento',
                                      *self.field_names)


class ContratoMixin(FieldSetModelFormMixin):
    contrato = forms.ModelChoiceField(label="",
                                      queryset=Contrato.objects.all(),
                                      widget=forms.HiddenInput(),
                                      required=False)


class EventoForm(ContratoMixin):
    class Meta:
        model = Evento
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(EventoForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Formulario de Evento',
                                      *self.field_names)


class PagoForm(ContratoMixin):
    class Meta:
        model = Pago
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(PagoForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Formulario de Registro de Pago',
                                      *self.field_names)


class VendedorForm(FieldSetModelFormMixin):
    class Meta:
        model = Vendedor
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(VendedorForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Formulario de Vendedor',
                                      *self.field_names)


class VendedorChoiceForm(FieldSetFormMixin):
    vendedor = forms.ModelChoiceField(queryset=Vendedor.objects.all())

    def __init__(self, *args, **kwargs):
        super(VendedorChoiceForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Buscar Vendedor', *self.field_names)
        self.helper.add_input(Submit('submit', u'Buscar'))


class VendedorPeriodoForm(PeriodoForm):
    vendedor = forms.ModelChoiceField(queryset=Vendedor.objects.all())

    def __init__(self, *args, **kwargs):
        super(VendedorPeriodoForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Por Vendedor y Periodo',
                                      *self.field_names)


class ContratoSearchForm(FieldSetFormMixin):
    numero = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        super(ContratoSearchForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Buscar Contrato', *self.field_names)
        self.helper.add_input(Submit('submit', u'Buscar'))


class BeneficiarioForm(ContratoMixin):
    class Meta:
        model = Beneficiario
        fields = '__all__'

    inscripcion = forms.DateTimeField(widget=DateTimeWidget(), required=False,
                                      initial=timezone.now)

    def __init__(self, *args, **kwargs):
        super(BeneficiarioForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Formulario de Registro de Beneficiario',
                                      *self.field_names)


class BeneficiarioPersonaForm(BasePersonaForm):
    class Meta:
        model = Beneficiario
        exclude = ('activo', 'dependiente',)

    contrato = ModelChoiceField(
        queryset=Contrato.objects.all(),
        name="nombre", model="")
    inscripcion = forms.DateTimeField(widget=DateTimeWidget(), required=False,
                                      initial=timezone.now)

    def __init__(self, *args, **kwargs):
        super(BeneficiarioPersonaForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Formulario de Registro de Beneficiario',
                                      *self.field_names)


class PlanFormMixin(FieldSetModelFormMixin):
    plan = forms.ModelChoiceField(label="", queryset=Plan.objects.all(),
                                  widget=forms.HiddenInput(),
                                  required=False)


class LimiteEventoForm(PlanFormMixin):
    class Meta:
        model = LimiteEvento
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(LimiteEventoForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Agregar Limite de Evento',
                                      *self.field_names)


class BeneficioForm(PlanFormMixin):
    class Meta:
        model = Beneficio
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(BeneficioForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Agregar un Beneficio',
                                      *self.field_names)


class PlanChoiceForm(FieldSetFormMixin):
    plan = forms.ModelChoiceField(queryset=Plan.objects.all())

    def __init__(self, *args, **kwargs):
        super(PlanChoiceForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Buscar Contrato por Nombre',
                                      *self.field_names)
        self.helper.add_input(Submit('submit', u'Buscar'))


class EmpleadorChoiceForm(FieldSetFormMixin):
    empresa = forms.ModelChoiceField(queryset=Empleador.objects.all())

    def __init__(self, *args, **kwargs):
        super(EmpleadorChoiceForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Buscar Contratos Empresariales',
                                      *self.field_names)
        self.helper.add_input(Submit('submit', u'Buscar'))


class MasterContractForm(FieldSetModelFormMixin):
    class Meta:
        model = MasterContract
        exclude = ('processed',)

    item = ModelChoiceField(name="", model="",
                            queryset=ItemTemplate.objects.filter(
                                activo=True).order_by('descripcion').all())

    def __init__(self, *args, **kwargs):
        super(MasterContractForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Crear un Contrato Maestro',
                                      *self.field_names)


class MetaForm(FieldSetModelFormMixin):
    class Meta:
        model = Meta
        fields = '__all__'

    fecha = forms.DateField(widget=FutureDateWidget(), required=False,
                            initial=timezone.now().date())

    def __init__(self, *args, **kwargs):
        super(MetaForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Formulario de Meta', *self.field_names)


class CancelacionForm(ContratoMixin):
    class Meta:
        model = Cancelacion
        fields = '__all__'

    fecha = forms.DateField(widget=FutureDateWidget(), required=False,
                            initial=timezone.now().date())

    def __init__(self, *args, **kwargs):
        super(CancelacionForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Cancelar Contrato', *self.field_names)


class PrecontratoForm(FieldSetModelFormMixin):
    class Meta:
        model = Precontrato
        fields = ('metodo_de_pago', 'de_acuerdo', 'plan')

    def __init__(self, *args, **kwargs):
        super(PrecontratoForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Preaprobar Contrato de Servicios',
                                      *self.field_names)
        self.helper.form_tag = False


class ImportFileForm(FieldSetModelFormMixin):
    class Meta:
        model = ImportFile
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ImportFileForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Agregar Archivo', *self.field_names)


class PCDForm(BasePersonaForm):
    class Meta:
        model = PCD
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(PCDForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Formulario de PCD', *self.field_names)


class AseguradoraForm(FieldSetModelFormMixin):
    class Meta:
        model = Aseguradora
        fields = '__all__'

    representante = ModelChoiceField(
        queryset=Persona.objects.filter(mostrar_en_cardex=True).all(),
        name="representante", model="")
    cardex = ModelChoiceField(
        queryset=Persona.objects.filter(mostrar_en_cardex=True).all(),
        name="representante", model="")

    def __init__(self, *args, **kwargs):
        super(AseguradoraForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Formulario de Aseguradora',
                                      *self.field_names)
