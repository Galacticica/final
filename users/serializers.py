"""
File: serializers.py
Author: Reagan Zierke
Date: 2025-04-27
Description: Serializers for the Users app.
Serializers for user-related operations such as coin flip betting.
"""



from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    '''
    Serializer for the CustomUser model.
    This serializer is used to serialize user data for the profile endpoint.
    '''

    class Meta:
        model = CustomUser
        fields = ['discord_id', 'username', 'level', 'xp', 'money']

class CoinFlipBetSerializer(serializers.Serializer):
    '''
    Serializer for the CoinFlipBet model.
    This serializer is used to validate the data for a coin flip bet.
    It checks if the user has enough money to place the bet and creates a new user if they don't exist.
    It also validates the bet amount and the side of the coin flip.
    '''

    discord_id = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255)
    bet = serializers.IntegerField(min_value=1)
    side = serializers.ChoiceField(choices=['heads', 'tails'])

    def validate(self, data):
        self.user, created = CustomUser.objects.get_or_create(
            discord_id=data['discord_id'],
            defaults={
                "username": data['username'],
                "level": 1,
                "xp": 0,
                "money": 100,
            }
        )

        if self.user.money < data['bet']:
            raise serializers.ValidationError("Insufficient funds.")
        return data


