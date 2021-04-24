from django.db import models
from django.contrib.auth.models import AbstractUser,UserManager


 
class CustomUser(AbstractUser):
    fonction = models.CharField(max_length=15)
    mdp = models.CharField(max_length=20)
    objects=UserManager()

    #def __init__(self, user, *args, **kwargs):
     #   self.user = user
