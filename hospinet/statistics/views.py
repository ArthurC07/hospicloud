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

import calendar
from datetime import date
from decimal import Decimal
from datetime import datetime, time
from collections import defaultdict

from django.views.generic.base import TemplateView
from django.shortcuts import redirect
from crispy_forms.layout import Fieldset
from imaging.models import Examen

from statistics.forms import ReporteAnualForm, ReporteMensualForm
from spital.models import Habitacion, Admision, PreAdmision
from invoice.forms import PeriodoForm
from emergency.models import Emergencia
from users.mixins import LoginRequiredMixin


class HabitacionAdapter(object):
    def __init__(self):
        self.admisiones = 0
        self.dias = 0


class Estadisticas(TemplateView, LoginRequiredMixin):
    template_name = 'estadisticas/index.html'

    def create_forms(self, context):
        context['formulario_anual'] = ReporteAnualForm()

        context['admision_periodo'] = PeriodoForm(prefix='admisiones')
        context['admision_periodo'].helper.form_action = \
            'estadisticas-hospitalizacion'
        context['admision_periodo'].helper.layout = Fieldset(
            u'Admisiones por Periodo',
            *context['admision_periodo'].field_names)

        context['emergencia_periodo'] = PeriodoForm(prefix='emergencia')
        context['emergencia_periodo'].helper.form_action = \
            'estadisticas-emergencias'
        context['emergencia_periodo'].helper.layout = Fieldset(
            u'Emergencias por Periodo',
            *context['emergencia_periodo'].field_names)

        context['habitacion_popular'] = PeriodoForm(prefix='popular')
        context['habitacion_popular'].helper.form_action = \
            'estadisticas-habitacion-popular'
        context['habitacion_popular'].helper.layout = Fieldset(
            u'Uso de Habitaciones',
            *context['habitacion_popular'].field_names)

        context['diagnostico'] = PeriodoForm(prefix='diagnostico')
        context['diagnostico'].helper.form_action = 'estadisticas-diagnostico'
        context['diagnostico'].helper.layout = Fieldset(
            u'Admisiones por Diagnóstico',
            *context['diagnostico'].field_names)

        context['doctor'] = PeriodoForm(prefix='doctor')
        context['doctor'].helper.form_action = 'estadisticas-doctor'
        context['doctor'].helper.layout = Fieldset(
            u'Admisiones por Doctor',
            *context['doctor'].field_names)

        context['cargo'] = PeriodoForm(prefix='cargos')
        context['cargo'].helper.form_action = 'estadisticas-cargo'
        context['cargo'].helper.layout = Fieldset(
            u'Cargos por Periodo',
            *context['cargo'].field_names)

    def get_fechas(self):

        now = date.today()
        self.fin = date(now.year, now.month,
                        calendar.monthrange(now.year, now.month)[1])
        self.inicio = date(now.year, now.month, 1)
        self.inicio = datetime.combine(self.inicio, time.min)
        self.fin = datetime.combine(self.fin, time.max)

    def get_admisiones(self):

        self.admisiones = Admision.objects.filter(
            admision__range=(self.inicio, self.fin),
            habitacion__isnull=False)

    def get_diagnosticos(self, context):

        diangosticos = defaultdict(int)
        for admision in self.admisiones.all():
            diangosticos[admision.diagnostico.upper()] += 1
        context['diagnosticos'] = sorted(diangosticos.iteritems())

    def get_habitaciones(self, context):
        habitaciones = defaultdict(HabitacionAdapter)
        context['dias'] = 0
        context['total'] = 0

        for habitacion in Habitacion.objects.all():
            habitaciones[habitacion].admisiones += self.admisiones.filter(
                habitacion=habitacion).count()
        for admision in self.admisiones.all():
            habitaciones[
                admision.habitacion].dias += admision.tiempo_hospitalizado()
        context['habitaciones'] = sorted(habitaciones.items(),
                                         key=lambda x: x[0].tipo)

        for habitacion in Habitacion.objects.all():
            context['total'] += habitaciones[habitacion].admisiones
            context['dias'] += habitaciones[habitacion].dias

    def get_doctor(self, context):

        doctores = defaultdict(int)

        for admision in self.admisiones.all():
            doctor = admision.doctor.upper().split('/')[0].rstrip()

            doctores[doctor] += 1

        context['doctores'] = reversed(
            sorted(doctores.iteritems(), key=lambda x: x[1]))
        context['total_doctores'] = sum(doctores[d] for d in doctores)
        return context

    def get_year(self, context):

        today = date.today()
        admisiones = Admision.objects.filter(momento__year=today.year,
                                             habitacion__isnull=False)
        meses = defaultdict(int)
        for n in range(1, 13):
            meses[n] = 0

        for admision in admisiones.all():
            meses[admision.momento.month] += 1

        context['meses'] = list()
        for mes in sorted(meses.iteritems()):
            context['meses'].append((calendar.month_name[mes[0]], mes[1]))

        return context

    def get_emergencies(self, context):

        self.emergencias = Emergencia.objects.filter(
            created__gte=self.inicio,
            created__lte=self.fin
        )

        context['emergencias'] = self.emergencias

        doctores = defaultdict(int)
        for emergencia in self.emergencias:
            doctores[emergencia.usuario] += 1

        context['emergencia_doctores'] = reversed(
            sorted(doctores.items(), key=lambda x: x[1]))
        context['emergencia_grafico'] = reversed(
            sorted(doctores.items(), key=lambda x: x[1]))
        context['emergencia_grafico2'] = reversed(
            sorted(doctores.items(), key=lambda x: x[1]))
        context['emergencia_total'] = self.emergencias.count()

        return context

    def get_preadmision(self, context):

        self.preadmisiones = PreAdmision.objects.filter(
            emergencia__created__gte=self.inicio,
            emergencia__created__lte=self.fin
        )

        context['preadmisiones'] = self.emergencias

        doctores = defaultdict(int)
        for preadmision in self.preadmisiones:
            doctores[preadmision.emergencia.usuario] += 1

        context['preadmision_doctores'] = reversed(
            sorted(doctores.items(), key=lambda x: x[1]))
        context['preadmision_grafico'] = reversed(
            sorted(doctores.items(), key=lambda x: x[1]))
        context['preadmision_grafico2'] = reversed(
            sorted(doctores.items(), key=lambda x: x[1]))
        context['preadmision_total'] = self.preadmisiones.count()

        return context

    def get_examenes(self, context):

        self.examenes = Examen.objects.filter(
            fecha__gte=self.inicio,
            fecha__lte=self.fin
        )

        context['examenes'] = self.examenes

        doctores = defaultdict(int)
        examenes = defaultdict(int)
        for examen in self.examenes:
            doctores[examen.usuario] += 1
            examenes[examen.tipo_de_examen.item] += 1

        context['examenes_tecnicos'] = reversed(
            sorted(doctores.items(), key=lambda x: x[1]))
        context['examenes_grafico'] = reversed(
            sorted(examenes.items(), key=lambda x: x[1]))
        context['examenes_grafico2'] = reversed(
            sorted(examenes.items(), key=lambda x: x[1]))
        context['examenes_tipo'] = reversed(
            sorted(examenes.items(), key=lambda x: x[1]))

        context['examenes_total'] = self.examenes.count()

        return context

    def get_context_data(self, **kwargs):

        context = super(Estadisticas, self).get_context_data(**kwargs)

        self.create_forms(context)
        self.get_fechas()
        self.get_admisiones()

        self.get_habitaciones(context)
        self.get_diagnosticos(context)
        self.get_doctor(context)
        self.get_year(context)
        self.get_emergencies(context)
        self.get_preadmision(context)
        self.get_examenes(context)

        return context


