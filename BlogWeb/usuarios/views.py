from django.shortcuts import render

# Create your views here.

from django.views.generic.edit import CreateView;
from django.urls import reverse;
from .models import Usuario;
from .forms import RegistroForm;


class Registro(CreateView):
    model = Usuario;
    template_name = "registro.html";
    form_class = RegistroForm;

    def get_success_url(self):
        return reverse("inicio");

 