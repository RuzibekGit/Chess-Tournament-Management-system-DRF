from django.urls import path
from tournament.views import LeaderboardView

app_name = 'tournament'

urlpatterns = [
    path('<int:tournament_id>/leaderboard/', LeaderboardView.as_view(), name='leaderboard'),
]
