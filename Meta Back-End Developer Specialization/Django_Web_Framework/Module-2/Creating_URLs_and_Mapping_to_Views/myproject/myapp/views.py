from django.shortcuts import render
from django.http import HttpResponse

def home(request) :
    return HttpResponse(f'<h1>Welcome to Little Lemon!</h1>')

# About View
def about(request) :
    return HttpResponse(f'<h2>About Us</h2>')

# Menu
def menu(request) :
    return HttpResponse(f'<h2>Menu for Little Lemon</h2>')

# Book
def book(request) :
    return HttpResponse(f'<h2>Make a booking</h2>')