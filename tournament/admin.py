from django.contrib import admin
from tournament.models import TournamentModel, MatchModel, RoundsModel

@admin.register(TournamentModel)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ['name', 'start_date', 'end_date', 'state']


@admin.register(MatchModel)
class MatchAdmin(admin.ModelAdmin):
    list_display = ['rounds', 'white', 'black', 'winner']


@admin.register(RoundsModel)
class RoundsAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
