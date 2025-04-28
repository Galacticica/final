from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Adventure
from . import serializers as cereal
from users.models import CustomUser, CurrentAdventure
from django.utils import timezone
import random

class GetAdventuresView(APIView):
    def get(self, request):
        serializer = cereal.AdventureSerializer
        adventures = Adventure.objects.all()
        serialized_adventures = serializer(adventures, many=True)
        return Response(serialized_adventures.data, status=status.HTTP_200_OK)
    
class StartAdventureView(APIView):
    def post(self, request):
        discord_id = request.data.get('discord_id')
        adventure_name = request.data.get('adventure_name').title()

        if not discord_id or not adventure_name:
            return Response({"error": "discord_id and adventure_name are required"}, status=status.HTTP_400_BAD_REQUEST)


        serializer = cereal.AdventureStartSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.user
            adventure = Adventure.objects.get(name=adventure_name)
            current_adventure = CurrentAdventure.objects.create(user=user, adventure=adventure, time_left=adventure.time_to_complete)
            current_adventure_serializer = cereal.CurrentAdventureSerializer(current_adventure)
            return Response(current_adventure_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class AdventureStatusView(APIView):
    def post(self, request):
        discord_id = request.data.get('discord_id')

        if not discord_id:
            return Response({"error": "discord_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        seralizer = cereal.AdventureStatusSerializer(data=request.data)

        if seralizer.is_valid():
            user = seralizer.user


            #Update the time left for the adventure
            current_adventure = CurrentAdventure.objects.filter(user=user).first()
            time_started = current_adventure.time_started
            current_time = timezone.now()
            time_left = current_adventure.time_left - int((current_time - time_started).total_seconds())
            current_adventure.time_left = time_left
            current_adventure.save()
            

            if current_adventure.time_left <= 0:
                return Response({'complete': True}, status=status.HTTP_200_OK)
            else:
                current_adventure_serializer = cereal.CurrentAdventureSerializer(current_adventure)
                return Response(current_adventure_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(seralizer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompleteAdventureView(APIView):
    def post(self, request):
        discord_id = request.data.get('discord_id')

        if not discord_id:
            return Response({"error": "discord_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = cereal.AdventureCompleteSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.user
            current_adventure = CurrentAdventure.objects.filter(user=user).first()

            if not current_adventure:
                return Response({"error": "User is not on an adventure."}, status=status.HTTP_400_BAD_REQUEST)

            adventure = current_adventure.adventure

            # Calculate rewards
            xp_reward = random.randint(adventure.xp_min, adventure.xp_max)
            money_reward = random.randint(adventure.reward_min, adventure.reward_max)

            # Update user stats
            user.xp += xp_reward
            user.money += money_reward
            user.save()

            # Delete the current adventure
            current_adventure.delete()

            return Response({
                "message": "Adventure completed successfully!",
                "adventure_name": adventure.name,
                "xp_reward": xp_reward,
                "money_reward": money_reward,
            }, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        