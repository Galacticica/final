from rest_framework import serializers
from users.models import CustomUser, OwnedItem
from .models import Gear

 
class ShopListSerializer(serializers.ModelSerializer):
    '''
    Serializer for the shop list.
    This serializer is used to serialize gear data for the shop list endpoint.
    '''
    
    class Meta:
        model = Gear
        fields = ['id', 'name', 'cost', 'description', 'xp_bonus', 'money_bonus', 'time_bonus']

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
        
        if OwnedItem.objects.filter(user=self.user, item=gear).exists():
            raise serializers.ValidationError("User already owns this gear.")
        
        if self.user.money < gear.cost:
            raise serializers.ValidationError("User does not have enough money to purchase this gear.")
        
        data['gear'] = gear
        return data


class UnownedGearSerializer(serializers.Serializer):
    '''
    Serializer to list all gear items not owned by the user.
    '''
    discord_id = serializers.CharField(max_length=255)

    def validate(self, data):
        discord_id = data.get('discord_id')

        # Get or create the user
        self.user, created = CustomUser.objects.get_or_create(
            discord_id=discord_id,
            defaults={
                "level": 1,
                "xp": 0,
                "money": 100,
            }
        )

        owned_gear_ids = OwnedItem.objects.filter(user=self.user).values_list('item_id', flat=True)

        unowned_gear = Gear.objects.exclude(id__in=owned_gear_ids)

        data['gear'] = unowned_gear
        return data


class OwnedGearSerializer(serializers.Serializer):
    '''
    Serializer to list all gear items owned by the user.
    '''
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

        owned_gear_ids = OwnedItem.objects.filter(user=self.user).values_list('item_id', flat=True)

        owned_gear = Gear.objects.filter(id__in=owned_gear_ids)
        if not owned_gear.exists():
            raise serializers.ValidationError("User does not own any gear.")

        data['gear'] = owned_gear
        return data

class BestGearSerializer(serializers.Serializer):
    '''
    Serializer to list the best gear owned by the user.
    '''
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

        owned_gear_ids = OwnedItem.objects.filter(user=self.user).values_list('item_id', flat=True)

        best_gear_xp = Gear.objects.filter(id__in=owned_gear_ids).order_by('-xp_bonus').first() or None
        best_gear_money = Gear.objects.filter(id__in=owned_gear_ids).order_by('-money_bonus').first() or None
        best_gear_time = Gear.objects.filter(id__in=owned_gear_ids).order_by('time_bonus').first() or None

        data['best_gear_xp'] = best_gear_xp
        data['best_gear_money'] = best_gear_money
        data['best_gear_time'] = best_gear_time
        return data