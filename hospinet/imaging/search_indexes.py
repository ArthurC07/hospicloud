# -*- coding: utf-8 -*-
from haystack import indexes
from imaging.models import Examen

class ExamenIndex(indexes.SearchIndex, indexes.Indexable):
    
    """Permite buscar en los examenes utilizando Haystack"""

    text = indexes.CharField(document=True, use_template=True)
    
    def get_model(self):
        
        return Examen
