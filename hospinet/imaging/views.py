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
from guardian.decorators import permission_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import (DetailView, UpdateView, CreateView, ListView,
                                  TemplateView, RedirectView, FormView)
from django.contrib import messages
from templated_email import send_templated_mail

from imaging.forms import (ExamenForm, ImagenForm, AdjuntoForm, DicomForm,
                           EstudioProgramadoForm, EmailForm, EstudioForm)
from imaging.models import (Examen, Imagen, Adjunto, Dicom, EstudioProgramado,
                            Estudio)
from persona.forms import PersonaForm, PersonaSearchForm
from persona.models import Persona
from persona.views import PersonaCreateView
from users.mixins import LoginRequiredMixin


class ExamenPermissionMixin(LoginRequiredMixin):
    @method_decorator(permission_required('imaging.examen'))
    def dispatch(self, *args, **kwargs):
        return super(ExamenPermissionMixin, self).dispatch(*args, **kwargs)


class ExamenIndexView(ListView, ExamenPermissionMixin):
    """Muestra un listado de los ultimos 20 :class:`Examen`es que se han
    ingresado al sistema"""

    template_name = 'examen/index.html'
    context_object_name = 'examenes'
    paginate_by = 20

    def get_queryset(self):
        return Examen.objects.all().order_by('-fecha')

    def get_context_data(self, **kwargs):
        """Agrega los ultimos :class:`Examen`es efectuados a la vista"""

        context = super(ExamenIndexView, self).get_context_data(**kwargs)
        context['estudios_programados'] = EstudioProgramado.objects.filter(
            efectuado=False)
        return context


class PersonaExamenCreateView(PersonaCreateView):
    """Permite agregar una :class:`Persona` para efectuarle un
    :class:`Examen`"""

    template_name = 'persona/nuevo.html'

    def get_success_url(self):
        return reverse('examen-agregar', args=[self.object.id])


class ExamenPreCreateView(TemplateView):
    """Permite mostrar una interfaz donde decidir si agregar una nueva
    :class:`Persona` o agregar el :class:`Examen a una ya ingresada previamente
    """

    template_name = 'examen/examen_agregar.html'

    def get_context_data(self, **kwargs):
        context = super(ExamenPreCreateView, self).get_context_data()
        context['persona_form'] = PersonaForm()
        return context


class ExamenDetailView(DetailView, LoginRequiredMixin):
    """Permite ver los detalles de un :class:`Examen`"""

    context_object_name = 'examen'
    model = Examen
    template_name = 'examen/examen_detail.html'
    slug_field = 'uuid'


class ExamenPersonaListView(DetailView, LoginRequiredMixin):
    """Muestra los :class:`Examen`es realizados a una :class:`Persona`"""

    context_object_name = 'persona'
    model = Persona
    template_name = 'examen/examen_paciente_detail.html'


class ExamenUpdateView(UpdateView, LoginRequiredMixin):
    """Permite actualizar los datos de un :class:`Examen`"""

    model = Examen
    form_class = ExamenForm
    template_name = 'examen/examen_update.html'


