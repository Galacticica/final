from rest_framework import serializers
from users.models import CustomUser, OwnedItem
from .models import Gear


class ShopListSerializer(serializers.ModelSerializer):
    '''
    Serializer for listing gear items.
    This serializer is used to serialize gear data for the gear list endpoint.
    '''
    
    class Meta:
        model = Gear
        fields = ['id', 'name', 'description', 'cost', 'xp_bonus', 'money_bonus', 'time_bonus']

    
class GearDetailSerializer(serializers.Serializer):
    '''
    Serializer for gear details.
    This serializer is used to serialize gear data for the gear detail endpoint.
    '''
    
    gear_name = serializers.CharField(source='name')

    def validate(self, data):
        gear_name = data.get('name').title()
        
        try:
            gear = Gear.objects.get(name=gear_name)
        except Gear.DoesNotExist:
            raise serializers.ValidationError("Gear does not exist.")
        
        data['gear'] = gear
        return data