from django.urls import path, include
from . import views
urlpatterns = [
    path('logout', views.logout, name='logout'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('offre', views.offre, name='offre'),
    path('cv/', views.cv, name='cv'),
    path('cv.html', views.cv, name='cv'),
    path('edit/<int:id>', views.edit, name='edit'),
    path('profile/<int:id>', views.profile, name='profile'),
    path('postuler/<int:id>', views.postuler, name='postuler')
]


  