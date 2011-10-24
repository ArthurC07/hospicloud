# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.core import serializers
from django.views.generic.base import TemplateResponseMixin
from django.http import Http404
from django.core.exceptions import ImproperlyConfigured

class MultiFormatResponseMixin(TemplateResponseMixin):
    """
    Render http response in in either in HTML (default), HTML snippet or any
    serializer that is supported format.  The rendering output is determined by
    ``output`` request GET variable  as follows:
    
    ``?output=serialzier_<serializer_name> OR <html> OR <inc.html>``
    OPTIONAL: defaults to html 
    
    <serializer_name> part of the GET variable is passed to the Django
    serializer frame with additional ``serializer_options`` defined on your
    custom class views. Hence if one has added additional serializers they are
    fully supported.
    
    If <serializer_name> dosen't exist or output serializer format is not
    supported or serializer_options are missing a 404 response is generated.
     
    To use simple define your class based view as follows and based on
    ?output=<value> different format is returned:
    
    ```
    class AdCategoryListView(MultiFormatResponseMixin, ListView):
    
    context_object_name="adcategories_list"
    serializer_options = {
                    'json': {
                            'fields': ['locations'],
                            'extras': ['get_firstmedia_url']
                            },
                    'geojson': {
                            'fields': ['locations'],   
                            }
                    }
    
    def get_queryset(self):
        return AdCategory.objects.filter(parent_category__isnull = True) 
    
    ...
    ...
    
    ```
    
    Template naming convention for different outputs:
    
    ```?output=serialzier_json``` = NO TEMPLATE - response is output of calling json serialzier on the query
    ```?output=serialzier_foobar``` = NO TEMPLATE - response is output of calling foobar serialzier on the query
                            
                            
    ```?output=html``` = <templates>/<app_label>/<model name><template_name_suffix>.html
    ```?output=inc.html``` = <templates>/<app_label>/<model name><template_name_suffix>.inc.html
    
    Suggested aditional serialziers: 
        GEOJSON - http://djangosnippets.org/snippets/2434/)
        DjangoFullSerializers http://code.google.com/p/wadofstuff/wiki/DjangoFullSerializers 
    
    """
    def render_to_response(self, context):
        # Look for a 'format=<foo>' GET argument if dosen't exist then do normal
        # html Template Response mixin response
        if self.request.GET.get('output','html') == 'html':
            # call original ListView.render_to_response()
            return super(MultiFormatResponseMixin,
                         self).render_to_response(context)
        
        elif self.request.GET.get('output','') == 'inc.html':
            opts = self.get_queryset().model._meta
            self.template_name = "{0}/{1}{2}.inc.djhtml".format(
                                                      opts.app_label,
                                                      opts.object_name.lower(),
                                                      self.template_name_suffix)
            # call original ListView.render_to_response()
            return super(MultiFormatResponseMixin,
                         self).render_to_response(context)
        
        output = self.request.GET.get('output')
        if not 'serializer_' in output:
            raise Http404
        
        # Check we are configured properly first - we do the check here so that
        # adding this mixin dosen't prevent original view logic from executing 
        if not hasattr(self, 'serializer_options'):
            raise ImproperlyConfigured(
                    u"'{0}' must define 'serializer_options'".format(
                                                    self.__class__.__name__)
        )

        serializer = output.split('_')[1] # grap serialzier name

        # if serialzier is not supported or it's options not specified in
        # view's serializer_options raise 404
        if not serializer in serializers.get_serializer_formats() \
            or serializer not in self.serializer_options:
            raise Http404
            
        output = self.request.GET.get('output','')
        query = self.get_queryset()
        
        # if get_object attribute exists than we should filter to that object
        # only
        if hasattr(self, 'get_object'):
            query = query.filter(pk=self.get_object().pk)
        
        content = serializers.serialize(serializer, query,
                                        **self.serializer_options[serializer])
        #return HttpResponse(content, content_type='application/%s' % serializer)
        return HttpResponse(content)
