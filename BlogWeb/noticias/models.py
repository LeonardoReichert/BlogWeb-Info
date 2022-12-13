from django.db import models
from usuarios.models import Usuario
# Create your models here.



class Categorias(models.Model):
    nombre = models.CharField(max_length=50);


class Noticia(models.Model):
    titulo = models.CharField(max_length=200);
    #detalles = models.CharField(max_length=200);
    fecha = models.DateTimeField(auto_now=True);
    autor = models.ForeignKey(Usuario, on_delete=models.CASCADE);
    categoria = models.ForeignKey(Categorias, null=True, on_delete=models.SET_NULL);
    #agregar regla de negocios para que esta fk no sea nula amenos que se elimine la categoria.
    

class NoticiaParte(models.Model):
    noticia = models.ForeignKey(Noticia, on_delete=models.CASCADE);
    mensaje = models.TextField();
    urlImagen = models.CharField(max_length=250, null=True);


class Comentario(models.Model):
    noticia = models.ForeignKey(Noticia, on_delete=models.CASCADE);
    autor = models.ForeignKey(Usuario, on_delete=models.CASCADE);
    mensaje = models.TextField();
    fecha = models.DateTimeField(auto_now=True);

