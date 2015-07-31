from django.contrib import admin

from budget.models import Presupuesto, Cuenta, Gasto


class PresupuestoAdmin(admin.ModelAdmin):
    list_display = ('ciudad', 'created')
    ordering = ('ciudad', 'created')
    search_fields = ['ciudad', ]


class CuentaAdmin(admin.ModelAdmin):
    list_display = ['get_ciudad', 'presupuesto', 'nombre', 'limite']
    ordering = ['presupuesto', 'nombre', 'limite']

    def get_ciudad(self, obj):
        return obj.presupuesto.ciudad

    get_ciudad.short_description = 'Ciudad'
    get_ciudad.admin_order_field = 'presupuesto__ciudad'


class GastoAdmin(admin.ModelAdmin):
    list_display = ['descripcion', 'proveedor', 'cuenta', 'get_presupuesto',
                    'monto', 'ejecutado', 'fecha_maxima_de_pago']
    ordering = ['descripcion', 'monto']

    def get_ciudad(self, obj):
        return obj.cuenta.presupuesto.ciudad

    def get_presupuesto(self, obj):
        return obj.cuenta.presupuesto

    get_ciudad.short_description = 'Ciudad'
    get_ciudad.admin_order_field = 'cuenta__presupuesto__ciudad'

    get_presupuesto.short_description = 'Presupuesto'
    get_presupuesto.admin_order_field = 'cuenta__presupuesto'


admin.site.register(Presupuesto, PresupuestoAdmin)
admin.site.register(Cuenta, CuentaAdmin)
admin.site.register(Gasto, GastoAdmin)
