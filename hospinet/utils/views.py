# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from django.views.generic.edit import FormMixin
from hospinet.utils.forms import PeriodoForm


class PeriodoView(FormMixin):
    """
    Allows basic handling of a :class:`PeriodoForm` making its beginning and
    end date available for later usage as the inicio and fin class members.
    """
    form_class = PeriodoForm
    prefix = 'periodo'
    redirect_on_invalid = 'home'

    def dispatch(self, request, *args, **kwargs):
        """Efectua la consulta de los :class:`Recibo` de acuerdo a los
        datos ingresados en el formulario"""

        self.form = self.get_form_class()(request.GET, prefix=self.prefix)

        if self.form.is_valid():
            self.inicio = self.form.cleaned_data['inicio']
            self.fin = self.form.cleaned_data['fin']
        else:
            messages.info(
                self.request,
                _('Los Datos Ingresados en el formulario no son validos')
            )
            return HttpResponseRedirect(reverse(self.redirect_on_invalid))

        return super(PeriodoView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Adds the beginning and end date to the template context
        """

        context = super(PeriodoView, self).get_context_data(**kwargs)
        context['inicio'] = self.inicio
        context['fin'] = self.fin

        return context
