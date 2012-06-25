# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.db.models.query_utils import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import (ListView, UpdateView, DetailView, CreateView,
                                  RedirectView)
from library.protected import LoginRequiredView
from nightingale.forms import (IngresarForm, CargoForm, EvolucionForm,
    GlicemiaForm, InsulinaForm, GlucosuriaForm, IngestaForm, ExcretaForm,
    NotaEnfermeriaForm, OrdenMedicaForm, SignoVitalForm, MedicamentoForm,
    DosisForm, DevolucionForm)
from nightingale.models import (Cargo, Evolucion, Glicemia, Insulina,
    Glucosuria, Ingesta, Excreta, NotaEnfermeria, OrdenMedica, SignoVital,
    Medicamento, Dosis, Devolucion)
from spital.models import Admision
from django.contrib import messages
from django.utils import timezone

class NightingaleIndexView(ListView, LoginRequiredView):
    
    """Permite ingresar al lobby de Admisiones que estan siendo atendidas en
    una institucion hospitalaria"""

    queryset = Admision.objects.filter(Q(estado='H'))
    context_object_name = 'admitidos'
    template_name = 'enfermeria/index.html'
    
    def get_context_data(self, **kwargs):
        
        context = super(NightingaleIndexView, self).get_context_data(**kwargs)
        
        admisiones = self.queryset.all()
        context['hospitalizados'] = Admision.objects.filter(Q(estado='I'))
        if self.queryset.count() == 0:
            context['promedio'] = 0
        else:
            context['promedio'] = sum(a.tiempo_hospitalizacion()
                           for a in admisiones) / self.queryset.count()
        
        context['puntos'] = '[0 , 0],' + u','.join('[{0}, {1}]'.format(n + 1,
                                       admisiones[n].tiempo_hospitalizacion())
                      for n in range(self.queryset.count()))
        
        return context

class IngresarView(UpdateView, LoginRequiredView):
    
    """Permite actualizar los datos de ingreso en la central de enfermeria"""

    model = Admision
    form_class = IngresarForm
    template_name = 'enfermeria/ingresar.html'
    
    def get_success_url(self):
        
        self.object.ingresar()
        return reverse('nightingale-view-id', args=[self.object.id])

class NotaUpdateView(UpdateView, LoginRequiredView):
    
    """Permite editar una :class:`NotaEnfermeria` en caso de ser necesario"""

    model = NotaEnfermeria
    form_class = NotaEnfermeriaForm
    template_name = 'enfermeria/nota_create.html'

class NotaCerrarView(RedirectView, LoginRequiredView):

    """Permite cambiar el estado de un :class:`NotaEnfermeria`"""
     
    permanent = False
    
    def get_redirect_url(self, **kwargs):
        
        """Obtiene la :class:`NotaEnfermeria` desde la base de datos, y la
        marca como cerrada."""

        nota = get_object_or_404(NotaEnfermeria, pk=kwargs['pk'])
        nota.cerrada = True
        nota.save()
        return reverse('enfermeria-notas', args=[nota.admision.id])

class NightingaleDetailView(DetailView, LoginRequiredView):
    
    """Permite ver los datos de una :class:`Admision` desde la interfaz de
    enfermeria
    
    Esta vista se utiliza en conjunto con varias plantillas que permite mostrar
    una diversidad de datos como ser resumenes, :class:`NotaEnfermeria`s,
    :class:`SignoVital`es, :class:`OrdenMedica`s, y todos los demas datos que
    se relacionan con una :class:`Admision` de manera directa.
    """

    model = Admision
    template_name = 'enfermeria/nightingale_detail.html'
    slug_field = 'uuid'

class SignosDetailView(DetailView, LoginRequiredView):
    
    """Muestra los datos sobre los signos vitales de una :class:`Persona` en
    en una :class:`Admision`"""
    
    model = Admision
    template_name = 'enfermeria/signos_grafico.html'
    
    def get_context_data(self, **kwargs):

        """Formatea los datos para ser utilizado las graficas de signos
        vitales
        
        Actualmente se generan gráficas separadas para Pulso y Temperatura; la
        Presión Sistólica y Diastólica comparten una misma gráfica
        """
        
        context = super(SignosDetailView, self).get_context_data(**kwargs)
        signos = self.object.signos_vitales.extra(order_by=['fecha_y_hora']).all()

        context['min'] = self.object.hospitalizacion.strftime('%Y-%m-%d %H:%M')

        if self.object.signos_vitales.count() == 0:
            context['temp_promedio'] = 0
            context['pulso_promedio'] = 0
            context['presion_diastolica_promedio'] = 0
            context['presion_sistolica_promedio'] = 0
        else:
            context['temp_promedio'] = self.object.temperatura_promedio
            context['pulso_promedio'] = self.object.pulso_promedio
            context['presion_diastolica_promedio'] = self.object.presion_diastolica_promedio
            context['presion_sistolica_promedio'] = self.object.presion_sistolica_promedio
            inicio = signos[0].fecha_y_hora - timezone.timedelta(minutes=5)
            context['min'] = inicio.strftime('%Y-%m-%d %H:%M')
        
        context['pulso'] = u','.join("['{0}', {1}]".format(
                            s.fecha_y_hora.strftime('%Y-%m-%d %H:%M'), s.pulso)
                        for s in signos)
        context['temperatura'] = "['{0}', 37.00], ".format(context['min']) + \
                                 u','.join("['{0}', {1}]".format(
                                   s.fecha_y_hora.strftime('%Y-%m-%d %H:%M'),
                                   s.temperatura)
                        for s in signos)

        context['presion_sistolica'] = u','.join("['{0}', {1}]".format(
                                     s.fecha_y_hora.strftime('%Y-%m-%d %H:%M'),
                                     s.presion_sistolica)
                        for s in signos)

        context['presion_diastolica'] = u','.join("['{0}', {1}]".format(
                                     s.fecha_y_hora.strftime('%Y-%m-%d %H:%M'),
                                     s.presion_diastolica)
                        for s in signos)

        return context

