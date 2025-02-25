from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, TournamentForm
from .models import Tournament, Duel
from django.contrib import messages 
from collections import defaultdict 


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

    # Create and associate a new tournament with the user using the tournament form
    if request.method == 'POST':
        form = TournamentForm(request.POST)
        if form.is_valid():
            tournament = form.save(commit=False)
            tournament.user = request.user
            tournament.save()
            
            # Get choices from the form
            choices = []
            for key, value in request.POST.items():
                if key.startswith("choice"):
                    choices.append(value)

            # Create duels from the choices for the first round
            if len(choices) >= 2:
                for i in range(0, len(choices), 2):  
                    phone_1 = choices[i]

                    # Assign phone_2 to the next choice unless there is an odd number of choices 
                    if i + 1 < len(choices):
                        phone_2 = choices[i + 1]
                    else:
                        phone_2 = None

                    Duel.objects.create(
                        tournament=tournament,
                        round_number=1,
                        phone_1=phone_1,
                        phone_2=phone_2
                    )

            return redirect('tournament', tournament_id=tournament.id) 
    else:
        form = TournamentForm()

    # Get and display previous tournaments created by the user
    user_tournaments = Tournament.objects.filter(user=request.user)
    return render(request, 'home.html', {'form': form, 'tournaments': user_tournaments})


# Allow users to properly delete previous tournaments from the database
@login_required
def delete_tournament(request, tournament_id):
    tournament = get_object_or_404(Tournament, id=tournament_id, user=request.user)

    if request.method == "POST":
        tournament.delete()
        messages.success(request, "Tournament deleted successfully.")
        return redirect('home') 

    return redirect('home')


# Render the tournament bracket page to diplay and advance user choices
@login_required
def tournament_page(request, tournament_id):
    tournament = get_object_or_404(Tournament, id=tournament_id, user=request.user)

    # Assign duels to their specific round
    duels = Duel.objects.filter(tournament=tournament).order_by('round_number')
    rounds = defaultdict(list)
    for duel in duels:
        rounds[duel.round_number].append(duel)

    # When a choice is selected as a winner in the duel, save and advance the winner
    if request.method == "POST":
        duel_id = request.POST.get("duel_id")
        winner = request.POST.get("winner")
        duel = get_object_or_404(Duel, id=duel_id, tournament=tournament)
        duel.winner = winner
        duel.save()
        duel.advance_winner()
        
        # Get updated duels after advancing the winner
        duels = Duel.objects.filter(tournament=tournament).order_by('round_number')
        rounds = defaultdict(list)
        for duel in duels:
            rounds[duel.round_number].append(duel)

        # If there is only one duel left in the final round, the winner selected is the final winner
        if rounds: 
            last_round = max(rounds)
            if last_round and len(rounds[last_round]) == 1:
                final_duel = rounds[last_round][0]
                if final_duel.winner and not tournament.winner: 
                    tournament.winner = final_duel.winner
                    tournament.save()
                    return redirect('tournament', tournament_id=tournament.id)

        return redirect('tournament', tournament_id=tournament.id)

    return render(request, 'tournament.html', {'tournament': tournament, 'rounds': dict(rounds)})
