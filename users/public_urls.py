from django.urls import path

from users.views import UserDataAPIView


app_name = 'public'

urlpatterns = [
    path('<str:username>/', UserDataAPIView.as_view(), name='my-acount'),

]
