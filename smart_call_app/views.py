from django.shortcuts import render, redirect
from .models import Tournament, Duel
from .forms import DuelForm, WinnerForm

def landing_page(request):
    return render(request, 'landing.html')

def signup(request):
    return render(request, 'signup.html')

def login(request):
    return render(request, 'login.html') 