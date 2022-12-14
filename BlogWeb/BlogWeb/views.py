
from django.shortcuts import render, redirect;
from noticias.models import *
from django.urls import reverse

from noticias.models import *;

from math import ceil;

#from django.conf import settings
#from django.core.files.storage import FileSystemStorage

"""
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
"""




def _paginarResultados(resultados_consulta, pagina_actual, elementos_visibles):
    """
    resultados_consulta:
        se refiere a todos los ids de una consulta tal como:
            Tabla.objects.all().order_by("-fecha").values("id")
                o tambien:
            Tabla.objects.filter(categoria=id).values("id")
    
    pagina_actual:
        la pagina actual donde esta la vista, puede ser mayor o igual a 1
    
    elementos_visibles:
        cantidad de elementos por vista
    
    devuelve:
    los ids de la pagina actual,
    pagina anterior, posterior, y maxima
             la pagina anterior o posterior tambien podria ser 0 para no avanzar
        la pagina minima siempre sera 1
    """

    cantidad_resultados = resultados_consulta.count();

    paginaMaxima = ceil(cantidad_resultados / elementos_visibles);

    paginaAnterior = pagina_actual-1 if int(pagina_actual) > 1 else 0;
    paginaSiguiente = pagina_actual+1 if int(pagina_actual) < paginaMaxima else 0;
    
    idsPagina = resultados_consulta[elementos_visibles*paginaAnterior:
                                    elementos_visibles*pagina_actual];

    return idsPagina, paginaAnterior, paginaSiguiente, paginaMaxima;




def inicio(request):

    # - juntar info de noticias -

    noticiasVisibles = [];

    SHOW_MAX = 5; #noticias
    DESC_MAX = 200;

    filtroCategoriaNombre = request.GET.get("categoria", "")
    if filtroCategoriaNombre:
        #argumentos de filtro por categoria
        if filtroCategoriaNombre.lower() == "null":
            #noticias sin categorisar
            categoria = None;
        else:
            #noticias con categoria existente
            try:
                categoria = Categorias.objects.get(nombre=filtroCategoriaNombre);
            except:
                #se puso una categoria inexistente, salir
                return redirect("inicio");

        consulta = Noticia.objects.filter(categoria=categoria).order_by("-fecha");
        filtroParam = "categoria="+filtroCategoriaNombre;
    else:
        # sin argumentos de filtro, filtrar entonces como "mas nuevos"
        consulta = Noticia.objects.all().order_by("-fecha");
        filtroParam = "";
    
    maxPagina = ceil(consulta.count() / SHOW_MAX);
    
    paginaActual = request.GET.get("pagina", "1");
    if not paginaActual.isdigit() or int(paginaActual) < 1 or int(paginaActual) > maxPagina:
        if maxPagina != 0:
            #fuera de rango, pero puede haber 0 resultados validamente
            return redirect("inicio");

    paginaActual = int(paginaActual);

    noticias,pAnterior,pSiguiente,pMaxima = _paginarResultados(consulta,paginaActual,SHOW_MAX);

    for noticia in noticias:
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

    
    categorias = [c for c in Categorias.objects.all()]

    #parametros a la web template
    contexto = {"noticiasVisibles": noticiasVisibles,
                "paginaActual": paginaActual,
                "paginaAnterior": pAnterior,
                "paginaSiguiente": pSiguiente,
                "paginaMaxima": pMaxima,

                "categoriaSeleccionada": filtroCategoriaNombre,
                "categoriasExistentes": categorias,
                "filtroParam": filtroParam,
                };

    return render(request, "inicio.html", contexto);




