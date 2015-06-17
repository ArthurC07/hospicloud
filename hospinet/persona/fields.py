# -*- coding: utf-8 -*-
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

import re

from django_countries.fields import CountryField
from django_countries.data import COUNTRIES
from django.db import models
from django.core.validators import RegexValidator
from django.forms import TextInput
from django.utils.translation import ugettext_lazy as _


class OrderedCountryField(CountryField):
    """Permite mostrar algunos códigos de país antes que el resto"""

    def __init__(self, *args, **kwargs):

        choices = COUNTRIES
        ordered = kwargs.pop('ordered', None)
        sort = kwargs.pop('sort', None)
        if sort:
            from operator import itemgetter

            if sort == 'Name':
                choices = sorted(choices, key=itemgetter(1))
            else:
                pass  # right now choices is sorted by code already
        if ordered:
            choices_in_ordered = {}
            ordered_choices = []
            other_choices = []
            for code in choices:
                if code in ordered:
                    choices_in_ordered[code] = choices[code]
                else:
                    other_choices.append((code, choices[code]))
            for o in ordered:
                ordered_choices.append((o, choices_in_ordered[o]))
            choices = tuple(ordered_choices + other_choices)

        kwargs.setdefault('max_length', 2)
        kwargs.setdefault('choices', choices)

        super(OrderedCountryField, self).__init__(*args, **kwargs)


color_re = re.compile('^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$')
validate_color = RegexValidator(color_re, _(u'Enter a valid hex color.'),
                                'invalid')


class ColorInput(TextInput):
    input_type = 'color'


class ColorField(models.CharField):
    default_validators = [validate_color]

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 10
        super(ColorField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        kwargs['widget'] = ColorInput
        return super(ColorField, self).formfield(**kwargs)