class ResumenDetailView(NightingaleDetailView, SignosDetailView):
    
    """Muestra la información de una :class:`Admision` de forma totalmente
    consolidada, para evitar grandes saltos de navegación. También permite
    imprimir adecuadamente la historia clínica de la :class:`Persona` admitida
    durante esta :class:`Admision`
    """

    model = Admision
    template_name='enfermeria/resumen.html'
    slug_field = 'uuid'

class BaseCreateView(CreateView, LoginRequiredView):
    
    """Permite llenar el formulario de una clase que requiera
    :class:`Admision`es de manera previa - DRY"""

    def get_context_data(self, **kwargs):
        
        context = super(BaseCreateView, self).get_context_data(**kwargs)
        context['admision'] = self.admision
        return context
    
    def get_form_kwargs(self):
        
        """Agrega la :class:`Admision` obtenida como el valor a utilizar en el
        formulario que será llenado posteriormente"""

        kwargs = super(BaseCreateView, self).get_form_kwargs()
        kwargs.update({'initial':{'admision':self.admision.id,
                                  'fecha_y_hora': timezone.now(),
                                  'usuario':self.request.user.id}})
        return kwargs
    
    def dispatch(self, *args, **kwargs):
        
        """Obtiene la :class:`Admision` que se entrego como argumento en la
        url"""

        self.admision = get_object_or_404(Admision, pk=kwargs['admision'])
        return super(BaseCreateView, self).dispatch(*args, **kwargs)
    
    def form_valid(self, form):
        
        """Guarda el objeto generado espeficando la :class:`Admision` obtenida
        de los argumentos y el :class:`User` que esta utilizando la aplicación
        """

        self.object = form.save(commit=False)
        self.object.admision = self.admision
        self.usuario = self.request.user
        self.object.save()
        
        messages.info(self.request, u"Hospitalización Actualizada")
        
        return HttpResponseRedirect(self.get_success_url())

class CargoCreateView(BaseCreateView):
    
    """Permite crear un :class:`Cargo` a una :class:`Admision`"""
    
    model = Cargo
    form_class = CargoForm
    template_name = 'enfermeria/cargo_create.html'

class EvolucionCreateView(BaseCreateView):
    
    """Permite crear un :class:`Evolucion` a una :class:`Admision`"""
    
    model = Evolucion
    form_class = EvolucionForm
    template_name = 'enfermeria/evolucion_create.html'

class GlicemiaCreateView(BaseCreateView):
    
    """Permite registrar un :class:`Glicemia` efectuada a una
    :class:`Persona` durante una :class:`Admision`"""
    
    model = Glicemia
    form_class = GlicemiaForm
    template_name = 'enfermeria/glicemia_create.html'
    
class InsulinaCreateView(BaseCreateView):
    
    """Permite crear un dosis de :class:`Insulina` suministrada a una
    :class:`Persona` durante :class:`Admision`"""
    
    model = Insulina
    form_class = InsulinaForm
    template_name = 'enfermeria/insulina_create.html'

class GlucosuriaCreateView(BaseCreateView):
    
    """Permite registrar un :class:`Glucosuria` de una :class:`Persona`
    durante una :class:`Admision`"""
    
    model = Glucosuria
    form_class = GlucosuriaForm
    template_name = 'enfermeria/glucosuria_create.html'
    
class IngestaCreateView(BaseCreateView):
    
    """Permite crear un :class:`Examen` a una :class:`Persona`"""
    
    model = Ingesta
    form_class = IngestaForm
    template_name = 'enfermeria/ingesta_create.html'

class ExcretaCreateView(BaseCreateView):
    
    """Permite crear un :class:`Examen` a una :class:`Persona`"""
    
    model = Excreta
    form_class = ExcretaForm
    template_name = 'enfermeria/excreta_create.html'

