# -*- coding: utf-8 -*-
#
# Copyright (C) 2011-2014 Carlos Flores <cafg10@gmail.com>
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

from invoice import views

urlpatterns = [

    url(r'^$', views.IndexView.as_view(), name='invoice-index'),

    url(r'^nuevo', views.ReciboCreateView.as_view(), name='invoice-new'),

    url(r'^(?P<persona>\d+)/crear', views.ReciboPersonaCreateView.as_view(),
        name='invoice-create'),

    url(r'^examen/(?P<examen>\d+)/crear',
        views.ReciboExamenCreateView.as_view(),
        name='invoice-create-examen'),

    url(r'^(?P<pk>\d+)$',
        views.ReciboDetailView.as_view(),
        name='invoice-view-id'),

    url(r'^(?P<pk>\d+)/impresion$',
        views.ReciboPrintView.as_view(),
        name='invoice-print'),

    url(r'^(?P<pk>\d+)/cambiar/tipo$', views.ReciboTipoFormUpdateView.as_view(),
        name='invoice-change-type'),

    url(r'^(?P<pk>\d+)/impresion/credito$',
        views.ReciboDetailView.as_view(
                template_name='invoice/recibo_credito.html'),
        name='invoice-print-credito'),

    url(r'^(?P<pk>\d+)/anular$',
        views.ReciboAnularView.as_view(),
        name='invoice-nullify'),

    url(r'^(?P<pk>\d+)/cerrar$',
        views.ReciboCerrarView.as_view(),
        name='invoice-close'),

    url(r'^(?P<recibo>\d+)/venta/add$',
        views.VentaCreateView.as_view(),
        name='venta-add'),

    url(r'^venta/(?P<pk>\d+)/delete$',
        views.VentaDeleteView.as_view(),
        name='venta-delete'),

    url(r'^pago/(?P<pk>\d+)/delete$',
        views.PagoDeleteView.as_view(),
        name='pago-delete'),

    url(r'^periodo$',
        views.ReporteReciboView.as_view(),
        name='invoice-periodo'),

    url(r'^estadisticas$',
        views.EstadisticasView.as_view(),
        name='invoice-estadisticas'),

    url(r'^numero$',
        views.ReciboNumeroListView.as_view(),
        name='invoice-numero'),

    url(r'^estadistica/periodo$',
        views.EstadisticasPeriodoView.as_view(),
        name='invoice-estadisticas-periodo'),

    url(r'^periodo/detalle$',
        views.ReporteReciboDetailView.as_view(),
        name='invoice-periodo-detail'),

    url(r'^periodo/tipo$',
        views.ReporteTipoView.as_view(),
        name='invoice-tipo'),

    url(r'^periodo/producto$',
        views.ReporteProductoView.as_view(),
        name='invoice-periodo-producto'),

    url(r'^periodo/pago$',
        views.PagoPeriodoView.as_view(),
        name='invoice-periodo-pago'),

    url(r'^pago/list$',
        views.PagoListView.as_view(),
        name='invoice-pago-list'),

    url(r'^pago/aseguradora/(?P<aseguradora>\d+)/list$',
        views.PagoAseguradoraList.as_view(),
        name='invoice-pago-aseguradora-list'),

    url(r'^periodo/emergencia$',
        views.EmergenciaPeriodoView.as_view(),
        name='invoice-periodo-emergencia'),

    url(r'^periodo/venta$',
        views.VentaListView.as_view(),
        name='periodo-venta'),

    url(r'^periodo/tipopago$',
        views.TipoPagoPeriodoView.as_view(),
        name='periodo-tipopago'),

    url(r'^periodo/ciudad$',
        views.CiudadPeriodoListView.as_view(),
        name='periodo-ciudad'),

    url(r'^periodo/turno',
        views.TurnoCajaPeriodoView.as_view(),
        name='turno-periodo'),

    url(r'^periodo/venta/area$',
        views.VentaAreaListView.as_view(),
        name='periodo-venta-area'),

    url(r'^dia/emergencia$',
        views.EmergenciaDiaView.as_view(),
        name='invoice-dia-emergencia'),

    url(r'^examenes$',
        views.ExamenView.as_view(),
        name='invoice-imaging'),

    url(r'^corte$',
        views.CorteView.as_view(),
        name='invoice-corte'),

    url(r'^inventario',
        views.ReciboInventarioView.as_view(),
        name='invoice-inventario'),

    url(r'^dia/altas$',
        views.AdmisionAltaView.as_view(),
        name='invoice-dia-altas'),

    url(r'^emergencia/(?P<pk>\d+)$',
        views.EmergenciaFacturarView.as_view(),
        name='emergency-invoice'),

    url(r'^admision/(?P<pk>\d+)$',
        views.AdmisionFacturarView.as_view(),
        name='admision-invoice'),

    url(r'^deposito/(?P<pk>\d+)$',
        views.DepositoFacturarView.as_view(),
        name='deposito-invoice'),

    url(r'^examen/(?P<pk>\d+)$',
        views.ExamenFacturarView.as_view(),
        name='examen-invoice'),

    url(r'^consulta/(?P<pk>\d+)$',
        views.ConsultaFacturarView.as_view(),
        name='consulta-invoice'),

    url(r'^aseguradora/(?P<pk>\d+)$',
        views.AseguradoraContractsFacturarView.as_view(),
        name='aseguradora-invoice'),

    url(r'^aseguradora/(?P<pk>\d+)$',
        views.AseguradoraMasterFacturarView.as_view(),
        name='aseguradora-invoice-master'),

    url(r'^aseguradora/contratos/cotizar/(?P<pk>\d+)$',
        views.AseguradoraContractsCotizarView.as_view(),
        name='aseguradora-cotizar-contrato'),

    url(r'^aseguradora/maestro/cotizar/(?P<pk>\d+)$',
        views.AseguradoraMasterCotizarView.as_view(),
        name='aseguradora-cotizar-master'),

    url(r'^aseguradora/list$',
        views.AseguradoraListView.as_view(),
        name='invoice-aseguradora-list'),

    url(r'^master/cotizar/(?P<pk>\d+)$',
        views.MasterCotizarView.as_view(),
        name='master-cotizar'),

    url(r'^(?P<recibo>\d+)/pago/add$',
        views.PagoCreateView.as_view(),
        name='pago-add'),

    url(r'^pago/(?P<pk>\d+)/status/edit$',
        views.PagoUpdateView.as_view(),
        name='invoice-pago-status-edit'),

    url(r'^pago/status$',
        views.StatusPagoListView.as_view(),
        name='invoice-pago-status-index'),

    url(r'^turno/(?P<pk>\d+)$',
        views.TurnoCajaDetailView.as_view(),
        name='invoice-turno'),

    url(r'^turno/(?P<pk>\d+)/recibos$',
        views.TurnoCajaDetailView.as_view(
                template_name="invoice/turno_recibo_list.html"),
        name='invoice-turno-recibos'),

    url(r'^turno/nuevo',
        views.TurnoCajaCreateView.as_view(),
        name='invoice-turno-nuevo'),

    url(r'^turno/(?P<turno>\d+)/cierre/nuevo$',
        views.CierreTurnoCreateView.as_view(),
        name='invoice-cierre-nuevo'),

    url(r'^cierre/(?P<pk>\d+)/delete$',
        views.CierreTurnoDeleteView.as_view(),
        name='cierre-delete'),

    url(r'^turno/(?P<pk>\d+)/update$',
        views.TurnoCajaUpdateView.as_view(),
        name='invoice-turno-edit'),

    url(r'^deposito/(?P<pk>\d+)$',
        views.DepositoDetailView.as_view(),
        name='invoice-deposito'),

    url(r'^turno/(?P<pk>\d+)/cerrar$',
        views.TurnoCierreUpdateView.as_view(),
        name='invoice-turno-cerrar'),

    url(r'^turno/activos$',
        views.TurnoCajaListView.as_view(),
        name='invoice-turno-activo'),

    url(r'^cpc$',
        views.CuentaPorCobrarListView.as_view(),
        name='invoice-cpc-list'),

    url(r'^cpc/(?P<pk>\d+)$',
        views.CuentaPorCobrarDetailView.as_view(),
        name='invoice-cpc'),

    url(r'^cpc/agregar$',
        views.CuentaPorCobrarCreateView.as_view(),
        name='invoice-cpc-add'),

    url(r'^pago/(?P<pk>\d+)/status/next$',
        views.PagoSiguienteStatusView.as_view(),
        name='invoice-pago-status-next'),

    url(r'^cpc/(?P<pk>\d+)/status/next$',
        views.CuentaPorCobrarSiguienteStatusRedirectView.as_view(),
        name='invoice-cpc-status-next'),

    url(r'^cpc/(?P<pk>\d+)/status/previous$',
        views.CuentaPorCobrarAnteriorStatusRedirectView.as_view(),
        name='invoice-cpc-status-previous'),

    url(r'^cpc/(?P<cuenta>\d+)/pago/next$',
        views.PagoCuentaCreateView.as_view(),
        name='invoice-cpc-pago-add'),

    url(r'^notification/(?P<pk>\d+)$',
        views.NotificationDetailView.as_view(),
        name='notification'),

    url(r'^cotizacion/(?P<pk>\d+)$',
        views.CotizacionDetailView.as_view(),
        name='cotizacion'),

    url(r'^cotizacion/(?P<cotizacion>\d+)/cotizado/agregar$',
        views.CotizadoCreateView.as_view(),
        name='cotizado-add'),

    url(r'^(?P<persona>\d+)/cotizacion/agregar$',
        views.CotizacionCreateView.as_view(),
        name='cotizacion-add'),

    url(r'^cotizado/(?P<pk>\d+)/delete$',
        views.CotizadoDeleteView.as_view(),
        name='cotizado-delete'),

    url(r'^cotizado/(?P<pk>\d+)/editar$',
        views.CotizadoUpdateView.as_view(),
        name='cotizado-edit'),

    url(r'^cotizacion/(?P<pk>\d+)/facturar$',
        views.CotizacionFacturar.as_view(),
        name='cotizacion-facturar'),

    url(r'^comprobante/agregar$',
        views.ComprobanteDeduccionCreateView.as_view(),
        name='comprobante-agregar'),

    url(r'^comprobante/(?P<pk>\d+)$',
        views.ComprobanteDeduccionDetailView.as_view(),
        name='comprobante'),

    url(r'^comprobante/list$',
        views.ComprobanteDeduccionListView.as_view(),
        name='invoice-comprobantededuccion-list'),

    url(r'^comprobante/(?P<pk>\d+)/imprimir$',
        views.ComprobanteDeduccionDetailView.as_view(
                template_name='invoice/comprobantededuccion_print.html'
        ),
        name='comprobante-print'),

    url(r'^comprobante/(?P<comprobante>\d+)/concepto/add$',
        views.ConceptoDeduccionCreateView.as_view(),
        name='concepto-agregar'),

    url(r'^reembolso/agregar$',
        views.ReembolsoCreateView.as_view(),
        name='reembolso-add'),

]
