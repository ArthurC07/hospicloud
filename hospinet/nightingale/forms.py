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
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Fieldset
from select2.fields import ModelChoiceField
from django.utils import timezone

from spital.models import Admision
from nightingale.models import (Cargo, Evolucion, Glicemia, Insulina, Dosis,
                                Glucosuria, Ingesta, Excreta, NotaEnfermeria,
                                OrdenMedica, SignoVital, Medicamento,
                                Devolucion, Sumario, OxigenoTerapia, Honorario)
from persona.forms import DateTimeWidget, FieldSetModelFormMixin
from inventory.models import ItemTemplate
from users.mixins import HiddenUserForm


class AdmisionBaseForm(HiddenUserForm):
    admision = forms.ModelChoiceField(label="",
                                      queryset=Admision.objects.all(),
                                      widget=forms.HiddenInput(),
                                      required=False)


class BaseForm(FieldSetModelFormMixin):
    """Formulario base para los distintos ingresos de información de parte de
    los diversos modelos de enfermeria"""

    fecha_y_hora = forms.DateTimeField(widget=DateTimeWidget(), required=False)

    admision = forms.ModelChoiceField(label="",
                                      queryset=Admision.objects.all(),
                                      widget=forms.HiddenInput(),
                                      required=False)

    usuario = forms.ModelChoiceField(label="",
                                     queryset=User.objects.all(),
                                     widget=forms.HiddenInput(), required=False)


