from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, TournamentForm
from .models import Tournament, Duel, AIChatbot
from django.contrib import messages 
from collections import defaultdict 

import google.generativeai as genai
from django.conf import settings
from django.http import HttpResponse

# Configure the Gemini API
genai.configure(api_key=settings.GOOGLE_GEMINI_API_KEY)

# Get the response from Gemini AI
def get_ai_response(user_input):
    model = genai.GenerativeModel("gemini-1.5-pro")
    chat = model.start_chat()
    response = chat.send_message(user_input)
    return response.text

# Handle AI responses and save chat history 
@login_required
def ai_chat(request, tournament_id):
    tournament = get_object_or_404(Tournament, id=tournament_id, user=request.user)
    user_query = request.POST.get("query", "")

    ai_response = get_ai_response(user_query)

    # Save chat history
    chat_history = AIChatbot.objects.create(
        user=request.user, tournament=tournament, query=user_query, response=ai_response
    )

    return HttpResponse(ai_response)


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
    
            # Get choices from the form
            choices = []
            for key, value in request.POST.items():
                if key.startswith("choice"):
                    choices.append(value)

            # Check for duplicates by converting all to lowercase and putting them in a set
            lowercased_choices = [choice.lower() for choice in choices]

            # If the set length is different from the original length of choices, then there were duplicates removed
            if len(lowercased_choices) != len(set(lowercased_choices)):
                messages.error(request, "Duplicate choices are not allowed. Please enter unique phone names.")
                return redirect('home')

            tournament = form.save(commit=False)
            tournament.user = request.user
            tournament.save()

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
        return redirect('home') 

    return redirect('home')


# Render the tournament bracket page to diplay and advance user choices
@login_required
def tournament_page(request, tournament_id):
    tournament = get_object_or_404(Tournament, id=tournament_id, user=request.user)

    # Assign duels to their specific round using a dictionary
    duels = Duel.objects.filter(tournament=tournament).order_by('round_number')
    rounds = defaultdict(list)
    for duel in duels:
        rounds[duel.round_number].append(duel)

    # Debug statement
    for round_num, duels_in_round in rounds.items():
        print(f"Round {round_num}:")
        for duel in duels_in_round:
            print(f" Duel {duel.id} | {duel.phone_1} vs {duel.phone_2} | Winner: {duel.winner}")

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
                    return redirect('winner', tournament_id=tournament.id)
        return redirect('tournament', tournament_id=tournament.id)


    # Functionality to filter and display only two rounds at a time
    last_completed_round = None
    incomplete_rounds = [] 

    if rounds: 
        sorted_rounds = sorted(rounds.keys())

        # Iterate through each round to get the most recently completed round
        for round_num in sorted_rounds:
            round_duels = rounds[round_num]

            # If all duels in this round have a winner, it is completed 
            if all(duel.winner for duel in round_duels):
                last_completed_round = round_num
            else: 
                incomplete_rounds.append(round_num)
                if len(incomplete_rounds) >= 2:
                    break
        
    filtered_rounds = {}
    if last_completed_round:

        # Display the last completed round only if the user has not selected a winner in the new round yet
        if incomplete_rounds and not any(duel.winner for duel in rounds[incomplete_rounds[0]]):
            filtered_rounds[last_completed_round] = rounds[last_completed_round]

        # If there are no more incomplete rounds (final winner chosen), still display the last completed round
        elif not incomplete_rounds: 
            filtered_rounds[last_completed_round] = rounds[last_completed_round]
    
    # Always display two incomplete rounds to account for advancing winners
    for round_num in incomplete_rounds:
        filtered_rounds[round_num] = rounds[round_num]

    return render(request, 'tournament.html', {
        'tournament': tournament,
        'rounds': filtered_rounds,
    })


@login_required
def winner_page(request, tournament_id):
    tournament = get_object_or_404(Tournament, id=tournament_id, user=request.user)
    duels = Duel.objects.filter(tournament=tournament).order_by('round_number')

    rounds = defaultdict(list)
    for duel in duels:
        rounds[duel.round_number].append(duel)

    return render(request, 'winner.html', {
        'tournament': tournament,
        'rounds': dict(rounds),
    })
