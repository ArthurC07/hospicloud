# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django_extensions.models import TimeStampedModel

class Recibo(TimeStampedModel):

    """Permite registrar pagos por productos y servicios"""

    cliente = models.CharField(max_length=255)

class Producto(TimeStampedModel):

    """Describe los diversos productos y servicios que son serán vendidos
    por la empresa"""

    cajero = models.ForeignKey(User, related_name='recibos')
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    precio = models.DecimalField(decimal_places=2, max_digits=10)
    impuesto = models.DecimalField(decimal_places=2, max_digits=4)

class Venta(TimeStampedModel):

    """Relaciona :class:`Producto` a un :class:`Recibo` lo cual permite
    realizar los cobros asociados"""

    cantidad = models.IntegerField()
    descripcion = models.TextField()
    producto = models.ForeignKey(Producto, related_name='ventas')
    recibo = models.ForeignKey(Recibo, related_name='ventas')

    def monto(self):

        """Obtiene el valor a pagar por esta :class:`Venta`"""

        return self.producto.precio * self.cantidad

    def tax(self):

        """Obtiene los impuestos a pagar por esta :class:`Venta`"""

        return self.producto.precio * self.cantidad * self.producto.impuesto
