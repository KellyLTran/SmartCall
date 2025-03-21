from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', landing_page, name='landing'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('home/', home_page, name='home'),
    path('logout/', auth_views.LogoutView.as_view(next_page='landing'), name='logout'),
    path('tournament/<int:tournament_id>/', tournament_page, name='tournament'),
    path('delete_tournament/<int:tournament_id>/', delete_tournament, name='delete_tournament'),
    path('tournament/<int:tournament_id>/chat/', ai_chat, name="ai_chat"),
]
