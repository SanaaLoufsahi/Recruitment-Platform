from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from accueil.models import CustomUser
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from administrateur.models import offres, formulaire, diplome
import os
import shutil


@login_required
def logout(request):
    auth.logout(request)
    return redirect('/')

@login_required
def offre(request):
    Offres = offres.objects.all()
    return render(request, 'candidat/offre.html', {'Offres': Offres})

@login_required
def dashboard(request):
    return render(request, 'candidat/dashboard.html')

@login_required
def cv(request):
    if formulaire.objects.filter(id=request.user).exists():
        form = formulaire.objects.get(id=request.user)
        dip = diplome.objects.get(id=form)
        #form = formulaire(id='',cin='',nom='',prenom='',date_naissance='',adresse='',phone='',email='',encadrant1='', encadrant2='', encadrant3='')
        return render(request, 'candidat/cv.html',{'form':form, 'dip':dip})
    else :
        return render(request, 'candidat/cv.html')

@login_required
def edit(request, id):
    if request.method == 'POST':
        cin = request.POST['cin']
        nom = request.POST['name']
        prenom = request.POST['prenom']
        dateNaissance = request.POST['date'] 
        adresse = request.POST['adress']
        telephone = request.POST['numero']
        email = request.POST['email']
        encadrant1 = request.POST['encadrant1']
        encadrant2 = request.POST['encadrant2']
        encadrant3 = request.POST['encadrant3']
        encadrant3 = request.POST['encadrant3']
        bac = request.FILES['bac']
        licence = request.FILES['licence']
        master = request.FILES['master']
        these = request.FILES['these']
        article = request.FILES['article']
        doctorat = request.FILES['doctorat'] 
        cv = request.FILES['cv']
        lettre_motivation = request.FILES['lettre_motivation']
        user = CustomUser.objects.get(id=id)
        path=str(user.id)
        if formulaire.objects.filter(cin=cin).exists():
            update1 = formulaire.objects.get(cin=cin)
            update1 = formulaire(id=user,cin=cin, nom=nom, prenom=prenom, date_naissance=dateNaissance, email=email, phone=telephone, adresse=adresse, encadrant1=encadrant1, encadrant2=encadrant2, encadrant3=encadrant3)
            update1.save()
            update2 = diplome.objects.get(id=update1)
            os.remove('C:\\Users\\hasna\\Documents\\files\\website/media/'+update2.attestation_bac.name)
            os.remove('C:\\Users\\hasna\\Documents\\files\\website/media/'+update2.attestation_licence.name)
            os.remove('C:\\Users\\hasna\\Documents\\files\\website/media/'+update2.attestation_master.name)
            os.remove('C:\\Users\\hasna\\Documents\\files\\website/media/'+update2.attestation_doc.name)
            os.remove('C:\\Users\\hasna\\Documents\\files\\website/media/'+update2.these_doc.name)
            os.remove('C:\\Users\\hasna\\Documents\\files\\website/media/'+update2.article_doc.name)
            os.remove('C:\\Users\\hasna\\Documents\\files\\website/media/'+update2.cv.name)
            os.remove('C:\\Users\\hasna\\Documents\\files\\website/media/'+update2.lettre_motivation.name)
            os.remove('C:\\Users\\hasna\\Documents\\files\\website/media/user_'+path+'/informations.csv')
            file_name = "{}informations.csv".format('media/user_'+path+'/')
            with open(file_name, 'w') as file:     
                header='CIN,Nom,Prenom,email,Telephone,Adresse,Naissance \n'
                file.write(header)
                file.write(str(update1.cin)+','+update1.nom+','+update1.prenom+','+str(update1.email)+','+str(update1.phone)+','+update1.adresse+','+str(update1.date_naissance))
            update2 = diplome(id=update1,attestation_bac=bac,attestation_licence=licence,attestation_master=master,attestation_doc=doctorat,these_doc=these,article_doc=article,cv=cv,lettre_motivation=lettre_motivation)
            update2.save()
            return redirect('dashboard')
        else:
            update1 = formulaire(id=user,cin=cin, nom=nom, prenom=prenom, email=email, date_naissance=dateNaissance, phone=telephone, adresse=adresse, encadrant1=encadrant1, encadrant2=encadrant2, encadrant3=encadrant3)
            update1.save()
            update2 = diplome(id=update1,attestation_bac=bac,attestation_licence=licence,attestation_master=master,attestation_doc=doctorat,these_doc=these,article_doc=article,cv=cv,lettre_motivation=lettre_motivation)
            update2.save()
            file_name = "{}informations.csv".format('media/user_'+path+'/')
            with open(file_name, 'w') as file:     
                header='CIN,Nom,Prenom,email,Telephone,Adresse,Naissance \n'
                file.write(header)
                file.write(str(update1.cin)+','+update1.nom+','+update1.prenom+','+str(update1.email)+','+str(update1.phone)+','+update1.adresse+','+str(update1.date_naissance))
            return redirect('dashboard')
    else: 
        return render(request, 'cv.html')
 

@login_required
def profile(request,id):
    if request.method=='POST':
            fname = request.POST['nom']
            lname = request.POST['prenom']
            username = request.POST['username']
            email = request.POST['email']
            password1 = request.POST['password1']
            user=CustomUser(id=id,first_name=fname,last_name=lname,username=username,email=email,password=password1,mdp=password1,fonction='candidat')
            user.set_password(password1)
            user.save()
            auth.login(request, user)
            messages.success(request, f'profile modifié !')
            return redirect('dashboard')
    else:  
        return render(request, 'candidat/dashboard.html') 
 
@login_required
def postuler(request,id):
    if formulaire.objects.filter(id=request.user).exists():
        path=str(request.user.id)
        src = 'C:\\Users\\hasna\\Documents\\files\\website/media/user_'+path  
        path2=str(id)
        dest = 'C:\\Users\\hasna\\Documents\\files\\website/media/offre_'+path2+'/user_'+path
        if os.path.isdir(dest):
            messages.success(request, f'Vous avez déjà postulé à cette offre!')
            return redirect(offre)
        else:
            shutil.copytree(src, dest)
            messages.success(request, f'Votre candidature à été envoyé avec succès ! Si vous êtes admis, vous recevrez un email !')
            return redirect(offre)
    else :
        messages.success(request, f'Vous devez remplir la formulaire de candidature avant de postuler!')
        return redirect(offre)
