from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register({Visitantes})#para o admin reconhecer suas classes
