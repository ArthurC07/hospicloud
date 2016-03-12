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

from django.conf.urls import url
from statistics import views

urlpatterns = [

    url(r'^$',
        views.Estadisticas.as_view(),
        name='estadisticas'),

    url(r'^estadisticas/adulto$',
        views.AtencionAdulto.as_view(),
        name='estadisticas-admision-adulto'),

    url(r'^estadisticas/infantil$',
        views.AtencionInfantil.as_view(),
        name='estadisticas-admision-infantil'),

    url(r'^estadisticas/productividad$',
        views.Productividad.as_view(),
        name='estadisticas-productividad'),

    url(r'^estadisticas/ingresos$',
        views.IngresosHospitalarios.as_view(),
        name='estadisticas-ingresos-hospitalarios'),

    url(r'^hospitalizado$',
        views.AdmisionPeriodo.as_view(),
        name='estadisticas-hospitalizacion'),

    url(r'^emergencia$',
        views.EmergenciaPeriodo.as_view(),
        name='estadisticas-emergencias'),

    url(r'^habitacion/popular$',
        views.HabitacionPopularView.as_view(),
        name='estadisticas-habitacion-popular'),

    url(r'^admision/diagnostico$',
        views.DiagnosticoView.as_view(),
        name='estadisticas-diagnostico'),

    url(r'^admision/doctor$',
        views.DoctorView.as_view(),
        name='estadisticas-doctor'),

    url(r'^admision/cargos$',
        views.CargoView.as_view(),
        name='estadisticas-cargo'),
]
