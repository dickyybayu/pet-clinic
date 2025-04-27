from django.urls import path
from . import views

app_name = 'putih'

urlpatterns = [
    path('', views.home, name='home'),  
    path('login/', views.login_view, name='login'),  
    path('register/', views.register_selection, name='register_selection'),
    path('register/klien_individu_register/', views.register_klien_individu, name='register_klien_individu'),
    path('register/<str:role>/', views.register_role, name='register_role'),
    path('profil/', views.show_profile, name='show_profile'),
]
