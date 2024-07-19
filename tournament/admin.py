from django.contrib import admin
from tournament.models import TournamentModel, RoundsModel

@admin.register(TournamentModel)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ['name', 'start_date', 'end_date', 'state']


@admin.register(RoundsModel)
class RoundsAdmin(admin.ModelAdmin):
    list_display = ['rounds', 'white', 'black', 'winner']
