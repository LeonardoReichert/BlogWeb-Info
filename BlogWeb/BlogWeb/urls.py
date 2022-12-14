"""BlogWeb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_view

#add para media:
from django.conf import settings
from django.conf.urls.static import static

from noticias.views import *;
from usuarios.views import Registro;
from administrar.views import *;
from informacion.views import *;


from . import views



urlpatterns = [
    path('admin/', admin.site.urls),
    path("inicio/", views.inicio),
    path("", views.inicio, name="inicio"),
    path("informacion/", informeAcercaDe, name="acercade"),
    path("contacto/", informeContacto, name="contacto"),
    path("login/", auth_view.LoginView.as_view(template_name="login.html"), name="login"),
    path("registro/", Registro.as_view(), name="registro"),
    path("logout/", auth_view.logout_then_login, name="logout"),
    path("crearnoticia/", crearNoticia, name="crearnoticia"),
    path("noticia/", verNoticia, name="vernoticia"),
    path("administrar/", administrar, name="administrar")

    #includes apps urls:
    #path("noticias/", include("noticias.urls"))
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



