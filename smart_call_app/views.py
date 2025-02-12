from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, TournamentForm
from .models import Tournament

def landing_page(request):
    login_form = AuthenticationForm()
    register_form = RegisterForm()
    return render(request, 'landing.html', {'login_form': login_form, 'register_form': register_form})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else: 
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


@login_required
def home(request):
    if request.method == 'POST':
        form = TournamentForm(request.POST)
        if form.is_valid():
            tournament = form.save(commit=False)
            tournament.user = request.user
            tournament.save()
            return redirect('home')
    else:
        form = TournamentForm()

    user_tournaments = Tournament.objects.filter(user=request.user)
    return render(request, 'home.html', {'form': form, 'tournaments': user_tournaments})
