from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from accueil.models import CustomUser
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from administrateur.models import offres, formulaire, diplome
import os
import shutil
from django.core.mail import send_mail


@login_required
def accueil(request):
    return render(request, 'jury/accueil.html')

@login_required
def logout(request):
    auth.logout(request)
    return redirect('/')

@login_required
def edit(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        user = CustomUser(id=request.user.id, first_name=first_name, last_name=last_name,username=username,email=email,password=password1,mdp=password1,fonction='jury')
        user.set_password(password1)
        user.save()
        auth.login(request, user)
        messages.info(request, 'profile modifié')
        return redirect('accueil')
    else:
        return render(request, 'jury/accueil.html')


@login_required
def candidature(request):
    path1=str(request.user.id)
    offresvalidees={}
    offers = offres.objects.all()
    for offre in offers:
        path2=str(offre.id)
        if os.path.isdir('C:\\Users\\hasna\\Documents\\files\\website/media/jury_'+path1+'/offre_'+path2):
            offresvalidees[offre.titre]=offre.id
            
    return render(request, 'jury/candidature.html',{'offresvalidees':offresvalidees,'offers':offers})

@login_required 
def candidatures_offre(request):
    id2=request.POST['id2']
    path2=str(id2)
    path1=str(request.user.id)
    candidats={}
    users=CustomUser.objects.filter(fonction='candidat')
    for candidat in users:
        path3=str(candidat.id)
        if os.path.isdir('C:\\Users\\hasna\\Documents\\files\\website/media/jury_'+path1+'/offre_'+path2+'/user_'+path3):
            candidats[candidat.id]=candidat.id
    
    return render(request,'jury/candidatures_offre.html',{'candidats':candidats,'id2':id2,'users':users})


@login_required
def documents_candidature(request):
    id3=request.POST['id_candidat']
    id2=request.POST['id_offre']
    path1=str(request.user.id)
    path2=str(id2)
    path3=str(id3)
    folder=os.listdir('C:\\Users\\hasna\\Documents\\files\\website/media/jury_'+path1+'/offre_'+path2+'/user_'+path3)
    candidat=CustomUser.objects.get(id=id3)
    return render(request,'jury/documents_candidature.html',{'folder':folder,'candidat':candidat,'id2':id2})

@login_required
def approuver(request, id1,id2):
    user= CustomUser.objects.get(id=id1)
    offre= offres.objects.get(id=id2).titre
    email= user.email
    nom = user.last_name
    prenom= user.first_name
    send_mail('UH2C RECRUTEMENT : Candidature approuvée ',
    'Félicitations '+nom+' '+prenom+', Vous êtes admis à l''offre auquelle vous avez postulé, intitulée : '+offre+'. \n Vous êtes invité à passer un concours dont les détails seront communiqués aprés. \n Cordialement',
    'uh2c.contact@gmail.com', 
    [email],
    fail_silently=False
    )
    return redirect('candidature')