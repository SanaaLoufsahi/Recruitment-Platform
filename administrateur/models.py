from django.db import models
from django.contrib.auth.models import User, auth
from accueil.models import CustomUser 

class formulaire(models.Model): 
    id = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True, default='')
    cin = models.CharField(max_length=8, unique=True, default='')
    nom = models.CharField(max_length=25)
    prenom = models.CharField(max_length=25)
    email = models.EmailField(unique=True,default='')
    phone = models.IntegerField(default='')
    adresse = models.CharField(max_length=1000)
    date_naissance = models.DateField(models.SET_DEFAULT=='')
    encadrant1 = models.EmailField(default='')
    encadrant2 = models.EmailField(default='')
    encadrant3 = models.EmailField(default='')
    objects=models.Manager()


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.id_id, filename)

 
class diplome(models.Model):
    id = models.OneToOneField(formulaire, on_delete=models.CASCADE, primary_key=True )
    attestation_bac = models.FileField(upload_to=user_directory_path)
    attestation_licence = models.FileField(upload_to=user_directory_path)
    attestation_master = models.FileField(upload_to=user_directory_path)
    attestation_doc = models.FileField(upload_to=user_directory_path)
    these_doc = models.FileField(upload_to=user_directory_path)
    article_doc = models.FileField(upload_to=user_directory_path)
    cv = models.FileField(upload_to=user_directory_path)
    lettre_motivation = models.FileField(upload_to=user_directory_path)
    objects=models.Manager() 

class offres(models.Model):
    id = models.AutoField(primary_key=True)
    titre = models.CharField(max_length=100, unique=True)
    description = models.TextField(default='')
    objects=models.Manager()