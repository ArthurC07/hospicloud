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

from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User
from django_extensions.db.models import TimeStampedModel
from decimal import Decimal
from persona.models import Persona

class Recibo(TimeStampedModel):

    """Permite registrar pagos por productos y servicios"""

    cliente = models.ForeignKey(Persona, related_name='recibos')
    cerrado = models.BooleanField(default=False)
    nulo = models.BooleanField(default=False)
    cajero = models.ForeignKey(User, related_name='recibos')

    def get_absolute_url(self):
        
        """Obtiene la URL absoluta"""
        
        return reverse('invoice-view-id', args=[self.id])

    def anular(self):

        """Anula el :class:`Recibo` para que no se tome en cuenta en los
        calculos financieros"""

        self.nulo = True
        self.save()

    def __unicode__(self):

        """Crea una representación en texto del :class:`Recibo`"""

        if self.nulo:
            return u'{0} **NULO**'.format(self.cliente.nombre_completo())
        
        return self.cliente.nombre_completo()

    def subtotal(self):

        """Calcula el monto antes de impuestos"""

        return sum(v.monto() for v in self.ventas.all())

    def impuesto(self):

        """Calcula los impuestos que se deben pagar por este :class:`Recibo`"""

        return Decimal(sum(v.tax() for v in self.ventas.all()))

    def total(self):

        """Calcula el monto que será mostrado en los cálculos financieros"""

        if self.nulo:
            return Decimal(0)

        return Decimal(sum(v.total() for v in self.ventas.all())).quantize(Decimal('0.01'))

class Producto(TimeStampedModel):

    """Describe los diversos productos y servicios que son serán vendidos
    por la empresa"""
    
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(decimal_places=2, max_digits=10)
    impuesto = models.DecimalField(decimal_places=2, max_digits=4)

    def __unicode__(self):
        
        """Crea una representación en texto del producto"""

        return self.nombre

class Venta(TimeStampedModel):

    """Relaciona :class:`Producto` a un :class:`Recibo` lo cual permite
    realizar los cobros asociados"""

    cantidad = models.IntegerField()
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(blank=True, null=True, max_digits=7,
                                 decimal_places=2)
    impuesto = models.DecimalField(blank=True, null=True, max_digits=7,
                                   decimal_places=2)
    producto = models.ForeignKey(Producto, related_name='ventas')
    recibo = models.ForeignKey(Recibo, related_name='ventas')

    def get_absolute_url(self):
        
        """Obtiene la URL absoluta"""
        
        return reverse('invoice-view-id', args=[self.recibo.id])

    def monto(self):

        """Obtiene el valor a pagar por esta :class:`Venta`"""

        return Decimal(self.precio * self.cantidad)

    def tax(self):

        """Obtiene los impuestos a pagar por esta :class:`Venta`"""

        return self.precio * self.cantidad * self.producto.impuesto

    def total(self):

        """Calcula el valor total de esta :class:`Venta`"""

        return self.tax() + self.monto()
