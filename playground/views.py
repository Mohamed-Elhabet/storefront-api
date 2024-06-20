from django.shortcuts import render
import requests
from django.core.cache import cache
from django.views.decorators.cache import cache_page 
from rest_framework.views import APIView
from django.utils.decorators import method_decorator
import logging

# Create your views here.

logger = logging.getLogger(__name__)

class HelloWorld(APIView):
    @method_decorator(cache_page(5*60))
    def get(self, request):
        try:
            logger.info('Calling httpbin')
            response = requests.get('https://httpbin.org/delay/2')
            logger.info('Received the response')
            data = response.json()
        except requests.ConnectionError:
            logger.critical('httpbin is offline')
            data = None
        return render(request, 'hello.html', {'name': data})
    
    
    
# @cache_page(5*60)
# def say_hello(request):
#     response = requests.get('https://httpbin.org/delay/2')
#     data = response.json()
        
#     return render(request, 'hello.html',
#                   {'name': data} 
#                   )
    
    