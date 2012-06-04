# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import (DetailView, UpdateView, CreateView, ListView,
                                  TemplateView, RedirectView)
from imaging.forms import (ExamenForm, ImagenForm, AdjuntoForm, DicomForm,
                           EstudioProgramadoForm)
from imaging.models import Examen, Imagen, Adjunto, Dicom, EstudioProgramado
from library.protected import LoginRequiredView
from persona.forms import PersonaForm
from persona.models import Persona
from persona.views import PersonaCreateView
from django.contrib import messages

class ExamenIndexView(ListView):
    
    """Muestra un listado de los ultimos 5 :class:`Examen`es que se han
    ingresado al sistema"""

    template_name = 'examen/index.html'
    queryset = Examen.objects.all().order_by('-fecha')[:5]
    context_object_name = 'examenes'

class PersonaExamenCreateView(PersonaCreateView):
    
    """Permite agregar una :class:`Persona` para efectuarle un
    :class:`Examen`"""

    template_name = 'persona/persona_nuevo.html'
    
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

class ExamenDetailView(DetailView, LoginRequiredView):
    
    """Permite ver los detalles de un :class:`Examen`"""
    
    context_object_name = 'examen'
    model = Examen
    template_name = 'examen/examen_detail.html'
    slug_field = 'uuid'

class ExamenPersonaListView(DetailView, LoginRequiredView):
    
    """Muestra los :class:`Examen`es realizados a una :class:`Persona`"""

    context_object_name = 'persona'
    model = Persona
    template_name = 'examen/examen_paciente_detail.html'

class ExamenUpdateView(UpdateView, LoginRequiredView):
    
    """Permite actualizar los datos de un :class:`Examen`"""
    
    model = Examen
    form_class = ExamenForm
    template_name = 'examen/examen_update.html'

class ExamenCreateView(CreateView, LoginRequiredView):
    
    """Permite crear un :class:`Examen` a una :class:`Persona`"""
    
    model = Examen
    form_class = ExamenForm
    template_name = 'examen/examen_create.html'
    
    def get_form_kwargs(self):
        
        kwargs = super(ExamenCreateView, self).get_form_kwargs()
        kwargs.update({ 'initial':{'persona':self.persona.id}})
        return kwargs
    
    def dispatch(self, *args, **kwargs):
        
        self.persona = get_object_or_404(Persona, pk=kwargs['persona'])
        return super(ExamenCreateView, self).dispatch(*args, **kwargs)
    
    def form_valid(self, form):
        
        self.object = form.save(commit=False)
        self.object.persona = self.persona
        self.object.save()
        
        return HttpResponseRedirect(self.get_success_url())

class ExamenDocBaseCreateView(CreateView, LoginRequiredView):
    
    """Permite crear objetos que pertenecen a un :class:`Examen`"""

    def dispatch(self, *args, **kwargs):
        
        self.examen = get_object_or_404(Examen, pk=kwargs['examen'])
        return super(ExamenDocBaseCreateView, self).dispatch(*args, **kwargs)
    
    def get_form_kwargs(self):
        
        kwargs = super(ExamenDocBaseCreateView, self).get_form_kwargs()
        kwargs.update({ 'initial' : { 'examen' : self.examen.id } })
        return kwargs
    
    def form_valid(self, form):
        
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
        
        self.object = form.save(commit=False)
        self.object.examen = self.examen
        self.object.save()
        self.object.extraer_imagen()
        
        return HttpResponseRedirect(self.get_success_url())

class DicomDetailView(DetailView, LoginRequiredView):
    
    """Muestra el visor DICOM básico en el navegador del usuario"""

    context_object_name = 'dicom'
    model = Dicom
    template_name = "examen/dicom_detail.html"
    slug_field = 'uuid'

class EstudioProgramadoCreateView(CreateView, LoginRequiredView):

    """Permite recetar un :class:`Examen` a una :class:`Persona"""
    
    model = EstudioProgramado
    form_class = EstudioProgramadoForm
    template_name = 'examen/estudio_programado_create.html'
    
    def get_form_kwargs(self):
        
        kwargs = super(EstudioProgramadoCreateView, self).get_form_kwargs()
        kwargs.update({ 'initial':{'persona':self.persona.id}})
        return kwargs
    
    def dispatch(self, *args, **kwargs):
        
        self.persona = get_object_or_404(Persona, pk=kwargs['persona'])
        return super(EstudioProgramadoCreateView, self).dispatch(*args, **kwargs)
    
    def form_valid(self, form):
        
        self.object = form.save(commit=False)
        self.object.persona = self.persona
        self.object.save()
        
        return HttpResponseRedirect(self.get_success_url())

class EstudioProgramadoListView(ListView, LoginRequiredView):

    """Permite mostrar una lista de :class:`Estudios`es que aún no han sido
    llevados a cabo"""
    
    template_name = 'examen/estudio_programado_list.html'
    paginate_by = 25
    context_object_name = 'estudios_programados'
    
    def get_queryset(self):
        
        """Filtra los resultados para mostrar solo los estudios no realizados"""
        
        return EstudioProgramado.objects.filter(efectuado=False)

class EstudioProgramadoEfectuarView(RedirectView, LoginRequiredView):
    
    """Permite marcar un :class:`EstudioProgramado` como ya efectuado y
    muestra el formulario para crear un nuevo :class:`Examen` a la
    :class:`Persona`"""
     
    permanent = False
    
    def get_redirect_url(self, **kwargs):
        
        estudio = get_object_or_404(EstudioProgramado, pk=kwargs['pk'])
        estudio.efectuado = True
        dosis.save()
        messages.info(self.request, u'¡El estudio ha sido marcado como efectuado!')
        return reverse('examen-agregar', args=[estudio.persona.id])