class CargoForm(AdmisionBaseForm):
    """Muestra un formulario que permite agregar :class:`Cargo`s a una
    :class:`Persona` durante una :class:`Admision`"""

    class Meta:
        model = Cargo
        exclude = ('facturada', )

    cargo = ModelChoiceField(
        queryset=ItemTemplate.objects.filter(activo=True).order_by(
            'descripcion').all(), name="nombre", model="")
    inicio = forms.DateTimeField(widget=DateTimeWidget(), required=False,
                                 initial=timezone.now)
    fin = forms.DateTimeField(widget=DateTimeWidget(), required=False,
                              initial=timezone.now)

    def __init__(self, *args, **kwargs):
        super(CargoForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Agregar Cargo', *self.field_names)


class PreCargoForm(AdmisionBaseForm):
    """Muestra un formulario que permite agregar :class:`Cargo`s a una
    :class:`Persona` durante una :class:`Admision`"""

    class Meta:
        model = Cargo
        exclude = ('facturada', )

    cargo = forms.ModelChoiceField(label="",
                                   queryset=ItemTemplate.objects.filter(
                                       activo=True).order_by(
                                       'descripcion').all(),
                                   widget=forms.HiddenInput(), required=False)
    inicio = forms.DateTimeField(widget=DateTimeWidget(), required=False,
                                 initial=timezone.now)
    fin = forms.DateTimeField(widget=DateTimeWidget(), required=False,
                              initial=timezone.now)

    def __init__(self, *args, **kwargs):
        super(PreCargoForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Agregar Cargo', *self.field_names)


class SumarioForm(AdmisionBaseForm):
    """Muestra un formulario que permite agregar :class:`Cargo`s a una
    :class:`Persona` durante una :class:`Admision`"""

    fecha = forms.DateTimeField(widget=DateTimeWidget(), required=False,
                                initial=timezone.now)

    class Meta:
        model = Sumario
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(SumarioForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Ingresar Sumario Médico',
                                      *self.field_names)


class EvolucionForm(BaseForm):
    """Muestra un formulario que permite agregar :class:`Evolucion`es a una
    :class:`Persona` durante una :class:`Admision`"""

    class Meta:
        model = Evolucion
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(EvolucionForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Registrar Evolución', *self.field_names)


class GlicemiaForm(BaseForm):
    """Muestra un formulario que permite agregar una lectura de
    :class:`Glicemia` a una :class:`Persona` durante una :class:`Admision`"""

    class Meta:
        model = Glicemia
        fields = '__all__'

    control = forms.CharField(widget=forms.TextInput)

    def __init__(self, *args, **kwargs):
        super(GlicemiaForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Registrar Glicemia', *self.field_names)


class InsulinaForm(BaseForm):
    """Muestra un formulario que permite registrar una administración de
    :class:`Insulina` a una :class:`Persona` durante una :class:`Admision`"""

    class Meta:
        model = Insulina
        fields = '__all__'

    control = forms.CharField(widget=forms.TextInput)

    def __init__(self, *args, **kwargs):
        super(InsulinaForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Registrar Administración de Insulina',
                                      *self.field_names)


class GlucosuriaForm(BaseForm):
    """Muestra un formulario que permite registrar :class:`Glucosuria`s a una
    :class:`Persona` durante una :class:`Admision`"""

    class Meta:
        model = Glucosuria
        fields = '__all__'

    control = forms.CharField(widget=forms.TextInput)

    def __init__(self, *args, **kwargs):
        super(GlucosuriaForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Registrar Administración de Insulina',
                                      *self.field_names)


class IngestaForm(BaseForm):
    """Muestra un formulario que permite registrar :class:`Ingesta`s a una
    :class:`Persona` durante una :class:`Admision`"""

    class Meta:
        model = Ingesta
        exclude = ("usuario",)

    def __init__(self, *args, **kwargs):
        super(IngestaForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Registrar Ingesta', *self.field_names)


class ExcretaForm(BaseForm):
    """Muestra un formulario que permite agregar :class:`Excreta`s a una
    :class:`Persona` durante una :class:`Admision`"""

    class Meta:
        model = Excreta
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ExcretaForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Registrar Excreta', *self.field_names)


class NotaEnfermeriaForm(BaseForm):
    """Muestra un formulario que permite agregar :class:`Cargo`s a una
    :class:`Persona` durante una :class:`Admision`"""

    class Meta:
        model = NotaEnfermeria
        exclude = ('cerrada',)

    nota = forms.CharField(widget=forms.Textarea(attrs={'class': 'big'}))
    admision = forms.ModelChoiceField(label="",
                                      queryset=Admision.objects.all(),
                                      widget=forms.HiddenInput(),
                                      required=False)


    def __init__(self, *args, **kwargs):
        super(NotaEnfermeriaForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Agregar Nota Enfermeria',
                                      *self.field_names)


class OrdenMedicaForm(BaseForm):
    """Muestra un formulario que permite agregar :class:`OrdenMedica`s a una
    :class:`Persona` durante una :class:`Admision`"""

    class Meta:
        model = OrdenMedica
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(OrdenMedicaForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Agregar Orden Médica',
                                      *self.field_names)


class SignoVitalForm(BaseForm):
    """Muestra un formulario que permite registrar lectura de
    :class:`SignoVital`es a una :class:`Persona` durante una
    :class:`Admision`"""

    class Meta:
        model = SignoVital
        exclude = ("presion_arterial_media", )

    def __init__(self, *args, **kwargs):
        super(SignoVitalForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Registrar Signos Vitales',
                                      *self.field_names)


class MedicamentoForm(AdmisionBaseForm):
    """Permite Agregar o modificar los datos de un :class:`Medicamento`"""

    class Meta:
        model = Medicamento
        exclude = ('proxima_dosis', 'suministrado')

    inicio = forms.DateTimeField(widget=DateTimeWidget(), required=False)
    cargo = ModelChoiceField(name='cargo', model='',
                             queryset=ItemTemplate.objects.filter(
                                 activo=True).order_by('descripcion').all())

    admision = forms.ModelChoiceField(label="",
                                      queryset=Admision.objects.all(),
                                      widget=forms.HiddenInput(),
                                      required=False)

    usuario = forms.ModelChoiceField(label="",
                                     queryset=User.objects.all(),
                                     widget=forms.HiddenInput(), required=False)

    def __init__(self, *args, **kwargs):
        super(MedicamentoForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Recetar Medicamento', *self.field_names)


class DosificarForm(forms.Form):
    """Permite indicar el momento en el que se efectua la dosificación de un
    :class:`Medicamento`"""

    hora = forms.DateTimeField(widget=DateTimeWidget(), required=False)

    def __init__(self, *args, **kwargs):
        super(DosificarForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.html5_required = True
        self.field_names = self.fields.keys()
        self.helper.layout = Fieldset(u'Dosificar Medicamento',
                                      *self.field_names)
        self.helper.add_input(Submit('submit', 'Guardar'))


class DosisForm(FieldSetModelFormMixin):
    class Meta:
        model = Dosis
        fields = '__all__'

    fecha_y_hora = forms.DateTimeField(widget=DateTimeWidget(), required=False)

    medicamento = forms.ModelChoiceField(label="",
                                         queryset=Medicamento.objects.all(),
                                         widget=forms.HiddenInput(),
                                         required=False)

    usuario = forms.ModelChoiceField(label="",
                                     queryset=User.objects.all(),
                                     widget=forms.HiddenInput(), required=False)

    administrador = forms.ModelChoiceField(label="",
                                           queryset=User.objects.all(),
                                           widget=forms.HiddenInput(),
                                           required=False)

    def __init__(self, *args, **kwargs):
        super(DosisForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Registrar Dosis de Medicamento',
                                      *self.field_names)


class DevolucionForm(FieldSetModelFormMixin):
    """Permite editar los datos de una :class:`Devolucion`"""

    class Meta:
        model = Devolucion
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(DevolucionForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Efectuar Devolución', *self.field_names)


class MedicamentoUpdateForm(FieldSetModelFormMixin):
    """Permite editar los datos de una :class:`Devolucion`"""

    class Meta:
        model = Medicamento
        fields = ('repeticiones', 'unidades', 'intervalo')

    def __init__(self, *args, **kwargs):
        super(MedicamentoUpdateForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Actualizar Posología de Medicamento',
                                      *self.field_names)


class OxigenoTerapiaForm(FieldSetModelFormMixin):
    """Permite agregar y editar :class:`OxigenoTerapia`s"""

    class Meta:
        model = OxigenoTerapia
        fields = '__all__'

    admision = forms.ModelChoiceField(label="",
                                      queryset=Admision.objects.all(),
                                      widget=forms.HiddenInput(),
                                      required=False)

    usuario = forms.ModelChoiceField(label="",
                                     queryset=User.objects.all(),
                                     widget=forms.HiddenInput(), required=False)

    inicio = forms.DateTimeField(widget=DateTimeWidget(), required=False,
                                 initial=timezone.now)
    fin = forms.DateTimeField(widget=DateTimeWidget(), required=False,
                              initial=timezone.now)

    cargo = ModelChoiceField(name="", model="",
                             queryset=ItemTemplate.objects.filter(
                                 activo=True).order_by('descripcion').all())

    def __init__(self, *args, **kwargs):
        super(OxigenoTerapiaForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Oxigeno Terapia', *self.field_names)


class HonorarioForm(AdmisionBaseForm):
    class Meta:
        model = Honorario
        fields = '__all__'

    item = ModelChoiceField(name="", model="",
                            queryset=ItemTemplate.objects.filter(
                                activo=True).order_by('descripcion').all())

    def __init__(self, *args, **kwargs):
        super(HonorarioForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Agregar Honorarios', *self.field_names)
