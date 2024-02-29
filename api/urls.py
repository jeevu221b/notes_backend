from django.urls import path, include
from .views import apiHome, signup, login, token, createNotes, getNotes, logout


urlpatterns = [
    path('', apiHome),
    path('signup/', signup),
    path('login/', login),
    path('token/', token),
    path('getNotes/', getNotes),
    path('createNotes/', createNotes),
    path('logout/', logout)
]
