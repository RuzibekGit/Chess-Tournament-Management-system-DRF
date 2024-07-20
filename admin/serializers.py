from django.utils import timezone
from rest_framework import serializers

import re
from datetime import datetime, timedelta

from shared.utils import send_code_to_email
from users.models import UserModel, ADMIN
from tournament.models import TournamentModel, RoundsModel, MatchModel
from users.serializers import raise_error
from tournament.swiss_system import match_generator




# ----------------------- Users List ------------------------------
# region users list
class UserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserModel
        fields = ['id', 'first_name', 'last_name',
                  'username', 'email', 'auth_status', 'user_role']
# endregion


# ----------------------- About User ------------------------------
# region user
class AboutUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserModel
        fields = ['id', 'first_name', 'last_name',
                  'username', 'email', 'phone_number', 'bio', 'created_at', 'updated_at', 'last_login',  'auth_status', 'user_role']
# endregion


# ----------------------- Create Tournament ------------------------------
# region create
class CreateUpdateTournamentSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()
    participants = serializers.ListField(child=serializers.IntegerField(), write_only=True)

    start_time = serializers.TimeField(write_only=True, required=False)
    end_time = serializers.TimeField(write_only=True, required=False)

    not_found_players = []
    operation_type_is_create = True
    class Meta:
        model = TournamentModel
        fields = ['name', 'participants', 'start_date', 'start_time', 'end_date', 'end_time']
    
    
    # ------------------------------
    def is_valid_date(self, date_str):
        patterns = [
            r"^\d{4}\.\d{2}\.\d{2}$",  # YYYY.MM.DD
            r"^\d{4}-\d{2}-\d{2}$",    # YYYY-MM-DD
            r"^\d{4}/\d{2}/\d{2}$"     # YYYY/MM/DD
        ]
        

        for num, pattern in enumerate(patterns, 1):
            if re.match(pattern, date_str):
                return num
        return False
    
    # ------------------------------
    def is_valid_time(self, time_str):
        pattern = r"^(?:[01]\d|2[0-3]):[0-5]\d(?::[0-5]\d)?$" # HH:MM:SS or HH:MM 
        return re.match(pattern, time_str) is not None
    

    # ------------------------------
    def create(self, validated_data):
        validated_data.pop('start_time')
        validated_data.pop('end_time')
        participants_data = validated_data.pop('participants')

        tournament = TournamentModel.objects.create(**validated_data)

        participants = UserModel.objects.filter(id__in=participants_data)
        tournament.participants.set(participants)
        tournament.save()
        return tournament
    
    # ------------------------------
    def update(self, instance, validated_data):
        self.operation_type_is_create = False
        instance.name = validated_data.get('name', instance.name)
        instance.start_date = validated_data.get('start_date', instance.start_date)
        instance.end_date = validated_data.get('end_date', instance.end_date)

        participants_data = validated_data.pop('participants')
        participants = UserModel.objects.filter(id__in=participants_data)
        for player in participants:
            instance.participants.add(player)

        instance.save()
        return instance
   

    # ------------------------------
    def validate(self, data):
        self.not_found_players = []
        validation_error = dict()
        name = data.get('name')
        participants = data.get('participants', [])

        start_date = data.get('start_date')
        start_time = data.get('start_time')
        end_date = data.get('end_date')
        end_time = data.get('end_time')

        players = []
        for player in participants:
            if not UserModel.objects.filter(id=player).exists():
                self.not_found_players.append(player)
            else:
                players.append(player)

        data['participants'] = players

        if name and TournamentModel.objects.filter(name=name).exists():
            validation_error['name'] = "This name already exists in the tournament database!"

        if start_time and not self.is_valid_time(start_time.strftime('%H:%M:%S')):
            validation_error['start_time'] = "Invalid time format"

        if end_time and not self.is_valid_time(end_time.strftime('%H:%M:%S')):
            validation_error['end_time'] = "Invalid time format"


        if start_date:
            if not self.is_valid_date(start_date.strftime('%Y-%m-%d')):
                validation_error['start_date'] = "Invalid date format"
            elif start_time and not validation_error.get('start_time'):
                start_datetime = timezone.make_aware(datetime.combine(
                    start_date, start_time), timezone.get_current_timezone())
                if start_datetime <= timezone.now():
                    validation_error['start_date'] = "Start date and time must be in the future"
                data['start_date'] = start_datetime

        if end_date:
            if not self.is_valid_date(end_date.strftime('%Y-%m-%d')):
                validation_error['end_date'] = "Invalid date format"

            elif end_time and not validation_error.get('end_time'):
                end_datetime = timezone.make_aware(datetime.combine(
                    end_date, end_time), timezone.get_current_timezone())
                
                if 'start_date' in data and end_datetime <= data['start_date'] + timedelta(days=1):
                    validation_error['end_date'] = "End date and time must be at least one day after the start date and time"
                data['end_date'] = end_datetime

        if validation_error:
            if self.not_found_players:
                validation_error['not_found'] = self.not_found_players
            raise_error(validation_error)

        return data

    # ------------------------------
    def to_representation(self, instance):
        data = {
            "success": True,
            "message": f"Tournament successfully {'created' if self.operation_type_is_create else 'updated'} !.. ",
            "data": {
                "name": instance.name,
                "timing": f"{instance.start_date} ~ {instance.end_date}",
                "participants": {player.id: player.name for player in instance.participants.all()},
                "not_found": [id for id in self.not_found_players]
            }
        }

        return data
# endregion





# ----------------------- Create Rounds ------------------------------
# region round
class RoundsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoundsModel
        fields = [ 'tournament']

    def create(self, validated_data):
        round_instance = RoundsModel.objects.create(**validated_data)
        round_instance.write_round_id()
        round_instance.save()

        match_generator(round_instance.tournament, round_instance)

        return round_instance

    def validate_tournament(self, value):
        if value.state == 'ENDED':
            raise_error("Cannot create a round for a tournament that is has ended.")
        return value

    def to_representation(self, instance):
        data = {
            "success": True,
            "message": f"Round successfully created !  ",
            "data": {
                "name": instance.name,
                "tournament": instance.tournament.name
            }
        }

        return data
    
# endregion

    
class MatchResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatchModel
        fields = ['result']

    def to_representation(self, instance):
        data = {
            "success": True,
            "message": f"Match successfully updated !  ",
            "result": instance.result
        }

        return data
