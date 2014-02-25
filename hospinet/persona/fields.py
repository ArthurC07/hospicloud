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

from django_countries.fields import CountryField
from django_countries.data import COUNTRIES
from django.db.models.fields import CharField
from south.modelsinspector import add_introspection_rules


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
                pass  #right now choices is sorted by code already
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


add_introspection_rules([
                            (
                                [OrderedCountryField],
                                # Class(es) these apply to
                                [],  # Positional arguments (not used)
                                {  # Keyword argument
                                   #"ordered": ["ordered", {}],
                                   #"sort": ["sort", {}],
                                },
                            ),
                        ], ["^persona\.fields\.OrderedCountryField"])
