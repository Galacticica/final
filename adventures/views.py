from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Adventure
from . import serializers as cereal
from users.models import CustomUser, CurrentAdventure

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