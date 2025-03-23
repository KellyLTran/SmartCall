from django.contrib import admin
from .models import Tournament, Duel, AIChatbot

# Register your models here.
admin.site.register(Tournament)
admin.site.register(Duel)
admin.site.register(AIChatbot)