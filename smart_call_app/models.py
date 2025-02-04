from django.db import models

# Model to represent each full tournament
class Tournament(models.Model):
    name = models.CharField(max_length=255)

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
