from django.db import models
from usuarios.models import Usuario
# Create your models here.


class Limits:
    categoriaNombre = 30;
    tituloNoticia = 200;
    mensajeNoticia = 10000;
    nombreImagen = 250;
    mensajeComentario = 1000;



class Categorias(models.Model):
    nombre = models.CharField(max_length=Limits.categoriaNombre, unique=True);


class Noticia(models.Model):
    titulo = models.CharField(max_length=Limits.tituloNoticia);
    #detalles = models.CharField(max_length=200); #obviado
    fecha = models.DateTimeField(auto_now=True);
    autor = models.ForeignKey(Usuario, on_delete=models.CASCADE);
    categoria = models.ForeignKey(Categorias, null=True, on_delete=models.SET_NULL);
    #agregar regla de negocios para que esta fk no sea nula amenos que se elimine la categoria.
    

class NoticiaParte(models.Model):
    noticia = models.ForeignKey(Noticia, on_delete=models.CASCADE);
    mensaje = models.TextField(max_length=Limits.mensajeNoticia);
    urlImagen = models.CharField(max_length=Limits.nombreImagen, null=True);
    #la primera parte debe tener una imagen


class Comentario(models.Model):
    noticia = models.ForeignKey(Noticia, on_delete=models.CASCADE);
    autor = models.ForeignKey(Usuario, on_delete=models.CASCADE);
    mensaje = models.TextField(max_length = Limits.mensajeComentario);
    fecha = models.DateTimeField(auto_now=True);



