
from django.shortcuts import render, redirect;
from noticias.models import *
from django.urls import reverse

from django.http import HttpResponseRedirect


#from django.conf import settings
from django.core.files.storage import FileSystemStorage

from os.path import splitext, exists;
from os import remove as removeFile

# Create your views here.

#para subir la imagen:
fstorage = FileSystemStorage();



def publicarComentario(request):

    noticia = Noticia.objects.get(id=request.POST["idNoticiaComentario"])
    
    msgComentario = request.POST["msgComentario"];
    comentario = Comentario.objects.create(noticia=noticia,
                                            autor=request.user,
                                            mensaje=msgComentario);
    comentario.save()


    

def verNoticia(request):


    if "idNoticiaComentario" in request.POST and "msgComentario" in request.POST:
        publicarComentario(request);
        #el usuario uso post para dejar un comentario en la noticia
        return redirect("/noticia/?id="+str(request.POST["idNoticiaComentario"]))


    
    idNoticia = request.GET.get("id", None);
    try:
        noticia = Noticia.objects.get(pk=idNoticia);
    except:
        noticia = None;
    
    contexto = {}
    
    if noticia:
        contexto["idNoticia"] = noticia.id;
        contexto["noticiaTitulo"] = noticia.titulo;
        contexto["noticiaCategoria"] = noticia.categoria;

        partes = NoticiaParte.objects.filter(noticia=noticia);
        
        #por ahora las noticias se limitaran a un solo cuerpo o parte
        contexto["imgNoticia"] = partes[0].urlImagen;
        contexto["cuerpoNoticia"] = partes[0].mensaje;

        contexto["comentarios"] = [
            (c.autor,
            c.fecha.strftime("%Y-%m-%d %H:%M"),
            c.mensaje)  for c in Comentario.objects.filter(noticia=noticia)]
    else:
        return redirect( "inicio" );

    return render(request, "noticia.html", contexto);



def crearNoticia(request):
    """ Crea o modifica  o borra noticia """

    #Categorias.objects.get(id=6).delete()

    if not hasattr(request.user, "esAdmin") or not request.user.esAdmin:
        #si no es admin, no tendria los permisos para usar esta funcion
        return redirect("inicio");

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
            return redirect( "inicio" );
        
        mensajePost1 = mensajePost1[:Limits.mensajeNoticia];

        #tanto en la creacion como en la modificacion se puede crear una categoria
        idCategoria = request.POST.get("categoria", "");
        categoria = None;

        if not idCategoria:
            #no se selecciono ninguna categoria, error
            return redirect( "inicio" );

        elif idCategoria == "+":
            #se eligio crear la categoria
            nombreNuevaCategoria = request.POST.get("nueva_categoria", "");
            #categoria = None
            if nombreNuevaCategoria:
                #categoria son valores unicos, si no existe se crea
                categoria, created = Categorias.objects.get_or_create(
                                        nombre=nombreNuevaCategoria[:Limits.categoriaNombre]);
        else:
            try:
                categoria = Categorias.objects.get(id=idCategoria);
            except:
                #error al obtener categoria
                pass

        if not categoria:
            #dar error, no se creo una categoria
            return redirect( "inicio" );

        tituloPost = tituloPost[:Limits.tituloNoticia]; #200 length max

        imgPost1 = "";
        img1 = request.FILES.get("img1", "");
        if img1 :
            filename = fstorage.save("n"+splitext(img1.name)[1], img1);
            imgPost1 = fstorage.url(filename);
            

        if not idPostNoticia:
            #no se especifica el ID, se crea nueva noticia

            if not imgPost1:
                #dar error, no se puso imagen en una nueva noticia
                return redirect( "inicio" );

            noticia = Noticia.objects.create(titulo=tituloPost,
                                             autor=request.user,
                                             categoria=categoria);
            
            NoticiaParte.objects.create(noticia=noticia, mensaje=mensajePost1, urlImagen=imgPost1);

            idPostNoticia = noticia.id;
        else:
            #se especifica el ID en al peticion POST, se modifica
            noticia = Noticia.objects.get(id=idPostNoticia);
            noticia.titulo = tituloPost;
            noticia.categoria = categoria;

            parte1 = NoticiaParte.objects.get(noticia = noticia);
            
            parte1.mensaje = mensajePost1;
            if imgPost1:
                #se cambia de imagen porque se eligio otra imagen
                
                oldPathImg = parte1.urlImagen.removeprefix("/");
                if exists(oldPathImg):
                    #se intenta borrar la antigua imagen, para no ocupar espacio ya que no se ocupara mas
                    try:
                        removeFile(oldPathImg);
                    except:
                        pass;

                parte1.urlImagen = imgPost1;
                
            parte1.save();
            noticia.save();

        #print("post", request.POST)        
        return redirect("/noticia/?id="+str(idPostNoticia))

    elif idGetNoticia:
        #Peticion con metodo GET
        #pedido de entrar a modificar la noticia
        #se recupera y carga los campos de la notica:
        
        try:
            noticia = Noticia.objects.get(pk=idGetNoticia);

            #se pidio borrar la noticia?
            if request.GET.get("delete", "") == "yes":
                #pues se borra y se redirecciona al inicio:
                pathImg = NoticiaParte.objects.get(noticia=noticia).urlImagen.removeprefix("/");
                if exists(pathImg):
                    try:
                        removeFile(pathImg);
                    except:
                        pass;
                noticia.delete();
                return redirect("inicio" );

            tituloNoticia = noticia.titulo;
            categoria = noticia.categoria;

            partes = NoticiaParte.objects.filter(noticia=noticia);

            #por ahora las noticias se limitaran a un solo cuerpo o parte
            cuerpoNoticia = partes[0].mensaje;
            pathImgNoticia = partes[0].urlImagen;
        except:
            #si algun campo falla se reinician todos
            idGetNoticia = ""
        
    if not idGetNoticia:
        tituloNoticia = ""
        pathImgNoticia = ""
        cuerpoNoticia = ""
        categoria = ""

    categoriasExistentes = [c for c in Categorias.objects.all() if not c==categoria]
    
    #parametros a la web template
    contexto = {"modnoticia": idGetNoticia,
                "oldTitulo": tituloNoticia,
                "oldPathImg": pathImgNoticia,
                "oldCuerpoNoticia": cuerpoNoticia,
                "oldCategoria": categoria,
                "categoriasExistentes": categoriasExistentes,
                };

    return render(request, "crearnoticia.html", contexto);







