# -*- coding: utf-8 -*-
from django.contrib import admin
from invoice.models import (Recibo, Producto, Venta)

admin.site.register(Recibo)
admin.site.register(Producto)
admin.site.register(Venta)
