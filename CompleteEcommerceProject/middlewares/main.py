from django.shortcuts import render,HttpResponseRedirect,redirect,HttpResponse
class ExampleMiddleware:
    def __init__(self,get_response)->None:
        self.get_response=get_response

    def __call__(self, request ,*args, **kwargs):
        print('middleware called')
        paths=['/','/products/']
        #excluded_paths = ['/login/', '/signup/']
        print('the value is ',request.get_full_path())
        if request.path in paths:
            # Store the previous URL in the session
            
            request.session['previous_url'] = request.path
        response=self.get_response(request)
        return response
    # middleware.py
from django.urls import resolve
