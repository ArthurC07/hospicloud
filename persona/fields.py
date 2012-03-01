# -*- coding: utf-8 -*-

from django_countries.fields import CountryField
from django_countries.countries import COUNTRIES
from django.db.models.fields import CharField
from south.modelsinspector import add_introspection_rules

class OrderedCountryField(CountryField):
    
    def __init__(self, *args, **kwargs):
        
        choices = COUNTRIES
        ordered = kwargs.pop('ordered', None)
        sort = kwargs.pop('sort', None)
        if sort:
            from operator import itemgetter
            if sort == 'Name':
                choices = sorted(choices, key=itemgetter(1))
            else:
                pass #right now choices is sorted by code already
        if ordered:
            choices_in_ordered = {}
            ordered_choices = []
            other_choices = []
            for k, v in choices:
                if k in ordered:
                    choices_in_ordered[k] = v
                else:
                    other_choices.append((k, v))
            for o in ordered:
                ordered_choices.append((o, choices_in_ordered[o]))
            choices = tuple(ordered_choices + other_choices)
        
        kwargs.setdefault('max_length', 2) 
        kwargs.setdefault('choices', choices) 

        super(CharField, self).__init__(*args, **kwargs)

add_introspection_rules([
    (
        [OrderedCountryField], # Class(es) these apply to
        [],         # Positional arguments (not used)
        {           # Keyword argument
            #"ordered": ["ordered", {}],
            #"sort": ["sort", {}],
        },
    ),
], ["^persona\.fields\.OrderedCountryField"])
