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
    
class GearPurchaseSerializer(serializers.Serializer):
    '''
    Serializer for gear purchase.
    This serializer is used to serialize gear data for the gear purchase endpoint.
    '''

    discord_id = serializers.CharField(max_length=255)
    gear_name = serializers.CharField(source='name')


    def validate(self, data):
        gear_name = data.get('name').title()
        discord_id = data.get('discord_id')

        try:
            gear = Gear.objects.get(name=gear_name)
        except Gear.DoesNotExist:
            raise serializers.ValidationError("Gear does not exist.")
        
        self.user, created = CustomUser.objects.get_or_create(
            discord_id=discord_id,
            defaults={
                "level": 1,
                "xp": 0,
                "money": 100,
            }
        )
        
        if OwnedItem.objects.filter(user=self.user, gear=gear).exists():
            raise serializers.ValidationError("User already owns this gear.")
        
        if self.user.money < gear.cost:
            raise serializers.ValidationError("User does not have enough money to purchase this gear.")
        
        data['gear'] = gear
        data['user'] = self.user
        return data
        

    