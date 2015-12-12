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

from django.conf.urls import patterns, url

from invoice.views import (IndexView, ReciboPersonaCreateView, ReciboAnularView,
                           ReciboDetailView, VentaCreateView, ReporteReciboView,
                           ReporteProductoView, EmergenciaPeriodoView,
                           ReciboCerrarView, ReciboExamenCreateView,
                           EmergenciaDiaView, AdmisionAltaView, CorteView,
                           EmergenciaFacturarView, AdmisionFacturarView,
                           ExamenView, ReporteReciboDetailView, ReporteTipoView,
                           ReciboCreateView, ReciboInventarioView, PagoListView,
                           PagoCreateView, TurnoCajaCreateView,
                           TurnoCajaDetailView, CierreTurnoCreateView,
                           DepositoDetailView, ExamenFacturarView,
                           DepositoFacturarView, PagoCuentaCreateView,
                           VentaDeleteView, VentaListView, VentaAreaListView,
                           ConsultaFacturarView, TurnoCierreUpdateView,
                           TurnoCajaListView, AseguradoraContractsFacturarView,
                           PagoPeriodoView, ReciboPrintView, PagoUpdateView,
                           StatusPagoListView, TurnoCajaUpdateView,
                           TipoPagoPeriodoView, EstadisticasPeriodoView,
                           CiudadPeriodoListView, CotizadoDeleteView,
                           AseguradoraMasterFacturarView, PagoAseguradoraList,
                           CuentaPorCobrarDetailView, PagoSiguienteStatusView,
                           CuentaPorCobrarListView, CuentaPorCobrarCreateView,
                           CuentaPorCobrarSiguienteStatusRedirectView,
                           CuentaPorCobrarAnteriorStatusRedirectView,
                           NotificationDetailView, CotizacionDetailView,
                           CotizacionCreateView, CotizadoCreateView,
                           EstadisticasView, CotizacionFacturar,
                           ComprobanteDeduccionCreateView,
                           ComprobanteDeduccionDetailView,
                           ConceptoDeduccionCreateView, ReembolsoCreateView,
                           PagoDeleteView, AseguradoraContractsCotizarView,
                           AseguradoraMasterCotizarView, MasterCotizarView,
                           TurnoCajaPeriodoView, CotizadoUpdateView)

