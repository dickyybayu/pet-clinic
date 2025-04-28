from django.urls import path
from . import views

app_name = 'merah'

urlpatterns = [
    path('show_vaksinasi/', views.show_vaksinasi, name='show_vaksinasi'),  
]
