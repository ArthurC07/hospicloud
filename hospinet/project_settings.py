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

# Django settings for hospicloud project.

CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'
CONSTANCE_CONFIG = {
    'EMERGENCIA': (1, u'Cuenta utilizada para estadia en emergencias'),
    'DEPOSIT_ACCOUNT': (1, u'Cuenta utilizada para disminuir depositos'),
    'EXTRA_EMERGENCIA': (1, u'Cuenta utilizada para agregar tiempo extra de emergencias'),
    'DEPOSIT_PAYMENT': (1, u'Tipo de Pago para Abonos a cuenta'),
    'CHAT': (u'http://www.example.com', u'Url para el chat interno'),
    'ONLINE_HELP': (u'http://www.example.com', u'Url para ayuda en línea'),
    'DEFAULT_VENTA_TYPE': (1, u'Tipo de Venta Predeterminada'),
    'DEFAULT_CONSULTA_ITEM': (1, u'Costo de Consulta'),
    'NIGHT_CONSULTA_ITEM': (1, u'Costo de Consulta Nocturna'),
    'ELDER_VENTA_TYPE': (1, u'Tipo de Venta Predeterminada'),
    'ELDER_AGE': (60, u'Edad mínima de la Tercera Edad'),
    'RECEIPT_DAYS': (1, u'Dias que dura una factura al credito'),
    'CURRENCY_EXCHANGE': (22.03, u'Cambio de Moneda'),
    'PAYMENT_TYPE_PENDING': (1, u'Tipo de Pago Pendiente'),
    'PAYMENT_STATUS_PENDING': (1, u'Estado de Pago Pendiente'),
}

USERENA_ACTIVATION_REQUIRED = False
AUTH_PROFILE_MODULE = 'users.UserProfile'
