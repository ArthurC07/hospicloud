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
    NotaEnfermeriaForm, OrdenMedicaForm, SignoVitalForm, MedicamentoForm)
from nightingale.models import (Cargo, Evolucion, Glicemia, Insulina,
                                Glucosuria, Ingesta, Excreta, NotaEnfermeria,
                                OrdenMedica, SignoVital, Medicamento, Dosis)
from spital.models import Admision
from django.contrib import messages
from datetime import datetime

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

class NightingaleDetailView(DetailView, LoginRequiredView):
    
    """Permite ver los datos de una :class:`Admision` desde la interfaz de
    enfermeria"""

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
        signos = self.object.signos_vitales
        if self.object.signos_vitales.count() == 0:
            context['temp_promedio'] = 0
        else:
            context['temp_promedio'] = self.object.temperatura_promedio
        
        if self.object.signos_vitales.count() == 0:
            context['pulso_promedio'] = 0
        else:
            context['pulso_promedio'] = self.object.pulso_promedio
        
        if self.object.signos_vitales.count() == 0:
            context['presion_diastolica_promedio'] = 0
        else:
            context['presion_diastolica_promedio'] = self.object.presion_diastolica_promedio
        
        if self.object.signos_vitales.count() == 0:
            context['presion_sistolica_promedio'] = 0
        else:
            context['presion_sistolica_promedio'] = self.object.presion_sistolica_promedio
        
        context['pulso'] = '[0 , 0],' + u','.join('[{0}, {1}]'.format(n + 1, signos.all()[n].pulso) for n in range(signos.count()))
        context['temperatura'] = '[0 , 0],' + u','.join('[{0}, {1}]'.format(n + 1, signos.all()[n].temperatura) for n in range(signos.count()))
        context['presion_sistolica'] = '[0 , 0],' + u','.join('[{0}, {1}]'.format(n + 1, signos.all()[n].presion_sistolica) for n in range(signos.count()))
        context['presion_diastolica'] = '[0 , 0],' + u','.join('[{0}, {1}]'.format(n + 1, signos.all()[n].presion_diastolica) for n in range(signos.count()))
        
        return context

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
        kwargs.update({ 'initial':{'admision':self.admision.id, 'fecha_y_hora': datetime.now(), 'usuario':self.request.user.id}})
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
    
    def form_valid(self, form):
        
        self.object = form.save(commit=False)
        self.object.admision = self.admision
        self.usuario = self.request.user
        self.object.save()
        self.object.crear_dosis()
        
        messages.info(self.request, u"Medicamento preescrito exitósamente")
        
        return HttpResponseRedirect(self.get_success_url())

class DosisSuministrarView(RedirectView, LoginRequiredView):

    """Permite marcar una :class:`Dosis` como ya suministrada"""
     
    permanent = False
    
    def get_redirect_url(self, **kwargs):
        
        """Obtiene la :class:`Dosis` desde la base de datos, la marca como
        suministrada, estampa la hora y el :class:`User` que la suministro"""

        dosis = get_object_or_404(Dosis, pk=kwargs['pk'])
        dosis.suministrada = True
        dosis.usuario = self.request.user
        dosis.fecha_y_hora = datetime.now()
        dosis.save()
        messages.info(self.request, u'¡Dosis registrada como suministrada!')
        return reverse('nightingale-view-id', args=[dosis.medicamento.admision.id])
