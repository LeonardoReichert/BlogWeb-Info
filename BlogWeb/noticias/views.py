
from django.shortcuts import render, redirect;
from noticias.models import *
from django.urls import reverse

from django.http import HttpResponseRedirect


#from django.conf import settings
from django.core.files.storage import FileSystemStorage

from os.path import splitext, exists;
from os import remove as removeFile
import time;

# Create your views here.

#para subir la imagen:
fstorage = FileSystemStorage();





def publicarComentario(request):

    noticia = Noticia.objects.get(id=request.POST["idNoticiaComentario"])
    
    msgComentario = request.POST["msgComentario"];
    if msgComentario.strip() == "":
        #el comentario solo es contenido vacio.
        return;
        
    comentario = Comentario.objects.create(noticia=noticia,
                                            autor=request.user,
                                            mensaje=msgComentario);
    comentario.save()

    #return comentario.id;



def verNoticia(request):

    if "idNoticiaComentario" in request.POST and "msgComentario" in request.POST:
        publicarComentario(request);
        #el usuario uso post para dejar un comentario en la noticia
        return redirect("/noticia/?id="+str(request.POST["idNoticiaComentario"]));

    idNoticia = request.GET.get("id", None);
    try:
        noticia = Noticia.objects.get(id=idNoticia);
    except:
        noticia = None;
    
    contexto = {}
    
    if noticia:
        contexto["idNoticia"] = noticia.id;
        contexto["noticiaFecha"] = horaUtcToArg(noticia.fecha);
        contexto["noticiaTitulo"] = noticia.titulo;
        contexto["noticiaCategoria"] = noticia.categoria;

        partes = NoticiaParte.objects.filter(noticia=noticia);
        
        #por ahora las noticias se limitaran a un solo cuerpo o parte
        contexto["imgNoticia"] = partes[0].urlImagen;
        contexto["cuerpoNoticia"] = partes[0].mensaje;

        contexto["comentarios"] = [];
        for c in Comentario.objects.filter(noticia=noticia):
            
            contexto["comentarios"].append((c.id,
                                            c.autor.username,
                                            horaUtcToArg(c.fecha),
                                            c.mensaje));
    else:
        # probablemente se paso un id de pagina por parametro a la pagina que no existe
        return redirect( "inicio" );

    return render(request, "noticia.html", contexto);



def removeprefix(cadena, prefix):
    """ str.removeprefix aparece en python 3.9  """

    if cadena.startswith(prefix):

        return cadena[len(prefix):]
    return cadena;



def crearNoticia(request):
    """ Crea o modifica  o borra noticia """

    #Categorias.objects.get(id=6).delete()

    if not hasattr(request.user, "esAdmin") or not request.user.esAdmin:
        #si no es admin, no tendria los permisos para usar esta funcion
        print("no admin")
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
            print("no mensaje post")
            return redirect( "crearnoticia" );
        
        mensajePost1 = mensajePost1[:Limits.mensajeNoticia];

        #tanto en la creacion como en la modificacion se puede crear una categoria
        idCategoria = request.POST.get("categoria", "");
        categoria = None;

        if not idCategoria:
            #no se selecciono ninguna categoria, error
            print("No id de categoria")
            return redirect( "crearnoticia" );

        elif idCategoria == "+":
            #se eligio crear la categoria
            nombreNuevaCategoria = request.POST.get("nueva_categoria", "");
            #categoria = None
            if nombreNuevaCategoria and nombreNuevaCategoria.lower() != "null":
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
            print("No se creo una categoria")
            return redirect( "crearnoticia" );

        tituloPost = tituloPost[:Limits.tituloNoticia]; #200 length max

        imgPost1 = "";
        img1 = request.FILES.get("img1", "");
        if img1 :
            #elegimos una marca de tiempo unica para el nombre de la imagen
            #esto reduce problemas de cache donde se van imagenes anteriores
            timestamp = str(time.time());
            filename = fstorage.save(timestamp+splitext(img1.name)[1], img1);
            imgPost1 = fstorage.url(filename);

        if not idPostNoticia:
            #no se especifica el ID, se crea nueva noticia

            if not imgPost1:
                #dar error, no se puso imagen en una nueva noticia
                print("no se puso iagen a la nueva noticia")
                return redirect( "crearnoticia" );

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
                
                oldPathImg = removeprefix(parte1.urlImagen, "/");
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
        print("succes post")
        return redirect("/noticia/?id="+str(idPostNoticia))

    elif idGetNoticia:
        #Peticion con metodo GET
        #pedido de entrar a modificar la noticia
        #se recupera y carga los campos de la notica:
        
        try:
            noticia = Noticia.objects.get(id=idGetNoticia);

            #se pidio borrar la noticia?
            deleter = request.GET.get("delete", "");
            print("deleter", str(deleter), deleter, len(deleter), type(deleter))
            if str(deleter).upper() == "YES":
                #pues se borra y se redirecciona al inicio:
                pathImg = removeprefix(NoticiaParte.objects.get(noticia=noticia).urlImagen, "/");
                if exists(pathImg):
                    #se intenta borra la imagen que ya no se usara:
                    try:
                        removeFile(pathImg);
                    except:
                        pass;
                noticia.delete();
                print("se borro la noticia?")
                return redirect("inicio" );
            else:
                print("es falso %s" % deleter, deleter=="yes")
            
            tituloNoticia = noticia.titulo;
            categoria = noticia.categoria;

            partes = NoticiaParte.objects.filter(noticia=noticia);

            #por ahora las noticias se limitaran a un solo cuerpo o parte
            cuerpoNoticia = partes[0].mensaje;
            pathImgNoticia = partes[0].urlImagen;
            print("se modifico la noticia?")
        except Exception as msg:
            print("real problema", str(msg))
            #si algun campo falla se reinician todos
            idGetNoticia = ""
        
    if not idGetNoticia:
        tituloNoticia = ""
        pathImgNoticia = ""
        cuerpoNoticia = ""
        categoria = ""

    categoriasExistentes = [c for c in Categorias.objects.all() if c != categoria]
    
    #parametros a la web template
    contexto = {"modnoticia": idGetNoticia,
                "oldTitulo": tituloNoticia,
                "oldPathImg": pathImgNoticia,
                "oldCuerpoNoticia": cuerpoNoticia,
                "oldCategoria": categoria,
                "categoriasExistentes": categoriasExistentes,
                };

    return render(request, "crearnoticia.html", contexto);




#def paginarNoticias(consultaOrm, ):






