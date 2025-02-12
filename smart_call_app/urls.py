from django.urls import path
from .views import landing_page, signup, login

urlpatterns = [
    path('', landing_page, name='landing'),
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
]
