# your_app_name/scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from django.utils import timezone
from tournament.models import TournamentModel, START_SOON, GOING_ON, ENDED



def check_tournament_times():
    now = timezone.now()

    # Update tournaments that should start
    starting_tournaments = TournamentModel.objects.filter(start_date__lte=now, state=START_SOON)
    for tournament in starting_tournaments:
        tournament.state = GOING_ON
        tournament.save()
        print(f"Tournament {tournament.name} has started.")

    # Update tournaments that should end
    ending_tournaments = TournamentModel.objects.filter(end_date__lte=now, state=GOING_ON)
    for tournament in ending_tournaments:
        tournament.state = ENDED
        tournament.save()
        print(f"Tournament {tournament.name} has ended.")

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_tournament_times, 'interval', minutes=1)  # Check every minute
    scheduler.start()