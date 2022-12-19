
from django.shortcuts import render, redirect;
from noticias.models import *
from django.urls import reverse

from noticias.models import *;


#from django.conf import settings
#from django.core.files.storage import FileSystemStorage


def inicio(request):

    # - juntar info de noticias -

#    totalNoticias = Noticia.objects.count();
#    print("cantidad noticias: ", totalNoticias)

    noticiasVisibles = [];

    count = 0;
    SHOW_MAX = 5; #noticias
    DESC_MAX = 200;
    
    for noticia in Noticia.objects.all().order_by("-fecha"):
        parte = NoticiaParte.objects.get(noticia=noticia);

        idNoticia = noticia.id;
        urlImg = parte.urlImagen;
        titulo = noticia.titulo;
        fecha = horaUtcToArg(noticia.fecha);
        if noticia.categoria:
            categoria = noticia.categoria.nombre;
        else:
            #probablemente la categoria fue eliminada
            categoria = "Sin categoria";

        descripcionCorta = parte.mensaje.strip()[:DESC_MAX].replace("\n\n", "\n");

        noticiasVisibles.append( (idNoticia, titulo, fecha, urlImg,
                                    categoria, descripcionCorta) );

        count += 1;
        if count >= SHOW_MAX:
            break;

    #parametros a la web template
    contexto = {"noticiasVisibles": noticiasVisibles};

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










