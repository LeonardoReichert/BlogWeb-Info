from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Usuario(AbstractUser):
    esAdmin = models.BooleanField(default=False)
    fechaNac = models.DateField(default=None, null=True)
    #username = models.CharField(default=None, null=True)




