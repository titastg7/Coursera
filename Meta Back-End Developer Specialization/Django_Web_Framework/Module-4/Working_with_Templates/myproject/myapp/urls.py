from django.urls import path
from . import views

urlpatterns = [
    path('about/', views.about, name="about"),
    path('menu/', views.menu, name="menu"),
    path('home/', views.home, name='home'),
    path('book/', views.book, name='book'),  
 
]