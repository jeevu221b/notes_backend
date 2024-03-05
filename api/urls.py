from django.urls import path, include
from .views import apiHome, signup, login, createNotes, getNotes, logout, editNotes, deleteNotes


urlpatterns = [
    path('', apiHome),
    path('signup/', signup),
    path('login/', login),
    path('logout/', logout),
    path('createnotes/', createNotes),
    path('getnotes/', getNotes),
    path('getnotes/<str:id>/', getNotes),
    path('editnotes/', editNotes),
    path('deletenotes/', deleteNotes)
]
