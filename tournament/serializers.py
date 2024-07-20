from rest_framework import serializers

from users.models import UserModel


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['name',  'country', 'age', 'rating', 'username']
