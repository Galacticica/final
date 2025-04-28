from rest_framework import serializers
from .models import Adventure
from users.models import CustomUser, CurrentAdventure

class AdventureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adventure
        fields = ['idle', 'required_level', 'time_to_complete', 'name', 'description', 'reward_min', 'reward_max', 'xp_min', 'xp_max']        
    
class AdventureStartSerializer(serializers.Serializer):
    discord_id = serializers.CharField(max_length=255)
    adventure_name = serializers.CharField(max_length=255)
    
    def validate(self, data):
        adventure_name = data.get('adventure_name').title()
        discord_id = data.get('discord_id')

        try:
            adventure = Adventure.objects.get(name=adventure_name)
        except Adventure.DoesNotExist:
            raise serializers.ValidationError("Adventure does not exist.")
        
        self.user, created = CustomUser.objects.get_or_create(
            discord_id=discord_id,
            defaults={
                "level": 1,
                "xp": 0,
                "money": 100,
            }
        )

        if CurrentAdventure.objects.filter(user=self.user).exists():
            raise serializers.ValidationError("User is already on an adventure.")

        if self.user.level < adventure.required_level:
            raise serializers.ValidationError("User level is too low for this adventure.")
        
        return data

class CurrentAdventureSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='adventure.name')  
    time_left = serializers.IntegerField()  

    class Meta:
        model = CurrentAdventure
        fields = ['name', 'time_left']

class AdventureStatusSerializer(serializers.Serializer):
    discord_id = serializers.CharField(max_length=255)
    
    def validate(self, data):
        discord_id = data.get('discord_id')

        self.user, created = CustomUser.objects.get_or_create(
            discord_id=discord_id,
            defaults={
                "level": 1,
                "xp": 0,
                "money": 100,
            }
        )

        if not CurrentAdventure.objects.filter(user=self.user).exists():
            raise serializers.ValidationError("User is not on an adventure.")
    
        return data
            


