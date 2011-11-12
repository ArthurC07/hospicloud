# -*- coding: utf-8 -*-

import cStringIO
from django.core.files.base import ContentFile

def image_to_content(imagen):
    
    temporal = cStringIO.StringIO()
    imagen.save(temporal, 'jpeg')
    temporal.seek(0)
    return ContentFile(temporal.read())
