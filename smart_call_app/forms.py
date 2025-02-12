from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Tournament, Duel

# Form for user registration
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# Form for creating a new tournament 
class TournamentForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = ['name']

# Form for creating a new Duel by inputting two phones
class DuelForm(forms.ModelForm):
    class Meta:
        model = Duel
        fields = ["phone_1", "phone_2"]

# Form for selecting the winner of the current duel
class WinnerForm(forms.ModelForm):
    class Meta:
        model = Duel
        fields = ["winner"]
