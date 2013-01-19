# -*- coding: utf-8 -*-
from django import forms
from imaging.models import Examen, Imagen, Adjunto, Dicom, EstudioProgramado
from persona.models import Persona
from templated_email import send_templated_mail

class ExamenForm(forms.ModelForm):
    
    """Permite mostrar formularios para crear :class:`Examen`es nuevos"""

    class Meta:
        
        model = Examen
    
    fecha = forms.DateTimeField(widget=forms.DateTimeInput(
                                            attrs={'class': 'datetimepicker' },
                                            format='%d/%m/%Y %H:%M'),
                                input_formats=('%d/%m/%Y %H:%M',),
                                required=False)
    
    persona = forms.ModelChoiceField(label="",
                                  queryset=Persona.objects.all(),
                                  widget=forms.HiddenInput(), required=False)

class ImagenForm(forms.ModelForm):
    
    """"Permite mostrar un formulario para agregar una :class:`Imagen`
    a un :class:`Examen`"""

    class Meta:
        
        model = Imagen
    
    examen = forms.ModelChoiceField(label="",
                                  queryset=Examen.objects.all(),
                                  widget=forms.HiddenInput())

class AdjuntoForm(forms.ModelForm):
    
    """Muestra el formulario para agregar archivos :class:`Adjunto`s a un
    :class:`Examen`"""

    class Meta:
        
        model = Adjunto
    
    examen = forms.ModelChoiceField(label="",
                                  queryset=Examen.objects.all(),
                                  widget=forms.HiddenInput())

class DicomForm(forms.ModelForm):
    
    """Muestra el formulario para agregar un archivo :class:`Dicom` a un
    :class:`Examen`"""

    class Meta:
        
        model = Dicom
        fields = ('descripcion', 'archivo')
    
    examen = forms.ModelChoiceField(label="",
                                  queryset=Examen.objects.all(),
                                  widget=forms.HiddenInput())

class EstudioProgramadoForm(forms.ModelForm):
    
    """"Permite mostrar los formularios para crear una :class:`Remision`"""

    class Meta:
        
        model = EstudioProgramado
        exclude = ('efectuado', 'usuario',)
    
    persona = forms.ModelChoiceField(label="",
                                  queryset=Persona.objects.all(),
                                  widget=forms.HiddenInput(), required=False)

class EmailForm(forms.Form):

    """Permite mostrar un formulario para enviar notificaciones a diversos
    correos"""

    email = forms.CharField()
    examen = forms.ModelChoiceField(label="",
                                  queryset=Examen.objects.all(),
                                  widget=forms.HiddenInput())

    def send_email(self):

        """Realiza el envio del correo electrónico"""

        examen = self.cleaned_data['examen']
        get_templated_mail(
                           template_name='examen',
                           from_email='hospinet@casahospitalaria.com',
                           to=[self.cleaned_data['email']],
                           context={
                                    'examen':examen
                           }
        )
