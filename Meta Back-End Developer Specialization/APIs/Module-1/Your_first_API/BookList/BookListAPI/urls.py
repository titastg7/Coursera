from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.books,name="books"),
    #path('books/<int:pk>', views.book_item,name="book_item"),
]