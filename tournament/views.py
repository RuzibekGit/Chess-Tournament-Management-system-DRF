from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from tournament.models import TournamentModel
from tournament.serializers import UserSerializer
from shared.pagination import CustomPagination
from users.views import return_error




class LeaderboardView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    pagination_class = CustomPagination

    def get_queryset(self):
        tournament_id = self.kwargs['tournament_id']
        tournament = TournamentModel.objects.filter(id=tournament_id).first()
        if not tournament:
            return []
        return tournament.participants.all().order_by('-rating')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset:
            return return_error("No tournament found! ", http_request=status.HTTP_404_NOT_FOUND)

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
