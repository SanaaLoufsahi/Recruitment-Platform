from django.urls import path, include
from . import views

urlpatterns = [
    path('page1.html', views.home , name='home'),
    path('', views.home , name='home'),
    path('inscription', views.inscription  , name='inscription'),
    path('login', views.login , name='login'),
    path('contact', views.contact  , name='contact'),
    path('forget', views.forget, name='forget'),
    path('', include('administrateur.urls')),
    path('', include('candidat.urls')),
    path('', include('jury.urls'))
]
