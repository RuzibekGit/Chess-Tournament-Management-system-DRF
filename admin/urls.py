from django.urls import path

from admin.views import AdminListView, CreateTournamentView, UpdateTournamentView, CreateRoundView

app_name = 'admins'

urlpatterns = [
    path('users/', AdminListView.as_view(), name='users'),
    path('users/<int:pk>/', AdminListView.as_view(), name='about-user'),
    path('tournament/', CreateTournamentView.as_view(), name='tournament'),
    path('tournament/<int:pk>/update/', UpdateTournamentView.as_view(), name='tournament-update'),
    path('add_round/', CreateRoundView.as_view(), name='add-round'),




]
