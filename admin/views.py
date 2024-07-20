from rest_framework import generics, status
from rest_framework.response import Response

from users.models import UserModel, ADMIN
from rest_framework.permissions import IsAuthenticated

from admin.serializers import (UserListSerializer,
                               AboutUserSerializer,
                               CreateUpdateTournamentSerializer,
                               RoundsModelSerializer, 
                               MatchResultSerializer)

from shared.pagination import CustomPagination
from users.views import return_error
from tournament.models import TournamentModel, RoundsModel, MatchModel


#________________________________________________________________________ #
# --------------------------- Tournament -------------------------------- #

# region create tournament
class CreateTournamentView(generics.CreateAPIView):
    """
    This class for creating a new tournament! * Only Admin users can create a new tournament.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = CreateUpdateTournamentSerializer
    model = TournamentModel

    def post(self, request, *args, **kwargs):
        if request.user.user_role != ADMIN:
            return return_error(
                message="You do not have permission to create a tournament!", 
                http_request=status.HTTP_401_UNAUTHORIZED
                )
        
        return super().post(request, *args, **kwargs)
# endregion


# region create round
class CreateRoundView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RoundsModelSerializer
    model = RoundsModel

    def post(self, request, *args, **kwargs):

        if request.user.user_role != ADMIN:
            return return_error(
                message="You do not have permission to create a tournament!",
                http_request=status.HTTP_401_UNAUTHORIZED
            )

        return super().post(request, *args, **kwargs)
# endregion



# region create tournament
class UpdateTournamentView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateUpdateTournamentSerializer
    http_method_names = ['put', 'patch']

    def get_queryset(self):
        return TournamentModel.objects.all()
    
    def get_object(self):
        if self.request.user.user_role != ADMIN:
            return return_error(
                message="You do not have permission to create a tournament!",
                http_request=status.HTTP_401_UNAUTHORIZED
            )
        
        return TournamentModel.objects.get(pk=self.kwargs.get('pk'))

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer) 

        # Return serializer's data as response
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)  

        return Response(serializer.data)

# endregion

# region create tournament
class MatchResultUpdateView(generics.UpdateAPIView):
    """
    For updating the match result, only admin users can update
    """
    queryset = MatchModel.objects.all()
    serializer_class = MatchResultSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        if self.request.user.user_role != ADMIN:
            return return_error(
                message="You do not have permission to update a match!",
                http_request=status.HTTP_401_UNAUTHORIZED
            )
        
        return MatchModel.objects.get(id=self.kwargs['pk'])
# endregion
# _________________________________________________________________________ #
# --------------------------- Users Update -------------------------------- #

# region users list
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
# endregion



