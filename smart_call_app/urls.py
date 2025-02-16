from django.urls import path
from .views import landing_page, login_view, register_view, home_page
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', landing_page, name='landing'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('home/', home_page, name='home'),
    path('logout/', auth_views.LogoutView.as_view(next_page='landing'), name='logout'),
]
