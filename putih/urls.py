from django.urls import include, path
from . import views


app_name = 'putih'

urlpatterns = [
    #include urls from hijau app
    path('', views.home, name='home'),  
    path('login/', views.login_view, name='login'),  
    path('register/', views.register_selection, name='register_selection'),
    path('register/klien_register/', views.register_klien, name='register_klien'),
    path('register/<str:role>/', views.register_role, name='register_role'),
    path('profil/', views.show_profile, name='show_profile'),
    path('profil/update/', views.update_klien, name='update_klien'),
    path('logout/', views.logout, name='logout'),
    path('profil/update_password/', views.update_password, name='update_password'),

    
]
