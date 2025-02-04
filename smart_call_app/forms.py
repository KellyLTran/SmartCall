from django import forms
from .models import Duel

# Form that allow users to create a new Duel by inputting two phones
class DuelForm(forms.ModelForm):
    class Meta:
        model = Duel
        fields = ["phone_1", "phone_2"]

# Form that allow users to select the winner of the current duel
class WinnerForm(forms.ModelForm):
    class Meta:
        model = Duel
        fields = ["winner"]
