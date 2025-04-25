from rest_framework import serializers
from .models import Adventure

class AdventureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adventure
        fields = ['idle', 'required_level', 'time_to_complete', 'name', 'description', 'reward_min', 'reward_max', 'xp_min', 'xp_max']
