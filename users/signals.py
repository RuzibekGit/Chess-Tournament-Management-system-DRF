from django.db.models import Avg
from django.db.models.signals import pre_save
from django.dispatch import receiver

from users.models import UserModel





# ----------------------------------- Set name -------------------------------------------
@receiver(pre_save, sender=UserModel)
def user_name_update(instance, **kwargs):
    name = instance.name

    if name:
        if instance.first_name not in name or instance.last_name not in name:
            instance.name = instance.get_full_name()
    else:
        instance.name = instance.get_full_name()

   
    



    
