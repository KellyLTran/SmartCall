from django.db import models
from django.contrib.auth.models import User

# Model to represent each full tournament
class Tournament(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    winner = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

# Model to represent each pair of phones competing with each other (duels)
class Duel(models.Model):
    # Track which tournament and round the pair belongs to 
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    round_number = models.IntegerField()
    phone_1 = models.CharField(max_length=255) # First competitor
    phone_2 = models.CharField(max_length=255, blank=True, null=True) # Second competitor can be empty initially
    winner = models.CharField(max_length=255, blank=True, null=True) # Winner will be chosen by the user

    # Move the chosen winner to compete with another winner in the next round
    def advance_winner(self):
        if self.winner: 
            next_round = self.round_number + 1

            # If there is only one duel left in the final round, stop advancing
            last_round_duels = Duel.objects.filter(tournament=self.tournament, round_number=self.round_number)
            if last_round_duels.count() == 1:
                return

            # Find an incomplete duel in this next round
            incomplete_duel = Duel.objects.filter(
                tournament=self.tournament, 
                round_number=next_round,
                phone_2__isnull=True
            )

            # If an incomplete duel is found, assign this winner as the second phone in the duel
            if incomplete_duel.exists():
                incomplete_duel.update(phone_2=self.winner)
            
            # Otherwise, all duels are full, so create a new duel to assign this winner
            else:
                Duel.objects.create(
                    tournament=self.tournament,
                    round_number=next_round,
                    phone_1=self.winner
                )
    
    def __str__(self):
        return f"{self.phone_1} vs {self.phone_2 or 'Waiting for opponent'}"

# Model for the AI Chatbot
class AIChatbot(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    query = models.TextField()
    response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.query[:30]}"
