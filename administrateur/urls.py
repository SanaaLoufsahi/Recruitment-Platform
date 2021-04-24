from django.urls import path
from . import views

urlpatterns = [
    path('logout', views.logout, name='logout'),
    path('index', views.index , name='index'),
    path('afficher_offre', views.afficher_offre , name='afficher_offre'),
    path('candidatures', views.candidatures , name='candidatures'),
    path('ajouter_offre', views.ajouter_offre , name='ajouter_offre'),
    path('afficher_jury', views.afficher_jury , name='afficher_jury '),
    path('ajouter_jury', views.ajouter_jury  , name='ajouter_jury'),
    path('new_jury', views.new_jury  , name='new_jury'),
    path('new_offre', views.new_offre  , name='new_offre'),
    path('update_offer', views.update_offer, name='update_offer'),
    path('modifier_offre/<int:id>', views.modifier_offre, name='modifier_offre'),
    path('supprimer_offre/<int:id>', views.supprimer_offre, name='supprimer_offre'),
    path('modifier_admin/<int:id>', views.modifier_admin, name='modifier_admin'),
    path('infosCandidature', views.infosCandidature, name='infosCandidature'),
    path('validerCandidature/<int:id1>/<int:id2>', views.validerCandidature, name='validerCandidature'),
    path('choisirjury', views.choisirjury, name='choisirjury'),
]