class Atencion(object):
    """Permite calcular los puntos de ploteo para mostrar en un informe"""

    def calcular_meses(self, context, admisiones):
        dict_mes = dict((k, v) for k, v in enumerate(calendar.month_abbr))
        calc_mes = lambda m: (m, admisiones.filter(momento__month=m).count())
        context['meses'] = dict()
        parejas = map(calc_mes, range(1, 13))
        for pareja in parejas:
            mes = dict_mes[pareja[0]]
            context['meses'][mes] = pareja[1]

        return ','.join('[{0}, {1}]'.format(p[0], p[1]) for p in parejas)


class AtencionAdulto(TemplateView, Atencion, LoginRequiredMixin):
    template_name = 'estadisticas/atencion_adulto.html'

    def get_context_data(self, **kwargs):
        context = super(AtencionAdulto, self).get_context_data(**kwargs)
        form = ReporteAnualForm(self.request.GET)
        if not form.is_valid():
            redirect('admision-estadisticas')
        anio = form.cleaned_data['anio']
        # obtener la fecha de nacimiento máxima
        edad_min = date(anio - 18, 12, 31)
        admisiones = Admision.objects.filter(
            momento__year=anio,
            paciente__nacimiento__lte=edad_min)

        context['puntos'] = self.calcular_meses(context, admisiones)

        return context


