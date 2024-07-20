from django.urls import path

from admin.views import AdminListView, CreateTournamentView, UpdateTournamentView, CreateRoundView, MatchResultUpdateView

app_name = 'admins'

urlpatterns = [
    path('users/', AdminListView.as_view(), name='users'),
    path('users/<int:pk>/', AdminListView.as_view(), name='about-user'),
    path('add_tournament/', CreateTournamentView.as_view(), name='tournament-add'),
    path('tournament/<int:pk>/update/', UpdateTournamentView.as_view(), name='tournament-update'),
    path('add_round/', CreateRoundView.as_view(), name='add-round'),
    path('<int:pk>/update-result/', MatchResultUpdateView.as_view(), name='update-match-result'),
    
]
