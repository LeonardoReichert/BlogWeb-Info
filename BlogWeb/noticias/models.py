from django.db import models
from usuarios.models import Usuario
# Create your models here.

from datetime import datetime;



def horaUtcToArg(fecha):
    #transformar de utc a utc-3 (Argentina):
    fecha = datetime.utcfromtimestamp(fecha.timestamp()-(60*60*3));
    #formateamos la hora :
    return fecha.isoformat(" ", "minutes");



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
    mensaje = models.CharField(max_length = Limits.mensajeComentario);
    fecha = models.DateTimeField(auto_now=True);

"""

palabras = '''
zorro pierde el pelo, pero no las mañas, dice un refrán popular que, si lo adaptamos al capitán de la Selección argentina, Lionel Messi, sería “la pulga no pierde las mañas”. En las últimas horas se viralizó un video que muestra al crack rosarino haciendo una jugada en las inferiores de Newells muy parecida a la que hizo en el partido de los cuartos de final del Mundial de Qatar, contra Países Bajos, y que terminó en gol de Molina.

El video en cuestión muestra dos secuencias en espejo. Una ocurrida cuando arrancaba el siglo y Messi solo tenía 12 años y la que ocurrió hace una semana en Doha.
'''.split()

from random import choice, randint;

def randomNoticia():

    user = Usuario.objects.get(id=15)
    categoria = Categorias.objects.get_or_create(nombre=choice(palabras))[0]

    noticia = Noticia.objects.create(
        autor=user,
        titulo = "".join([choice(palabras) for i in range(randint(4, 12))]),
        categoria = categoria, 
        )

    parte1 = NoticiaParte.objects.create(noticia=noticia,
                    mensaje="".join([choice(palabras) for i in range(randint(30, 100))]),
                    urlImagen = "/media/n.png")
#    parte1.save()
##    noticia.save()
#    categoria.save()


#for i in range(100):
#    randomNoticia()

"""

