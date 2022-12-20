from django.shortcuts import render

# Create your views here.




def informeAcercaDe(request):

    contexto = {};

    return render(request, "informacion.html", contexto);


def informeContacto(request):

    contexto = {};

    return render(request, "contacto.html", contexto);

