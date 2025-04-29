"""
File: views.py
Author: Reagan Zierke
Date: 2025-04-27
Description: API views for the Adventure app.
This file contains views for getting a list of adventures, starting an adventure,
checking the status of an adventure, and completing an adventure.
"""



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Adventure
from . import serializers as cereal
from users.models import CurrentAdventure
from django.utils import timezone
import random

class GetAdventuresView(APIView):
    '''
    View to get a list of all adventures.
    '''

    def get(self, request):
        serializer = cereal.AdventureSerializer
        adventures = Adventure.objects.all()
        serialized_adventures = serializer(adventures, many=True)
        return Response(serialized_adventures.data, status=status.HTTP_200_OK)
    
class GetSpecificAdventureView(APIView):
    '''
    View to get a specific adventure by name.
    This view requires an adventure_name in the request data.
    '''

    def get(self, request):
        adventure_name = request.data.get('adventure_name').title()
        if not adventure_name:
            return Response({"error": "adventure_name is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = cereal.AdventureDetailSerializer(data=request.data)
        
        if serializer.is_valid():
            json_serializer = cereal.AdventureSerializer
            adventure = serializer.validated_data['adventure']
            serialized_adventure = json_serializer(adventure)
            return Response(serialized_adventure.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class StartAdventureView(APIView):
    '''
    View to start an adventure.
    This view requires a discord_id and adventure_name in the request data.
    It creates a new CurrentAdventure object for the user and returns its details.
    '''

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
    '''
    View to check the status of an adventure.
    This view requires a discord_id in the request data.
    It updates the time left for the adventure and returns its details.
    If the adventure is complete, it returns a message indicating completion.
    If the adventure is not complete, it returns the current status of the adventure.
    '''

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
    '''
    View to complete an adventure.
    This view requires a discord_id in the request data.
    It calculates the rewards for completing the adventure and updates the user's stats.
    It deletes the current adventure and returns the rewards.
    '''

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

            xp_reward = random.randint(adventure.xp_min, adventure.xp_max)
            money_reward = random.randint(adventure.reward_min, adventure.reward_max)

            critical_success = random.randint(0, 100)
            if critical_success < 5:
                xp_reward *= 2
                money_reward *= 2
                message = "Critical success! Double rewards!"
            elif critical_success < 10:
                xp_reward *= 1.5
                money_reward *= 1.5
                message = "Success! Rewards increased by 50%!"
            else:
                message = "Adventure completed successfully!"

            user.xp += xp_reward
            user.money += money_reward
            user.save()

            current_adventure.delete()

            return Response({
                "message": message,
                "adventure_name": adventure.name,
                "xp_reward": xp_reward,
                "money_reward": money_reward,
            }, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        