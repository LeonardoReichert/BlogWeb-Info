
from django.shortcuts import render, redirect;
from noticias.models import *
from django.urls import reverse



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


def verNoticia(request):

    idNoticia = request.GET.get("id", None);
    try:
        noticia = Noticia.objects.get(pk=idNoticia);
    except:
        noticia = None;
    
    contexto = {}

    if noticia:
        contexto["noticiaTitulo"] = noticia.titulo;
        contexto["noticiaCategoria"] = noticia.categoria;

        partes = NoticiaParte.objects.filter(noticia=noticia);
        
        #por ahora las noticias se limitaran a un solo cuerpo o parte
        contexto["cuerpoNoticia"] = partes[0].mensaje;
    else:
        return redirect( inicio );

    return render(request, "noticia.html", contexto);


def crearNoticia(request):
    """ Crea o modifica noticia """

    if not request.user.esAdmin:
        #no tendria los permisos
        return redirect(inicio);

    idPostNoticia = request.POST.get("modnoticia", "");
    tituloPost = request.POST.get("titulo_noticia", "");

    idGetNoticia = request.GET.get("modnoticia", "");

    if tituloPost:
        #Peticion con metodo POST
        #se crea o modifica una noticia:

        #si sobra tiempo se agregaran mas partes a la noticia
        mensajePost1 = request.POST.get("body_part1", "");
        if not mensajePost1:
            #dar error, el cuerpo de la noticia esta vacio
            return redirect( inicio );

        imgPost1 = request.POST.get("img_part1", "");
        #if not imgPost1:
        # futuramente los posts deberan tener almenos 1 imagen

        #tanto en la creacion como en la modificacion se puede crear una categoria
        idCategoria = request.POST.get("categoria", "");
        categoria = None;
        if idCategoria == "+":
            #se eligio crear la categoria
            nombreNuevaCategoria = request.POST.get("nueva_categoria", "");
            #categoria = None
            if nombreNuevaCategoria:
                #categoria son valores unicos, si no existe se crea
                categoria, created = Categorias.objects.get_or_create(nombre=nombreNuevaCategoria)
        else:
            try:
                categoria = Categorias.objects.get(id=idCategoria);
            except:
                #error al obtener categoria
                pass

        if not categoria:
            #dar error, no se creo una categoria
            return redirect( inicio );



        if not idPostNoticia:
            #se crea, no se especifica el ID
            noticia = Noticia.objects.create(titulo=tituloPost,
                                             autor=request.user,
                                             categoria=categoria);
            
            NoticiaParte.objects.create(noticia=noticia, mensaje=mensajePost1, urlImagen=imgPost1)

            idPostNoticia = noticia.id;
        else:
            #se modifica porque se especifica el ID en al peticion POST
            pass
            
        print("post", request.POST)

        
        return redirect("/noticia/?id="+str(idPostNoticia))

    elif idGetNoticia:
        #Peticion con metodo GET
        #pedido de entrar a modificar la noticia
        #se recupera y carga los campos de la notica:
        try:
            noticia = Noticia.objects.get(pk=idGetNoticia);

            tituloNoticia = noticia.titulo;
            categoria = noticia.categoria;

            partes = NoticiaParte.objects.filter(noticia=noticia);

            #por ahora las noticias se limitaran a un solo cuerpo o parte
            cuerpoNoticia = partes[0].mensaje;
        except:
            #si algun campo falla se reinician todos
            idGetNoticia = ""
        
    if not idGetNoticia:
        tituloNoticia = ""
        cuerpoNoticia = ""
        categoria = ""
        idNoticia = ""

    categoriasExistentes = Categorias.objects.all()
    
    #parametros a la web template
    contexto = {"modnoticia": idGetNoticia,
                "oldTitulo": tituloNoticia,
                "oldCuerpoNoticia": cuerpoNoticia,
                "oldCategoria": categoria,
                "categoriasExistentes": categoriasExistentes,
                };

    return render(request, "crearnoticia.html", contexto);




"""
def login(request):
    contexto = {};
    email = request.POST.get("email", None)
    password = request.POST.get("password", None)
    return render(request, "login.html", contexto)
"""