class ExamenCreateView(CreateView, LoginRequiredMixin):
    """Permite crear un :class:`Examen` a una :class:`Persona`"""

    model = Examen
    form_class = ExamenForm
    template_name = 'examen/examen_create.html'

    def get_form_kwargs(self):
        kwargs = super(ExamenCreateView, self).get_form_kwargs()
        kwargs.update({'initial': {'persona': self.persona.id}})
        return kwargs

    def dispatch(self, *args, **kwargs):
        self.persona = get_object_or_404(Persona, pk=kwargs['persona'])
        return super(ExamenCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super(ExamenCreateView, self).form_valid(form)


class ExamenFormMixin(CreateView, LoginRequiredMixin):
    def dispatch(self, *args, **kwargs):
        self.examen = get_object_or_404(Examen, pk=kwargs['examen'])
        return super(ExamenFormMixin, self).dispatch(*args, **kwargs)

    def get_initial(self):
        initial = super(ExamenFormMixin, self).get_initial()
        initial = initial.copy()
        initial['examen'] = self.examen.id
        return initial


class ExamenDocBaseCreateView(CreateView, LoginRequiredMixin):
    """Permite crear objetos que pertenecen a un :class:`Examen`"""

    def dispatch(self, *args, **kwargs):
        self.examen = get_object_or_404(Examen, pk=kwargs['examen'])
        return super(ExamenDocBaseCreateView, self).dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        """Busca el :class:`Examen` correspondiente y lo agrega a los
        argumentos del formulario"""

        kwargs = super(ExamenDocBaseCreateView, self).get_form_kwargs()
        kwargs.update({'initial': {'examen': self.examen.id}})
        return kwargs

    def form_valid(self, form):
        """Agrega el :class:`Examen` al objeto"""

        self.object = form.save(commit=False)
        self.object.examen = self.examen
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


class ImagenCreateView(ExamenDocBaseCreateView):
    """Permite crear :class:`Imagen`es a un :class:`Examen`"""

    model = Imagen
    form_class = ImagenForm
    template_name = "examen/imagen_create.html"


class AdjuntoCreateView(ExamenDocBaseCreateView):
    """Permite crear :class:`Adjunto`s a un :class:`Examen`"""

    model = Adjunto
    form_class = AdjuntoForm
    template_name = "examen/adjunto_create.html"


class DicomCreateView(ExamenDocBaseCreateView):
    """Permite agregar un archivo :class:`Dicom` a un examen"""

    model = Dicom
    form_class = DicomForm
    template_name = "examen/dicom_create.html"

    def form_valid(self, form):
        """Agrega y extrae la imagen del archivo DICOM"""

        self.object = form.save(commit=False)
        self.object.examen = self.examen
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


class DicomDetailView(DetailView, LoginRequiredMixin):
    """Muestra el visor DICOM básico en el navegador del usuario"""

    context_object_name = 'dicom'
    model = Dicom
    template_name = "examen/dicom_detail.html"
    slug_field = 'uuid'


class NotificarExamenView(FormView, LoginRequiredMixin):
    """Notifica a los interesados de que el :class:`Examen` se encuentra
    disponible"""

    template_name = 'examen/email.html'
    form_class = EmailForm

    def get_form_kwargs(self):
        kwargs = super(NotificarExamenView, self).get_form_kwargs()
        kwargs.update({'initial': {'examen': self.examen.id}})
        return kwargs

    def dispatch(self, *args, **kwargs):
        """Obtiene el examen que se va a enviar"""

        self.examen = get_object_or_404(Examen, pk=kwargs['pk'])
        return super(NotificarExamenView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        """Efectua el envio de correos utilizando el de envio del formulario"""

        examen = form.cleaned_data['examen']
        context = {'link_examen': self.request.build_absolute_uri(
            examen.get_absolute_url())}
        send_templated_mail(
            template_name='examen',
            from_email='hospinet@casahospitalaria.com',
            recipient_list=[form.cleaned_data['email']],
            context=context
        )

        return super(NotificarExamenView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        """Agrega los ultimos :class:`Examen`es efectuados a la vista"""

        context = super(NotificarExamenView, self).get_context_data(**kwargs)
        context['examen'] = self.examen
        return context

    def get_success_url(self):
        return self.examen.get_absolute_url()


class PersonaEstudioCreateView(PersonaCreateView):
    """Permite agregar una :class:`Persona` para efectuarle un
    :class:`Examen`"""

    template_name = 'persona/nuevo.html'

    def get_success_url(self):
        return reverse('examen-programar', args=[self.object.id])


class EstudioProgramadoDetailView(DetailView, LoginRequiredMixin):
    """Muestra las acciones disponibles para un :class:`EstudioProgramado`"""

    context_object_name = 'estudio'
    model = EstudioProgramado
    template_name = 'examen/estudio_detail.html'


class EstudioProgramadoCreateView(CreateView, LoginRequiredMixin):
    """Permite recetar un :class:`Examen` a una :class:`Persona"""

    model = EstudioProgramado
    form_class = EstudioProgramadoForm
    template_name = 'examen/estudio_programado_create.html'

    def get_form_kwargs(self):
        kwargs = super(EstudioProgramadoCreateView, self).get_form_kwargs()
        kwargs.update({'initial': {'persona': self.persona.id}})
        return kwargs

    def dispatch(self, *args, **kwargs):
        """Agrega la persona como parametro del Estudio a programar"""

        self.persona = get_object_or_404(Persona, pk=kwargs['persona'])
        return super(EstudioProgramadoCreateView, self).dispatch(*args,
                                                                 **kwargs)

    def form_valid(self, form):
        """Asocia el estudio a realizar con la persona que se incluye en
        los parametros"""

        self.object = form.save(commit=False)
        self.object.persona = self.persona
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


class EstudioProgramadoListView(ListView, LoginRequiredMixin):
    """Permite mostrar una lista de :class:`Estudios`es que aún no han sido
    llevados a cabo"""

    template_name = 'examen/estudio_programado_list.html'
    paginate_by = 25
    context_object_name = 'estudios_programados'

    def get_queryset(self):
        """Filtra los resultados para mostrar solo los estudios no realizados"""

        return EstudioProgramado.objects.filter(efectuado=False)

    def get_context_data(self, **kwargs):
        """Agrega los ultimos :class:`Examen`es efectuados a la vista"""

        context = super(EstudioProgramadoListView, self).get_context_data(
            **kwargs)
        context['examenes'] = Examen.objects.all().order_by('-fecha')[:20]
        return context


class EstudioProgramadoEfectuarView(RedirectView, LoginRequiredMixin):
    """Permite marcar un :class:`EstudioProgramado` como ya efectuado y
    muestra el formulario para crear un nuevo :class:`Examen` a la
    :class:`Persona`"""

    permanent = False

    def get_redirect_url(self, **kwargs):
        estudio = get_object_or_404(EstudioProgramado, pk=kwargs['pk'])
        examen = estudio.efectuar()
        examen.usuario = self.request.user
        examen.save()
        messages.info(self.request,
                      u'¡El estudio ha sido marcado como efectuado!')
        return reverse('examen-edit', args=[examen.id])


class EstudioPreCreateView(TemplateView, LoginRequiredMixin):
    """Permite mostrar una interfaz donde decidir si agregar una nueva
    :class:`Persona` o agregar el :class:`Examen a una ya ingresada previamente
    """

    template_name = 'examen/examen_agregar.html'

    def get_context_data(self, **kwargs):
        """Agrega el formulario de :class:`Persona` a la vista"""

        context = super(EstudioPreCreateView, self).get_context_data()
        context['persona_search_form'] = PersonaSearchForm()
        context['persona_form'] = PersonaForm()
        context['persona_form'].helper.form_action = 'examen-persona-nuevo'
        return context


class EstudioCreateView(ExamenFormMixin):
    model = Estudio
    form_class = EstudioForm
