
from django.shortcuts import render;




def inicio(request):

    #parametros a la web template
    contexto = {};

    return render(request, "inicio.html", contexto);

