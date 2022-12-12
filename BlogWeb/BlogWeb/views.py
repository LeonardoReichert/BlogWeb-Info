
from django.shortcuts import render;




def inicio(request):

    #parametros a la web template
    contexto = {};

    return render(request, "inicio.html", contexto);


"""
def login(request):
    contexto = {};
    email = request.POST.get("email", None)
    password = request.POST.get("password", None)
    return render(request, "login.html", contexto)
"""










