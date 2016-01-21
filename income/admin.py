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
from django.contrib import admin

# Register your models here.
from income.models import Deposito, Cheque, Banco, DetallePago, TipoDeposito, \
    TipoCheque


class TipoDepositoAdmin(admin.ModelAdmin):
    """
    Describes the interface to manage :class:`TipoDeposito`s in the Django
    administrative interface
    """
    list_display = ['nombre']


class BancoAdmin(admin.ModelAdmin):
    """
    Describes the interface to manage :class:`Banco`s in the Django
    administrative interface
    """
    list_display = ['nombre']


class DepositoAdmin(admin.ModelAdmin):
    """
    Describes the interface to manage :class:`Deposito`s in the Django
    administrative interface
    """
    list_display = ['tipo', 'cuenta', 'monto', 'fecha_de_deposito']
    ordering = ['monto', 'cuenta__nombre', 'tipo__nombre']


class TipoChequeAdmin(admin.ModelAdmin):
    """
    Describes the interface to manage :class:`TipoCheque`s in the Django
    administrative interface
    """
    list_display = ['nombre']


class ChequeAdmin(admin.ModelAdmin):
    """
    Describes the interface to manage :class:`Cheque`s in the Django
    administrative interface
    """
    list_display = ['banco_de_emision', 'numero_de_cheque', 'monto',
                    'monto_retenido', 'tipo']
    search_fields = ['banco_de_emision__nombre', 'numero_de_cheque']
    exclude = ('emisor', )


class DetallePagoAdmin(admin.ModelAdmin):
    """
    Describes the interface to manage :class:`DetallePago`s in the Django
    administrative interface
    """
    list_display = ['cheque', 'pago', 'monto']


admin.site.register(TipoDeposito, TipoDepositoAdmin)
admin.site.register(Deposito, DepositoAdmin)
admin.site.register(TipoCheque, TipoChequeAdmin)
admin.site.register(Cheque, ChequeAdmin)
admin.site.register(Banco, BancoAdmin)
admin.site.register(DetallePago, DetallePagoAdmin)
