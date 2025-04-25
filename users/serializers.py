from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['discord_id', 'username', 'level', 'xp', 'money']

class CoinFlipBetSerializer(serializers.Serializer):
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


