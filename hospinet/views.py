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

from django.views.generic.base import TemplateView
from userena.forms import AuthenticationForm
from users.mixins import LoginRequiredMixin


class IndexView(TemplateView):
    
    template_name = 'index.html'

    def get_context_data(self, **kwargs):

        context = super(IndexView, self).get_context_data(**kwargs)

        context['form'] = AuthenticationForm()

        return context
