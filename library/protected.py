# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import View

class LoginRequiredView(View):
    
    """Clase base para crear vistas que requieren inicio de sesión"""
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        
        """Permite despachar la petición en caso que el usuario tenga iniciada
        su sesión en la aplicación"""
        
        return super(LoginRequiredView, self).dispatch(request, *args, **kwargs)