class AtencionInfantil(TemplateView, Atencion, LoginRequiredMixin):
    template_name = 'estadisticas/atencion_infantil.html'

    def get_context_data(self, **kwargs):
        context = super(AtencionInfantil, self).get_context_data(**kwargs)
        form = ReporteAnualForm(self.request.GET)
        if not form.is_valid():
            redirect('admision-estadisticas')
        anio = form.cleaned_data['anio']
        # obtener la fecha de nacimiento mínima
        edad_min = date(anio - 18, 12, 31)
        admisiones = Admision.objects.filter(
            momento__year=anio,
            paciente__nacimiento__gte=edad_min)

        context['puntos'] = self.calcular_meses(context, admisiones)

        return context


class Productividad(TemplateView, LoginRequiredMixin):
    template_name = 'estadisticas/productividad.html'

    def get_context_data(self, **kwargs):
        context = super(Productividad, self).get_context_data(**kwargs)
        form = ReporteMensualForm(self.request.GET)
        if not form.is_valid():
            redirect('admision-estadisticas')
        anio = form.cleaned_data['anio']
        mes = form.cleaned_data['mes']
        # obtener la fecha de nacimiento máxima
        edad_min = date(anio - 18, 12, 31)

        context['adultos_m'] = Admision.objects.filter(
            momento__year=anio,
            momento__month=mes,
            paciente__nacimiento__lte=edad_min,
            paciente__sexo='M').count()
        context['adultos_f'] = Admision.objects.filter(
            momento__year=anio,
            momento__month=mes,
            paciente__nacimiento__lte=edad_min,
            paciente__sexo='F').count()
        context['adultos'] = Admision.objects.filter(
            momento__year=anio,
            momento__month=mes,
            paciente__nacimiento__lte=edad_min).count()

        context['infantes_m'] = Admision.objects.filter(
            momento__year=anio,
            momento__month=mes,
            paciente__nacimiento__gte=edad_min,
            sexo='M').count()
        context['infantes_f'] = Admision.objects.filter(
            momento__year=anio,
            momento__month=mes,
            paciente__nacimiento__gte=edad_min,
            paciente__sexo='F').count()
        context['adultos'] = Admision.objects.filter(
            momento__year=anio,
            momento__month=mes,
            paciente__nacimiento__lte=edad_min).count()

        context['neonatos_m'] = Admision.objects.filter(
            momento__year=anio,
            momento__month=mes,
            neonato=True,
            sexo='M').count()
        context['neonatos_f'] = Admision.objects.filter(
            momento__year=anio,
            momento__month=mes,
            neonato=True,
            paciente__sexo='F').count()

        context['neonatos'] = Admision.objects.filter(
            momento__year=anio,
            momento__month=mes,
            neonato=True).count()

        context['admisiones'] = Admision.objects.filter(
            momento__year=anio,
            momento__month=mes,
            neonato=True).count()

        return context


class IngresosHospitalarios(TemplateView, Atencion, LoginRequiredMixin):
    template_name = 'estadisticas/ingresos_hospitalarios.html'

    def get_context_data(self, **kwargs):
        context = super(IngresosHospitalarios, self).get_context_data(**kwargs)
        form = ReporteAnualForm(self.request.GET)
        if not form.is_valid():
            redirect('admision-estadisticas')
        anio = form.cleaned_data['anio']
        # obtener la fecha de nacimiento mínima
        admisiones = Admision.objects.filter(
            momento__year=anio)

        context['puntos'] = self.calcular_meses(context, admisiones)

        return context


class PeriodoMixin(TemplateView):
    def dispatch(self, request, *args, **kwargs):

        """Filtra las :class:`Admision` de acuerdo a los datos ingresados en
        el formulario"""

        if self.form.is_valid():

            self.inicio = datetime.combine(self.form.cleaned_data['inicio'],
                                           time.min)
            self.fin = datetime.combine(self.form.cleaned_data['fin'], time.max)

        else:
            return redirect('estadisticas')

        return super(PeriodoMixin, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):

        context = super(PeriodoMixin, self).get_context_data(**kwargs)

        context['inicio'] = self.inicio
        context['fin'] = self.fin

        return context


