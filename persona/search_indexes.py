# -*- coding: utf-8 -*-
from haystack import indexes
from persona.models import Persona

class PersonaIndex(indexes.SearchIndex, indexes.Indexable):
    
    text = indexes.CharField(document=True, use_template=True)
    
    def get_model(self):
        
        return Persona
