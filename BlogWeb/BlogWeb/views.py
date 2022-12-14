
from django.shortcuts import render;
from noticias.models import *



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


def crearNoticia(request):

    idNoticia = request.GET.get("modnoticia", None);
    #if idNoticia:

    #print("solicitud de modificar noticia: ", idNoticia)

    try:
        noticia = Noticia.objects.get(pk=int(idNoticia));

        tituloNoticia = noticia.titulo;
        categoria = noticia.categoria;

        partes = NoticiaParte.objects.filter(noticia=noticia);

        #por ahora las noticias se limitaran a un solo cuerpo o parte
        cuerpoNoticia = partes[0].mensaje;

    except:
        tituloNoticia = ""
        cuerpoNoticia = ""
        categoria = None
        idNoticia = None

    categoriasExistentes = Categorias.objects.all()
    
    #parametros a la web template
    contexto = {"modnoticia": idNoticia,
                "oldTitulo": tituloNoticia,
                "oldCuerpoNoticia": cuerpoNoticia,
                "oldCategoria": categoria,
                "categoriasExistentes": categoriasExistentes,
                };

    #print(contexto)
    
    return render(request, "crearnoticia.html", contexto);




"""
def login(request):
    contexto = {};
    email = request.POST.get("email", None)
    password = request.POST.get("password", None)
    return render(request, "login.html", contexto)
"""










