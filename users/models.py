from django.http import HttpResponse
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Permission, Group
from django.utils import timezone

from rest_framework_simplejwt.tokens import RefreshToken

import uuid
import random
from datetime import timedelta

from shared.models import BaseModel



ORDINARY_USER, ADMIN = "ORDINARY_USER", "ADMIN"
NEW, CODE_VERIFIED, DONE  = "NEW", "VERIFIED", "DONE",


# -------------------------- User Model -------------------------------
# region user
class UserModel(AbstractUser, BaseModel):

    AUTH_STATUSES = (
        (NEW, NEW),
        (CODE_VERIFIED, CODE_VERIFIED),
        (DONE, DONE), 
    )

    USER_ROLES = (
        (ADMIN, ADMIN),
        (ORDINARY_USER, ORDINARY_USER)
    )
    
    auth_status = models.CharField(max_length=128, choices=AUTH_STATUSES, default=NEW)
    user_role   = models.CharField(max_length=128, choices=USER_ROLES,    default=ORDINARY_USER)
    
    email        = models.EmailField(null=True, blank=True)
    phone_number = models.CharField (null=True, blank=True, max_length=13)
    avatar       = models.ImageField(null=True, blank=True, upload_to='avatars')
    bio          = models.TextField (null=True, blank=True)

    name         = models.CharField (max_length=25,blank=True, null=True)
    age          = models.SmallIntegerField (null=True, blank=True)
    rating       = models.IntegerField (default=0)
    country      = models.CharField (max_length=25, blank=True, null=True)

    last_activity = models.DateTimeField(default=timezone.now)

   
    # --------------- Functions -----------------
    def __str__(self): return self.get_full_name()



    # ------------------------------
    def check_username(self):
        if not self.username:
            temp_username = f"{self.first_name.lower()}-{self.last_name.lower()}-{random.randint(1, 10000)}"
            while UserModel.objects.filter(username=temp_username).exists():
                self.check_username()
            self.username = temp_username


    # ------------------------------
    def check_email(self):
        self.email = str(self.email).lower()

    # ------------------------------
    def hashing_password(self):
        if not self.password.startswith("pbkdf2_sha256"):
            self.set_password(self.password)

    

    # ------------------------------
    def clean(self) -> None:
        self.check_username()
        self.check_email()
        self.hashing_password()


    # ------------------------------
    def save(self, *args, **kwargs):
        if not self.pk:
            self.clean()
        super(UserModel, self).save(*args, **kwargs)

    # ------------------------------
    def create_verify_code(self):
        code = ''.join([str(random.randint(1, 100)%10) for _ in range(4)])

        ConfirmationModel.objects.create(
            code=code,
            user=self, 
            expiration_time= timezone.now() + timedelta(minutes=10)
        )
        return code
    
    # ------------------------------
    def token(self):
        refresh = RefreshToken.for_user(self)
        response = {
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh)
        }

        return response
# endregion


# -------------------------- Confirmation -------------------------------
# region confirmation
class ConfirmationModel(BaseModel):

 
    user            = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='verification_codes')
    expiration_time = models.DateField()
    is_confirmed    = models.BooleanField(default=False)
    code            = models.CharField(max_length=8, null=True)

    def __str__(self): return self.code



# endregion