class AdmisionPeriodoMixin(TemplateView):
    def dispatch(self, request, *args, **kwargs):

        """Filtra las :class:`Admision` de acuerdo a los datos ingresados en
        el formulario"""

        if self.form.is_valid():

            self.inicio = self.form.cleaned_data['inicio']
            self.fin = self.form.cleaned_data['fin']
            self.inicio = datetime.combine(self.inicio, time.min)
            self.fin = datetime.combine(self.fin, time.max)
            self.admisiones = Admision.objects.filter(
                admision__range=(self.inicio, self.fin),
                habitacion__isnull=False)

        else:
            return redirect('estadisticas')

        return super(AdmisionPeriodoMixin, self).dispatch(request, *args,
                                                          **kwargs)

    def get_context_data(self, **kwargs):

        context = super(AdmisionPeriodoMixin, self).get_context_data(**kwargs)

        context['inicio'] = self.inicio
        context['fin'] = self.fin

        return context


class HabitacionPopularView(AdmisionPeriodoMixin, LoginRequiredMixin):
    template_name = 'estadisticas/habitacion_popular.html'

    def dispatch(self, request, *args, **kwargs):
        """Filtra las :class:`Admision` de acuerdo a los datos ingresados en
        el formulario"""

        self.form = PeriodoForm(request.GET, prefix='popular')

        return super(HabitacionPopularView, self).dispatch(request, *args,
                                                           **kwargs)

    def get_context_data(self, **kwargs):
        context = super(HabitacionPopularView, self).get_context_data(**kwargs)

        habitaciones = defaultdict(HabitacionAdapter)
        context['total'] = 0
        context['dias'] = 0
        for habitacion in Habitacion.objects.all():
            habitaciones[habitacion].admisiones += self.admisiones.filter(
                habitacion=habitacion).count()

        for admision in self.admisiones.all():
            habitaciones[
                admision.habitacion].dias += admision.tiempo_hospitalizado()

        for habitacion in Habitacion.objects.all():
            context['total'] += habitaciones[habitacion].admisiones
            context['dias'] += habitaciones[habitacion].dias

        context['habitaciones'] = sorted(habitaciones.iteritems())
        return context


class DiagnosticoView(AdmisionPeriodoMixin, LoginRequiredMixin):
    template_name = 'estadisticas/diagnostico.html'

    def dispatch(self, request, *args, **kwargs):
        """Filtra las :class:`Admision` de acuerdo a los datos ingresados en
        el formulario"""

        self.form = PeriodoForm(request.GET, prefix='diagnostico')

        return super(DiagnosticoView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DiagnosticoView, self).get_context_data(**kwargs)

        diangosticos = defaultdict(int)

        for admision in self.admisiones.all():
            diangosticos[admision.diagnostico.upper()] += 1

        context['diagnosticos'] = sorted(diangosticos.iteritems())
        return context


class DoctorView(AdmisionPeriodoMixin, LoginRequiredMixin):
    template_name = 'estadisticas/doctor.html'

    def dispatch(self, request, *args, **kwargs):
        """Filtra las :class:`Admision` de acuerdo a los datos ingresados en
        el formulario"""

        self.form = PeriodoForm(request.GET, prefix='doctor')

        return super(DoctorView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DoctorView, self).get_context_data(**kwargs)

        doctores = defaultdict(int)

        for admision in self.admisiones.all():
            doctor = admision.doctor.upper().split('/')[0].rstrip()

            doctores[doctor] += 1

        context['doctores'] = sorted(doctores.iteritems())
        return context


class CargoView(AdmisionPeriodoMixin, LoginRequiredMixin):
    template_name = 'estadisticas/cargo.html'

    def dispatch(self, request, *args, **kwargs):
        """Filtra las :class:`Admision` de acuerdo a los datos ingresados en
        el formulario"""

        self.form = PeriodoForm(request.GET, prefix='cargos')

        return super(CargoView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CargoView, self).get_context_data(**kwargs)

        cargos = defaultdict(int)

        for admision in self.admisiones.all():

            charges = admision.agrupar_cargos()

            for cargo in charges:
                cargos[cargo] += int(charges[cargo].cantidad)

        context['cargos'] = sorted(cargos.iteritems())
        return context


