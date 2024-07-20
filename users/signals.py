from django.utils import timezone
from datetime import timedelta
from django.db.models import Avg
from django.db.models.signals import pre_save
from django.dispatch import receiver

from users.models import UserModel
from tournament.models import TournamentModel, GOING_ON, ENDED

from shared.utils import send_code_to_email




# ----------------------------------- Set name -------------------------------------------
@receiver(pre_save, sender=UserModel)
def user_name_update(instance, **kwargs):
    name = instance.name

    if name:
        if instance.first_name not in name or instance.last_name not in name:
            instance.name = instance.get_full_name()
    else:
        instance.name = instance.get_full_name()



# ----------------------------------- Send email -------------------------------------------
@receiver(pre_save, sender=TournamentModel)
def send_email_to_participants(sender, instance, **kwargs):
    state = instance.state
    time = instance.start_date
    now = timezone.now()
    if state == GOING_ON and instance.start_date <= now + timedelta(minutes=1):

        for participant in instance.participants.all():
            if email := participant.email:
                send_code_to_email(
                    email,
                    f"data: {instance.start_date.strftime('%Y.%m.%d %H.%M')} ~ {instance.end_date.strftime('%Y.%m.%d %H.%M')}",
                    participant.name,
                    subject="Your tournament updated",
                    heder="Tournament is started",
                    main_text=f"Siz qatnashmoqchi bolgan {instance.name} tournament boshlandi! Biz sizni kutib qolamiz."
                )

            
    elif state == ENDED and instance.end_date <= now + timedelta(minutes=1):
        for participant in instance.participants.all():
            if email := participant.email:
                send_code_to_email(
                    email,
                    f"data: {instance.start_date.strftime('%Y.%m.%d %H.%M')} ~ {instance.end_date.strftime('%Y.%m.%d %H.%M')}",
                    participant.name,
                    subject="Your tournament updated",
                    heder="Tournament is ended",
                    main_text=f"Siz qatnashgan {instance.name} tournament tugadi! Keyingi tournamentlarda ham kutib qolamiz!"
                )