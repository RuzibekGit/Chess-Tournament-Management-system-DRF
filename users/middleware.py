# middleware.py
from django.utils import timezone
from datetime import timedelta
from rest_framework_simplejwt.tokens import RefreshToken



from users.models import UserModel



class UpdateLastActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.user.is_authenticated:
            UserModel.objects.filter(id=request.user.id).update(last_activity=timezone.now())

        return response

