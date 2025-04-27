from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),  
    path('login/', views.login_view, name='login'),  
    path('register/', views.register_selection, name='register_selection'),
    path('register/<str:role>/', views.register_role, name='register_role'),
]
