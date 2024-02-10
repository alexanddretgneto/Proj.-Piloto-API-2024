from django.shortcuts import render

# Create your views here. 
# Esta é a visão mais simples possível no Django.
# Para chamar a view, precisamos mapeá-la para uma URL - e para isso precisamos de um URLconf.

# Para criar um URLconf no diretório polls, 
# crie um arquivo chamado urls.py.
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

