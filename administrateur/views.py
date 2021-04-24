from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import formulaire,offres,diplome
from django.contrib.auth.models import User, auth
from accueil.models import CustomUser
from django.core.mail import EmailMessage, send_mail
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import os
import shutil

@login_required
def logout(request):
    auth.logout(request)
    return redirect('/')

@login_required
def index(request):
     return render(request,'administrateur/index.html')

@login_required
def afficher_offre(request):
     offers=offres.objects.all()
     return render(request, 'administrateur/afficher_offre.html',{'offers' : offers})
     
@login_required
def ajouter_offre(request):
     return render(request, 'administrateur/ajouter_offre.html')   

@login_required
def candidatures(request):
     users=CustomUser.objects.filter(fonction='candidat')
     candidats={}
     for user in users:
          for offre in offres.objects.all():
               path1=str(offre.id)     
               path=str(user.id)
               if os.path.isdir('C:\\Users\\hasna\\Documents\\files\\website/media/offre_'+path1+'/user_'+path):
                    candidats[user.id]=user.username
     return render(request, 'administrateur/candidatures.html',{'candidats' : candidats,'users':users})   

@login_required
def afficher_jury(request):
     users=CustomUser.objects.filter(fonction='jury')      
     return render(request, 'administrateur/afficher_jury.html',{'jurys':users})     

@login_required
def ajouter_jury(request):
     return render(request, 'administrateur/ajouter_jury.html')      

@login_required
def new_offre(request):
     titre1=request.POST['titre']
     description1=request.POST['description']

     if offres.objects.filter(titre=titre1).exists():
          messages.info(request,'Offre déjà existe!')
          return redirect('ajouter_offre')
                  
     new = offres(titre=titre1, description=description1)
     new.save()
     path=str(new.id)
     os.mkdir('C:\\Users\\hasna\\Documents\\files\\website/media/offre_'+path)
     return redirect('afficher_offre')

@login_required
def update_offer(request):
     idoffre=request.POST['idoffre']
     offer=offres.objects.get(id=idoffre)
     return render(request,'administrateur/update_offer.html',{'offre':offer})
     
@login_required
def modifier_offre(request,id):
     description1=request.POST['description']
     titre1=request.POST['titre']
     offre=offres.objects.get(id=id)    
     offre=offres(id=id,titre=titre1,description=description1) 
     offre.save()  
     messages.info(request,'Offre modifié!')
     return redirect('afficher_offre')

@login_required
def supprimer_offre(request,id):
     offres.objects.filter(id=id).delete()
     messages.info(request,'Offre supprimé!')
     return redirect('afficher_offre')

@login_required 
def modifier_admin(request,id):
     if request.method=='POST':   
          fname = request.POST['nom']
          lname = request.POST['prenom']
          username = request.POST['username']
          email = request.POST['email']
          password1 = request.POST['password1']
          user=CustomUser(id=id,first_name=fname,last_name=lname,username=username,email=email,password=password1,mdp=password1,fonction='admin')
          user.set_password(password1)
          user.save()
          auth.login(request, user)
          messages.success(request, f'profile modifié !')
          return redirect('index')
     else:
          return render(request, 'administrateur/index.html') 

       
def new_jury(request):
     username = request.POST['username']
     first_name = request.POST['first']
     last_name = request.POST['last']
     email = request.POST['email']
     password = request.POST['password']
        
     if CustomUser.objects.filter(email=email).exists():
          messages.info(request, 'Email déjà existe  !')
          return redirect('ajouter_jury')
     elif CustomUser.objects.filter(username=username).exists():
          messages.info(request, 'Username déjà existe !')
          return redirect('ajouter_jury')
     else:
          user = CustomUser.objects.create_user(username=username,password=password,first_name=first_name,last_name=last_name,email=email,fonction='jury',mdp=password)
          user.save()
          path=str(user.id)
          os.mkdir('C:\\Users\\hasna\\Documents\\files\\website/media/jury_'+path)
          messages.info(request, "Jury ajouté avec succès!")
          send_mail('UH2C RECRUTEMENT : Compte Jury ',
          'Bonjour '+last_name+' '+first_name+', Voici vos coordonnées pour s''identifier à UH2C-RECRUTEMENT comme jury : \n Username : '+username+' \n Password : '+password+' \n Cordialement',
          'uh2c.contact@gmail.com', 
          [email],
          fail_silently=False
          )
          return redirect('ajouter_jury')

@login_required 
def infosCandidature(request):
     if request.method == 'POST':   
          id=request.POST['id']
          user=CustomUser.objects.get(id=id)
          offers = offres.objects.all()
          job={}
          path=str(id)
          folder = os.listdir('C:\\Users\\hasna\\Documents\\files\\website/media/user_'+path)
          for offre in offers:
               path1=str(offre.id)
               if os.path.isdir('C:\\Users\\hasna\\Documents\\files\\website/media/offre_'+path1+'/user_'+path):
                    job[offre.titre]= offre.id

          return render(request,'administrateur/infosCandidat.html',{'folder':folder,'offres':job,'id':id,'offers':offers,'cand':user})
     else :
          return redirect('candidatures')


@login_required 
def validerCandidature(request,id1,id2):
     id3=request.POST['jury']
     path1=str(id1)
     path2=str(id2)
     path3=str(id3)
     for jury in CustomUser.objects.filter(fonction='jury'): 
          path4=str(jury.id)   
          if os.path.isdir('C:\\Users\\hasna\\Documents\\files\\website/media/jury_'+path4+'/offre_'+path2+'/user_'+path1):
               messages.info(request, "Vous avez déjà validé cette candidature!"+path2)
               return  redirect('candidatures') 
     if os.path.isdir('C:\\Users\\hasna\\Documents\\files\\website/media/jury_'+path3+'/offre_'+path2):
          src='C:\\Users\\hasna\\Documents\\files\\website/media/user_'+path1
          dest='C:\\Users\\hasna\\Documents\\files\\website/media/jury_'+path3+'/offre_'+path2+'/user_'+path1
          shutil.copytree(src, dest)
     else:
          os.mkdir('C:\\Users\\hasna\\Documents\\files\\website/media/jury_'+path3+'/offre_'+path2)
          src='C:\\Users\\hasna\\Documents\\files\\website/media/user_'+path1
          dest='C:\\Users\\hasna\\Documents\\files\\website/media/jury_'+path3+'/offre_'+path2+'/user_'+path1
          shutil.copytree(src, dest)
     messages.info(request, "Candidature validée!")
     return  redirect('candidatures') 

def choisirjury(request):
     id1=request.POST['id_cand']
     id2=request.POST['id_offre']
     user=CustomUser.objects.get(id=id1)
     jurys=CustomUser.objects.filter(fonction='jury')
     form=formulaire.objects.get(id=user)
     encadrants={}
     nonEncadrants={}
     for jury in jurys :
          if jury.email == form.encadrant1 or jury.email == form.encadrant2 or jury.email == form.encadrant3 :
               encadrants[jury.id]=jury.id
          else :
               nonEncadrants[jury.id]=jury.id
     return render(request,'administrateur/choisirjury.html',{'nonEncadrants':nonEncadrants,'encadrants':encadrants,'jurys':jurys,'id1':id1,'id2':id2})