class NotaCreateView(BaseCreateView):
    
    """Permite crear un :class:`Examen` a una :class:`Persona`"""
    
    model = NotaEnfermeria
    form_class = NotaEnfermeriaForm
    template_name = 'enfermeria/nota_create.html'

class OrdenCreateView(BaseCreateView):
    
    """Permite crear un :class:`Examen` a una :class:`Persona`"""
    
    model = OrdenMedica
    form_class = OrdenMedicaForm
    template_name = 'enfermeria/orden_create.html'

class SignoVitalCreateView(BaseCreateView):
    
    """Permite crear un :class:`Examen` a una :class:`Persona`"""
    
    model = SignoVital
    form_class = SignoVitalForm
    template_name = 'enfermeria/signo_create.html'

class MedicamentoCreateView(BaseCreateView):

    """Permite preescribir un :class:`Medicamento` a una :class:`Admision`"""

    model = Medicamento
    form_class = MedicamentoForm
    template_name = 'enfermeria/medicamento_create.html'
    
    def get_form_kwargs(self):
        
        """Agrega la :class:`Admision` obtenida como el valor a utilizar en el
        formulario que será llenado posteriormente"""

        kwargs = super(BaseCreateView, self).get_form_kwargs()
        kwargs.update({'initial':{'admision':self.admision.id,
                                  'fecha_y_hora': timezone.now(),
                                  'inicio': timezone.now(),
                                  'usuario':self.request.user.id}})
        return kwargs

class DosisCreateView(CreateView, LoginRequiredView):

    """Permite crear las :class:`Dosis` de un determinado :class:`Medicamento`
    que sera suministrado durante una :class:`Admision`
    
    Esto es agregado manualmente ya que la suministración de
    :class:`Medicamentos` es algo extremadamente subjetivo y varia de
    :class:`Persona` y doctor que lo indica
    """

    model = Dosis
    form_class = DosisForm
    template_name = 'enfermeria/dosis_create.html'

    def get_context_data(self, **kwargs):
        
        context = super(DosisCreateView, self).get_context_data(**kwargs)
        context['medicamento'] = self.medicamento
        return context
    
    def get_form_kwargs(self):
        
        """Agrega el :class:`Medicamento` obtenida como el valor a utilizar en el
        formulario que será llenado posteriormente"""

        kwargs = super(DosisCreateView, self).get_form_kwargs()
        kwargs.update({'initial':{'medicamento':self.admision.id,
                                  'fecha_y_hora': timezone.now(),
                                  'usuario':self.request.user.id,
                                  'administrador':self.request.user.id}})
        return kwargs
    
    def dispatch(self, *args, **kwargs):
        
        """Obtiene la :class:`Admision` que se entrego como argumento en la
        url"""

        self.admision = get_object_or_404(Medicamento, pk=kwargs['medicamento'])
        return super(DosisCreateView, self).dispatch(*args, **kwargs)
    
    def form_valid(self, form):
        
        """Guarda el objeto generado especificando el :class:`Medicamento`
        a ser administrado de los argumentos y el :class:`User` que
        esta utilizando la aplicación
        """

        self.object = form.save(commit=False)
        self.object.medicamento = self.medicamento
        self.usuario = self.request.user
        self.object.save()
        
        messages.info(self.request, u"Dosis recetada exitósamente")
        
        return HttpResponseRedirect(self.get_success_url())

class DosisSuministrarView(RedirectView, LoginRequiredView):

    """Permite marcar una :class:`Dosis` como ya suministrada"""
     
    permanent = False
    
    def get_redirect_url(self, **kwargs):
        
        """Obtiene la :class:`Dosis` desde la base de datos, la marca como
        suministrada, estampa la hora y el :class:`User` que la suministro"""

        dosis = get_object_or_404(Dosis, pk=kwargs['pk'])
        dosis.estado = kwargs['estado']
        dosis.usuario = self.request.user
        dosis.fecha_y_hora = timezone.now()
        dosis.save()
        messages.info(self.request, u'¡Dosis registrada como suministrada!')
        return reverse('nightingale-view-id', args=[dosis.medicamento.admision.id])

class MedicamentoSuspenderView(RedirectView, LoginRequiredView):

    """Permite cambiar el estado de un :class:`Medicamento`"""
     
    permanent = False
    
    def get_redirect_url(self, **kwargs):
        
        """Obtiene el :class:`Medicamento` desde la base de datos, la marca como
        suministrada, estampa la hora y el :class:`User` que la suministro"""

        medicamento = get_object_or_404(Medicamento, pk=kwargs['pk'])
        mediamento.estado = kwargs['estado']
        medicamento.save()
        return reverse('nightingale-view-id', args=[medicamento.admision.id])

class DevolucionCreateView(BaseCreateView):

    model = Devolucion
    form_class = DevolucionForm
    template_name = 'enfermeria/devolucion_create.html'