urlpatterns = patterns('',

                       url(r'^$',
                           IndexView.as_view(),
                           name='invoice-index'),

                       url(r'^nuevo',
                           ReciboCreateView.as_view(),
                           name='invoice-new'),

                       url(r'^(?P<persona>\d+)/crear',
                           ReciboPersonaCreateView.as_view(),
                           name='invoice-create'),

                       url(r'^examen/(?P<examen>\d+)/crear',
                           ReciboExamenCreateView.as_view(),
                           name='invoice-create-examen'),

                       url(r'^(?P<pk>\d+)$',
                           ReciboDetailView.as_view(),
                           name='invoice-view-id'),

                       url(r'^(?P<pk>\d+)/impresion$',
                           ReciboPrintView.as_view(),
                           name='invoice-print'),

                       url(r'^(?P<pk>\d+)/impresion/credito$',
                           ReciboDetailView.as_view(
                               template_name='invoice/recibo_credito.html'),
                           name='invoice-print-credito'),

                       url(r'^(?P<pk>\d+)/anular$',
                           ReciboAnularView.as_view(),
                           name='invoice-nullify'),

                       url(r'^(?P<pk>\d+)/cerrar$',
                           ReciboCerrarView.as_view(),
                           name='invoice-close'),

                       url(r'^(?P<recibo>\d+)/venta/add$',
                           VentaCreateView.as_view(),
                           name='venta-add'),

                       url(r'^venta/(?P<pk>\d+)/delete$',
                           VentaDeleteView.as_view(),
                           name='venta-delete'),

                       url(r'^pago/(?P<pk>\d+)/delete$',
                           PagoDeleteView.as_view(),
                           name='pago-delete'),

                       url(r'^periodo$',
                           ReporteReciboView.as_view(),
                           name='invoice-periodo'),

                       url(r'^estadisticas$',
                           EstadisticasView.as_view(),
                           name='invoice-estadisticas'),

                       url(r'^estadistica/periodo$',
                           EstadisticasPeriodoView.as_view(),
                           name='invoice-estadisticas-periodo'),

                       url(r'^periodo/detalle$',
                           ReporteReciboDetailView.as_view(),
                           name='invoice-periodo-detail'),

                       url(r'^periodo/tipo$',
                           ReporteTipoView.as_view(),
                           name='invoice-tipo'),

                       url(r'^periodo/producto$',
                           ReporteProductoView.as_view(),
                           name='invoice-periodo-producto'),

                       url(r'^periodo/pago$',
                           PagoPeriodoView.as_view(),
                           name='invoice-periodo-pago'),

                       url(r'^pago/list$',
                           PagoListView.as_view(),
                           name='invoice-pago-list'),

                       url(r'^pago/aseguradora/(?P<aseguradora>\d+)/list$',
                           PagoAseguradoraList.as_view(),
                           name='invoice-pago-aseguradora-list'),

                       url(r'^periodo/emergencia$',
                           EmergenciaPeriodoView.as_view(),
                           name='invoice-periodo-emergencia'),

                       url(r'^periodo/venta$',
                           VentaListView.as_view(),
                           name='periodo-venta'),

                       url(r'^periodo/tipopago$',
                           TipoPagoPeriodoView.as_view(),
                           name='periodo-tipopago'),

                       url(r'^periodo/ciudad$',
                           CiudadPeriodoListView.as_view(),
                           name='periodo-ciudad'),

                       url(r'^periodo/turno',
                           TurnoCajaPeriodoView.as_view(),
                           name='turno-periodo'),

                       url(r'^periodo/venta/area$',
                           VentaAreaListView.as_view(),
                           name='periodo-venta-area'),

                       url(r'^dia/emergencia$',
                           EmergenciaDiaView.as_view(),
                           name='invoice-dia-emergencia'),

                       url(r'^examenes$',
                           ExamenView.as_view(),
                           name='invoice-imaging'),

                       url(r'^corte$',
                           CorteView.as_view(),
                           name='invoice-corte'),

                       url(r'^inventario',
                           ReciboInventarioView.as_view(),
                           name='invoice-inventario'),

                       url(r'^dia/altas$',
                           AdmisionAltaView.as_view(),
                           name='invoice-dia-altas'),

                       url(r'^emergencia/(?P<pk>\d+)$',
                           EmergenciaFacturarView.as_view(),
                           name='emergency-invoice'),

                       url(r'^admision/(?P<pk>\d+)$',
                           AdmisionFacturarView.as_view(),
                           name='admision-invoice'),

                       url(r'^deposito/(?P<pk>\d+)$',
                           DepositoFacturarView.as_view(),
                           name='deposito-invoice'),

                       url(r'^examen/(?P<pk>\d+)$',
                           ExamenFacturarView.as_view(),
                           name='examen-invoice'),

                       url(r'^consulta/(?P<pk>\d+)$',
                           ConsultaFacturarView.as_view(),
                           name='consulta-invoice'),

                       url(r'^aseguradora/(?P<pk>\d+)$',
                           AseguradoraContractsFacturarView.as_view(),
                           name='aseguradora-invoice'),

                       url(r'^aseguradora/(?P<pk>\d+)$',
                           AseguradoraMasterFacturarView.as_view(),
                           name='aseguradora-invoice-master'),

                       url(r'^aseguradora/contratos/cotizar/(?P<pk>\d+)$',
                           AseguradoraContractsCotizarView.as_view(),
                           name='aseguradora-cotizar-contrato'),

                       url(r'^aseguradora/maestro/cotizar/(?P<pk>\d+)$',
                           AseguradoraMasterCotizarView.as_view(),
                           name='aseguradora-cotizar-master'),

                       url(r'^master/cotizar/(?P<pk>\d+)$',
                           MasterCotizarView.as_view(),
                           name='master-cotizar'),

                       url(r'^(?P<recibo>\d+)/pago/add$',
                           PagoCreateView.as_view(),
                           name='pago-add'),

                       url(r'^pago/(?P<pk>\d+)/status/edit$',
                           PagoUpdateView.as_view(),
                           name='invoice-pago-status-edit'),

                       url(r'^pago/status$',
                           StatusPagoListView.as_view(),
                           name='invoice-pago-status-index'),

                       url(r'^turno/(?P<pk>\d+)$',
                           TurnoCajaDetailView.as_view(),
                           name='invoice-turno'),

                       url(r'^turno/(?P<pk>\d+)/recibos$',
                           TurnoCajaDetailView.as_view(
                               template_name="invoice/turno_recibo_list.html"),
                           name='invoice-turno-recibos'),

                       url(r'^turno/nuevo',
                           TurnoCajaCreateView.as_view(),
                           name='invoice-turno-nuevo'),

                       url(r'^turno/(?P<turno>\d+)/cierre/nuevo$',
                           CierreTurnoCreateView.as_view(),
                           name='invoice-cierre-nuevo'),

                       url(r'^turno/(?P<pk>\d+)/update$',
                           TurnoCajaUpdateView.as_view(),
                           name='invoice-turno-edit'),

                       url(r'^deposito/(?P<pk>\d+)$',
                           DepositoDetailView.as_view(),
                           name='invoice-deposito'),

                       url(r'^turno/(?P<pk>\d+)/cerrar$',
                           TurnoCierreUpdateView.as_view(),
                           name='invoice-turno-cerrar'),

                       url(r'^turno/activos$',
                           TurnoCajaListView.as_view(),
                           name='invoice-turno-activo'),

                       url(r'^cpc$',
                           CuentaPorCobrarListView.as_view(),
                           name='invoice-cpc-list'),

                       url(r'^cpc/(?P<pk>\d+)$',
                           CuentaPorCobrarDetailView.as_view(),
                           name='invoice-cpc'),

                       url(r'^cpc/agregar$',
                           CuentaPorCobrarCreateView.as_view(),
                           name='invoice-cpc-add'),

                       url(r'^pago/(?P<pk>\d+)/status/next$',
                           PagoSiguienteStatusView.as_view(),
                           name='invoice-pago-status-next'),

                       url(r'^cpc/(?P<pk>\d+)/status/next$',
                           CuentaPorCobrarSiguienteStatusRedirectView.as_view(),
                           name='invoice-cpc-status-next'),

                       url(r'^cpc/(?P<pk>\d+)/status/previous$',
                           CuentaPorCobrarAnteriorStatusRedirectView.as_view(),
                           name='invoice-cpc-status-previous'),

                       url(r'^cpc/(?P<cuenta>\d+)/pago/next$',
                           PagoCuentaCreateView.as_view(),
                           name='invoice-cpc-pago-add'),

                       url(r'^notification/(?P<pk>\d+)$',
                           NotificationDetailView.as_view(),
                           name='notification'),

                       url(r'^cotizacion/(?P<pk>\d+)$',
                           CotizacionDetailView.as_view(),
                           name='cotizacion'),

                       url(r'^cotizacion/(?P<cotizacion>\d+)/cotizado/agregar$',
                           CotizadoCreateView.as_view(),
                           name='cotizado-add'),

                       url(r'^(?P<persona>\d+)/cotizacion/agregar$',
                           CotizacionCreateView.as_view(),
                           name='cotizacion-add'),

                       url(r'^cotizado/(?P<pk>\d+)/delete$',
                           CotizadoDeleteView.as_view(),
                           name='cotizado-delete'),

                       url(r'^cotizado/(?P<pk>\d+)/editar$',
                           CotizadoUpdateView.as_view(),
                           name='cotizado-edit'),

                       url(r'^cotizacion/(?P<pk>\d+)/facturar$',
                           CotizacionFacturar.as_view(),
                           name='cotizacion-facturar'),

                       url(r'^comprobante/agregar$',
                           ComprobanteDeduccionCreateView.as_view(),
                           name='comprobante-agregar'),

                       url(r'^comprobante/(?P<pk>\d+)$',
                           ComprobanteDeduccionDetailView.as_view(),
                           name='comprobante'),

                       url(r'^comprobante/(?P<pk>\d+)/imprimir$',
                           ComprobanteDeduccionDetailView.as_view(
                               template_name='invoice/comprobantededuccion_print.html'
                           ),
                           name='comprobante-print'),

                       url(r'^comprobante/(?P<comprobante>\d+)/concepto/add$',
                           ConceptoDeduccionCreateView.as_view(),
                           name='concepto-agregar'),

                       url(r'^reembolso/agregar$',
                           ReembolsoCreateView.as_view(),
                           name='reembolso-add'),

                       )
