from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, TournamentForm
from .models import Tournament
from django.contrib import messages 

# Render the landing page with the user authentication forms
def landing_page(request):
    login_form = AuthenticationForm()
    register_form = RegisterForm()
    return render(request, 'landing.html', {'login_form': login_form, 'register_form': register_form})

# Log in users with valid credentials
def login_view(request):
    login_form = AuthenticationForm()
    register_form = RegisterForm()

    if request.method == "POST":
        login_form = AuthenticationForm(data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            return redirect('home')

    return render(request, 'landing.html', {'login_form': login_form, 'register_form': register_form})

# Handle user registration by storing new user info in the database and log the user in 
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else: 
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})


# Render the home page for authenticated users 
@login_required
def home_page(request):

    # Allow users to create and associate a new tournament with the user using the tournament form
    if request.method == 'POST':
        form = TournamentForm(request.POST)
        if form.is_valid():
            tournament = form.save(commit=False)
            tournament.user = request.user
            tournament.save()
            return redirect('home')
    else:
        form = TournamentForm()

    # Get and display previous tournaments created by the user
    user_tournaments = Tournament.objects.filter(user=request.user)
    return render(request, 'home.html', {'form': form, 'tournaments': user_tournaments})
