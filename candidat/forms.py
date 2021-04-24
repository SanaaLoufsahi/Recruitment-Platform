from django import forms
from accueil.models import CustomUser
from administrateur.models import formulaire


#class formulaire1(forms.ModelForm) :
    #cin = forms.CharField(max_length=8)
    #nom = forms.CharField(max_length=25)
    #prenom = forms.CharField(max_length=25)
    #email = forms.EmailField()
    #phone = forms.IntegerField()
    #adresse = forms.CharField(max_length=1000)
    #date_naissance = forms.DateField()
    #encadrant1 = forms.CharField(max_length=25)
    #encadrant2 = forms.CharField(max_length=25)
    #encadrant3 = forms.CharField(max_length=25)

    #class Meta:
     #   model = formulaire
      #  fields = ['cin','nom','prenom','email','phone','adresse','date_naissance','encadrant1','encadrant2','encadrant3']


class update_profile(forms.Form):
    Nom=forms.CharField()
    Prénom=forms.CharField()
    Username=forms.CharField()
    Email=forms.EmailField()
    Password = forms.PasswordInput()



     
    
    