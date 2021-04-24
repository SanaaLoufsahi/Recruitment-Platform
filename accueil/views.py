from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from .models import CustomUser
from django.core.mail import EmailMessage,send_mail
from django.contrib import messages
from administrateur.models import formulaire,offres,diplome
from django.views.decorators.csrf import csrf_exempt
from candidat.forms import update_profile
 
def home(request):
    return render(request, 'accueil/page1.html')  

def inscription(request):
     if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first']
        last_name = request.POST['last']
        email = request.POST['email']
        password = request.POST['mot_de_passe']
        
        if CustomUser.objects.filter(email=email).exists():
            messages.info(request, 'Email déjà utilisé !')
            return redirect('page1.html')
        elif CustomUser.objects.filter(username=username).exists():
            messages.info(request, 'Username déjà utilisé !')
            return redirect('page1.html')
        else: 
            user = CustomUser.objects.create_user(username=username,password=password,first_name=first_name,last_name=last_name,email=email,fonction='candidat',mdp=password)
            user.save()
            messages.info(request, "Compte créé, veuillez maintenant s'identifier pour accéder!")
            return redirect('page1.html')
     else:
          return render(request,'page1.html')
@csrf_exempt
def login(request):
    if request.method == 'POST':
        identifiant = request.POST['identifiant']
        password = request.POST['password']
        user = auth.authenticate(username=identifiant, password=password)
        if user is not None:
            utilisateur = CustomUser.objects.get(username=identifiant)
            if utilisateur.fonction == 'admin' :
                auth.login(request, user)
                return render(request, 'administrateur/index.html')
            elif utilisateur.fonction == 'candidat' :
                auth.login(request, user)
                return render(request, 'candidat/dashboard.html')
            elif utilisateur.fonction == 'jury' :
                auth.login(request, user)
                return render(request, 'jury/accueil.html')
        else:
            messages.info(request, "Votre nom d'utilisateur ou votre mot de passe est incorrect !!")
            return redirect('page1.html')
    else :
        return render(request,'accueil/page1.html')
    
def contact(request):
     name = request.POST['name']
     email = request.POST['email']
     subject = request.POST['subject']
     message = request.POST['message']

     email_msg = EmailMessage(
               "New contact form email ",
               'Name : '+name+'\nSubject : '+subject+'\nMessage : '+message+'\nFrom : '+email,
               "UH2C Plateforme " + email,
               ['uh2c.contact@gmail.com'],
          headers = { 'Reply to ': email}
     )
     email_msg.send()
     messages.info(request,'MESSAGE ENVOYE AVEC SUCCES, MERCI!')
     return redirect('page1.html')    
 
def forget(request):
    email=request.POST['email']

    if CustomUser.objects.filter(email=email).exists:
        user = CustomUser.objects.get(email=email)
        messages.info(request, "Vérifier votre boite email pour récupérer votre compte!")
        send_mail('UH2C RECRUTEMENT :Récupération de compte ',
        'Bonjour '+user.last_name+' '+user.first_name+', Voici vos coordonnées pour s''identifier à UH2C-RECRUTEMENT : \n Username : '+user.username+' \n Password : '+user.mdp+' \n Cordialement',
        'uh2c.contact@gmail.com', 
        [user.email],
        fail_silently=False
        )
    else:
        messages.info(request, "Vous n'êtes pas inscrit!")

    return redirect('home')
