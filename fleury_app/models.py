from django.db import models
from datetime import date
from datetime import datetime
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
# Create your models here.

class Visitantes(models.Model):
    dataAcesso = models.DateTimeField(default=datetime.now)
    def __str__(self):
        return str(self.dataAcesso)
