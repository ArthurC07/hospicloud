# -*- coding: utf-8 -*-
#
# Copyright (C) 2015 Carlos Flores <cafg10@gmail.com>
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

from django.conf.urls import url

from income import views

urlpatterns = [
    url(r'^$', views.IncomeIndexView.as_view(), name='income-index'),
    url(r'^deposito/crear$', views.DepositoCreateView.as_view(),
        name='deposito-create'),
    url(r'^deposito/periodo$', views.DepositoPeriodoListView.as_view(),
        name='deposito-periodo'),
    url(r'^cheque/crear$', views.ChequeCreateView.as_view(),
        name='cheque-create'),
    url(r'^cheque/periodo$', views.ChequePeriodoListView.as_view(),
        name='cheque-periodo'),
    url(r'^cierre/crear$', views.CierrePOSCreateView.as_view(),
        name='cierre-create'),
    url(r'^cheque/(?P<pk>\d+)$', views.ChequeCobroDetailView.as_view(),
        name='cheque-detail'),
    url(r'^cheque/numero$', views.ChequeNumeroListView.as_view(),
        name='cheque-numero'),
    url(r'^cheque/detalle/crear$', views.DetallePagoCreateView.as_view(),
        name='detallepago-create'),
    url(r'^deposito/(?P<pk>\d+)$', views.ChequeCobroDetailView.as_view(),
        name='income-deposito'),

]
