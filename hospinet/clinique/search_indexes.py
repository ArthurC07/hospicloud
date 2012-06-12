# -*- coding: utf-8 -*-
from haystack import indexes
from clinique.models import Paciente

class PacienteIndex(indexes.SearchIndex, indexes.Indexable):
    
    text = indexes.CharField(document=True, use_template=True)
    
    def get_model(self):
        
        return Paciente
