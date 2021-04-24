from django.urls import path
from . import views

urlpatterns = [
    path('accueil', views.accueil, name='accueil'),
    path('edit', views.edit, name='edit'),
    path('logout', views.logout, name='logout'),
    path('candidature', views.candidature, name='candidature'),
    path('candidatures_offre', views.candidatures_offre, name='candidatures_offre'),
    path('documents_candidature', views.documents_candidature, name='documents_candidature'),
    path('approuver/<int:id1>/<int:id2>', views.approuver, name='approuver')
]
