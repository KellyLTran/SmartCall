from django.urls import path
from .views import landing_page, register, login, home
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', landing_page, name='landing'),
    path('register/', register, name='register'),
    path('home/', home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='landing.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='landing'), name='logout'),
]
