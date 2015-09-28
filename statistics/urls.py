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

from django.conf.urls import patterns, url
from statistics.views import (AtencionAdulto, Estadisticas, AtencionInfantil,
    Productividad, IngresosHospitalarios, AdmisionPeriodo, EmergenciaPeriodo,
    HabitacionPopularView, DiagnosticoView, DoctorView, CargoView)

urlpatterns = patterns('',
    
    url(r'^$',
        Estadisticas.as_view(),
        name='estadisticas'),
    
    url(r'^estadisticas/adulto$',
        AtencionAdulto.as_view(),
        name='estadisticas-admision-adulto'),
    
    url(r'^estadisticas/infantil$',
        AtencionInfantil.as_view(),
        name='estadisticas-admision-infantil'),
    
    url(r'^estadisticas/productividad$',
        Productividad.as_view(),
        name='estadisticas-productividad'),
    
    url(r'^estadisticas/ingresos$',
        IngresosHospitalarios.as_view(),
        name='estadisticas-ingresos-hospitalarios'),
    
    url(r'^hospitalizado$',
        AdmisionPeriodo.as_view(),
        name='estadisticas-hospitalizacion'),

    url(r'^emergencia$',
        EmergenciaPeriodo.as_view(),
        name='estadisticas-emergencias'),

    url(r'^habitacion/popular$',
        HabitacionPopularView.as_view(),
        name='estadisticas-habitacion-popular'),

    url(r'^admision/diagnostico$',
        DiagnosticoView.as_view(),
        name='estadisticas-diagnostico'),

    url(r'^admision/doctor$',
        DoctorView.as_view(),
        name='estadisticas-doctor'),

    url(r'^admision/cargos$',
        CargoView.as_view(),
        name='estadisticas-cargo'),
)
