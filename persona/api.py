# -*- coding: utf-8 -*-
from django.conf.urls.defaults import url
from django.core.paginator import Paginator, InvalidPage
from django.http import Http404
from haystack.query import SearchQuerySet
from persona.models import Persona
from tastypie.resources import ModelResource
from tastypie.utils.urls import trailing_slash
from django.forms.models import model_to_dict

class PersonaResource(ModelResource):
    
    class Meta:
        
        queryset = Persona.objects.all()
        resource_name = 'persona'
    
    def override_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/search%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_search'), name="api_get_search"),
        ]

    def get_search(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)

        # Do the query.
        sqs = SearchQuerySet().models(Persona).load_all().auto_query(request.GET.get('q', ''))
        paginator = Paginator(sqs, 20)

        try:
            page = paginator.page(int(request.GET.get('page', 1)))
        except InvalidPage:
            raise Http404("Sorry, no results on that page.")

        objects = []

        for result in page.object_list:
            # Lo siguiente es un hack para que Haystack 2.0 alpha y tastypie 1.0beta
            # funcionen adecuadamente
            bundle = self.build_bundle(obj=result.object, data=model_to_dict(result.object))
            bundle.pk = result.object.id
            # bundle = self.full_dehydrate(bundle)
            objects.append(bundle)
        
        object_list = {
            'objects': objects,
        }

        self.log_throttled_access(request)
        return self.create_response(request, object_list)
