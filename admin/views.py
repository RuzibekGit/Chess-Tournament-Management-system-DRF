from rest_framework import generics, status
from django.utils import timezone
from rest_framework.response import Response

from shared.utils import send_code_to_email
from users.models import UserModel, ADMIN
from rest_framework.permissions import AllowAny, IsAuthenticated

from admin.serializers import (UserListSerializer,
                               AboutUserSerializer,
                               CreateTournamentSerializer)

from shared.pagination import CustomPagination
from users.views import return_error
from tournament.models import TournamentModel


class CreateTournamentView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateTournamentSerializer
    model = TournamentModel

    def post(self, request, *args, **kwargs):
        if request.user.user_role != ADMIN:
            return return_error(message="You do not have permission to create a tournament!", http_request=status.HTTP_401_UNAUTHORIZED)
        return super().post(request, *args, **kwargs)







class AdminListView(generics.ListAPIView):
    serializer_class = UserListSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get(self, request, *args, **kwargs):
        user = self.request.user
        if user.user_role != ADMIN:
            print(user.user_role)
            response = {
                "success": False,
                "message": "You do not have permission to access ⛔"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        if pk := self.kwargs.get('pk'):
            self.serializer_class = AboutUserSerializer
            self.pagination_class = None
            return UserModel.objects.filter(id=pk)
        return UserModel.objects.all()
