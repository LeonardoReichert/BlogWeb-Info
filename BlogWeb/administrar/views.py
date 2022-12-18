from django.shortcuts import render, redirect

# Create your views here.

from django.urls import reverse

from noticias.models import Categorias



def borrarCategoria(categoriaId):

    try:
        Categorias.objects.get(id=categoriaId).delete()
        return True; #succes
    except:
        pass;

    return False; #error



def administrar(request):

    if not hasattr(request.user, "esAdmin") or not request.user.esAdmin:
        #no tiene permisos para acceder a /administrar/
        return redirect("inicio");

    
    idCategoriaDel = request.POST.get("optCategoriasDel", "");
    if idCategoriaDel and borrarCategoria(idCategoriaDel):
        #se ha borrado una categoria, redireccionar...
        return redirect("administrar");

    contexto = {"categoriasExistentes": Categorias.objects.all()}
    
    return render(request, "administrar.html", contexto)


