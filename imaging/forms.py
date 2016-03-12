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
from __future__ import unicode_literals

from crispy_forms.layout import Fieldset
from django import forms
from django.utils.translation import ugettext_lazy as _

from imaging.models import Examen, Imagen, Adjunto, Dicom, EstudioProgramado, \
    Estudio, TipoExamen
from persona.forms import FieldSetModelFormMixin, FieldSetFormMixin, \
    DateTimeWidget
from persona.models import Persona


class ExamenForm(FieldSetModelFormMixin):
    """Permite mostrar formularios para crear :class:`Examen`es nuevos"""

    class Meta:
        model = Examen
        exclude = ('efectuado', 'usuario', 'pendiente')

    fecha = forms.DateTimeField(widget=DateTimeWidget)

    persona = forms.ModelChoiceField(label="",
                                     queryset=Persona.objects.all(),
                                     widget=forms.HiddenInput(), required=False)

    def __init__(self, *args, **kwargs):
        super(ExamenForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(_('Editar Examen'), *self.field_names)


class ImagenForm(FieldSetModelFormMixin):
    """"Permite mostrar un formulario para agregar una :class:`Imagen`
    a un :class:`Examen`"""

    class Meta:
        model = Imagen
        fields = '__all__'

    examen = forms.ModelChoiceField(label="",
                                    queryset=Examen.objects.all(),
                                    widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super(ImagenForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(_('Adjuntar Imagen'),
                                      *self.field_names)


class AdjuntoForm(FieldSetModelFormMixin):
    """Muestra el formulario para agregar archivos :class:`Adjunto`s a un
    :class:`Examen`"""

    class Meta:
        model = Adjunto
        fields = '__all__'

    examen = forms.ModelChoiceField(label="",
                                    queryset=Examen.objects.all(),
                                    widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super(AdjuntoForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(_('Adjuntar Archivo'),
                                      *self.field_names)


class DicomForm(FieldSetModelFormMixin):
    """Muestra el formulario para agregar un archivo :class:`Dicom` a un
    :class:`Examen`"""

    class Meta:
        model = Dicom
        fields = ('descripcion', 'archivo')

    examen = forms.ModelChoiceField(label="",
                                    queryset=Examen.objects.all(),
                                    widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super(DicomForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(_('Agregar Imagen Dicom'),
                                      *self.field_names)


class EstudioProgramadoForm(FieldSetModelFormMixin):
    """"Permite mostrar los formularios para crear una :class:`Remision`"""

    class Meta:
        model = EstudioProgramado
        exclude = ('efectuado', 'usuario',)

    persona = forms.ModelChoiceField(label="",
                                     queryset=Persona.objects.all(),
                                     widget=forms.HiddenInput(), required=False)

    def __init__(self, *args, **kwargs):
        super(EstudioProgramadoForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(_('Formulario de Estudio Programado'),
                                      *self.field_names)


class EmailForm(FieldSetFormMixin):
    """Permite mostrar un formulario para enviar notificaciones a diversos
    correos"""

    email = forms.CharField()
    examen = forms.ModelChoiceField(label="",
                                    queryset=Examen.objects.all(),
                                    widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super(EmailForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(_('Enviar Correo'), *self.field_names)

    def send_email(self):
        """Realiza el envio del correo electrónico"""

        pass


class EstudioForm(FieldSetModelFormMixin):
    class Meta:
        model = Estudio
        fields = '__all__'

    examen = forms.ModelChoiceField(label="",
                                    queryset=Examen.objects.all(),
                                    widget=forms.HiddenInput())
    tipo_de_examen = forms.ModelChoiceField(
            queryset=TipoExamen.objects.all()
    )

    def __init__(self, *args, **kwargs):
        super(EstudioForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(_('Agregar Examen'), *self.field_names)
