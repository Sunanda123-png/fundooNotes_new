from django.urls import path
from . import views

urlpatterns = [
    path('notes',views.Notes.as_view(), name='notes'),
    path('notedetails/<int:id>',views.NotesDetails.as_view(), name='note')
]