class AdmisionPeriodo(AdmisionPeriodoMixin, LoginRequiredMixin):
    template_name = 'estadisticas/admision.html'

    def dispatch(self, request, *args, **kwargs):

        self.form = PeriodoForm(request.GET, prefix='admisiones')

        return super(AdmisionPeriodo, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):

        context = super(AdmisionPeriodo, self).get_context_data(**kwargs)
        context['admisiones'] = self.admisiones
        if self.admisiones.count():
            context['tiempo_promedio'] = sum(a.tiempo_hospitalizado() for a in
                                             self.admisiones.all()) / self \
                                             .admisiones.count()
        else:
            context['tiempo_promedio'] = 0
            # Calcular todos los cargos efectuados en estas hospitalizaciones
        cargos = defaultdict(Decimal)
        habitaciones = defaultdict(int)
        for admision in self.admisiones:

            for cargo in admision.cargos.all():
                cargos[cargo.cargo] += cargo.cantidad

            habitaciones[admision.habitacion] += admision.tiempo_hospitalizado()

        context['cargos'] = cargos.items()
        context['habitaciones'] = habitaciones.items()
        context['total'] = sum(
            a.estado_de_cuenta(True) for a in self.admisiones)
        return context


class TratanteEstadisticaView(AdmisionPeriodoMixin, LoginRequiredMixin):
    template_name = 'estadisticas/tratante.html'

    def dispatch(self, request, *args, **kwargs):

        self.form = PeriodoForm(request.GET, prefix='admisiones')

        return super(TratanteEstadisticaView, self).dispatch(request, *args,
                                                             **kwargs)

    def get_context_data(self, **kwargs):

        context = super(TratanteEstadisticaView, self).get_context_data(
            **kwargs)
        context['admisiones'] = self.admisiones
        if self.admisiones.count():
            context['tiempo_promedio'] = sum(a.tiempo_hospitalizado() for a in
                                             self.admisiones.all()) / self \
                                             .admisiones.count()
        else:
            context['tiempo_promedio'] = 0
            # Calcular todos los cargos efectuados en estas hospitalizaciones
        cargos = defaultdict(Decimal)
        habitaciones = defaultdict(int)
        for admision in self.admisiones:

            for cargo in admision.cargos.all():
                cargos[cargo.cargo] += cargo.cantidad

            habitaciones[admision.habitacion] += admision.tiempo_hospitalizado()

        context['cargos'] = cargos.items()
        context['habitaciones'] = habitaciones.items()
        return context


class EmergenciaPeriodo(TemplateView):
    template_name = 'estadisticas/emergencia.html'

    def dispatch(self, request, *args, **kwargs):

        """Filtra las :class:`Admision` de acuerdo a los datos ingresados en
        el formulario"""

        self.form = PeriodoForm(request.GET, prefix='emergencia')
        if self.form.is_valid():

            self.inicio = self.form.cleaned_data['inicio']
            self.fin = datetime.combine(self.form.cleaned_data['fin'], time.max)
            self.emergencias = Emergencia.objects.filter(
                created__gte=self.inicio,
                created__lte=self.fin
            )

        else:

            return redirect('estadisticas')

        return super(EmergenciaPeriodo, self).dispatch(request, *args,
                                                       **kwargs)

    def get_context_data(self, **kwargs):

        context = super(EmergenciaPeriodo, self).get_context_data(**kwargs)
        context['inicio'] = self.inicio
        context['fin'] = self.fin
        context['emergencias'] = self.emergencias
        # Calcular todos los cargos efectuados en estas emergencias
        cargos = defaultdict(Decimal)

        doctores = defaultdict(int)
        for emergencia in self.emergencias:

            for cobro in emergencia.cobros.all():
                cargos[cobro.cargo] += cobro.cantidad
            doctores[emergencia.usuario] += 1

        context['cargos'] = cargos.items()

        context['doctores'] = reversed(
            sorted(doctores.items(), key=lambda x: x[1]))
        context['grafico'] = reversed(
            sorted(doctores.items(), key=lambda x: x[1]))
        context['grafico2'] = reversed(
            sorted(doctores.items(), key=lambda x: x[1]))
        context['total'] = sum(e.total() for e in self.emergencias)
        return context
