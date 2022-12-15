
from django.shortcuts import render, redirect;
from noticias.models import *
from django.urls import reverse

from noticias.models import *;


#from django.conf import settings
#from django.core.files.storage import FileSystemStorage



def inicio(request):


    # - juntar info de noticias -

    totalNoticias = Noticia.objects.count();

    print("cantidad noticias: ", totalNoticias)


    #parametros a la web template
    contexto = {};


    return render(request, "inicio.html", contexto);


def registro(request):

    #parametros a la web template
    contexto = {};

    return render(request, "registro.html", contexto);


"""
def login(request):
    contexto = {};
    email = request.POST.get("email", None)
    password = request.POST.get("password", None)
    return render(request, "login.html", contexto)
"""










