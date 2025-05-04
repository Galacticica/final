"""
File: views.py
Author: Reagan Zierke
Date: 2025-04-27
Description: Views for the Users app.
This file contains the views for non-admin user-related operations such as viewing profile, level up, etc.
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import serializers as cereal
from .models import CustomUser

class GetProfileView(APIView):
    '''
    View to get or create a user.
    This view requires a discord_id in the request data.
    Admin command
    '''

    def post(self, request):
        discord_id = request.data.get('discord_id')
        username = request.data.get('username')
        if not discord_id:
            return Response({"error": "discord_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        user, created = CustomUser.objects.get_or_create(
            discord_id= discord_id,
            defaults={
                "username": username,
                "level": 1,
                "xp": 0,
                "money": 100,
            }
        )

        if not created and user.username != username:
            user.username = username
            user.save()

        serializer = cereal.CustomUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK if not created else status.HTTP_201_CREATED)

class LevelUpView(APIView):
    '''
    View to level up a user.
    This view requires a discord_id in the request data.
    It checks if the user has enough XP to level up and updates their level and XP accordingly.
    '''

    def post(self, request):
        discord_id = request.data.get('discord_id')

        if not discord_id:
            return Response({"error": "discord_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = cereal.LevelUpSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.user
            user.xp -= user.xp_needed
            user.level += 1
            user.save()
            new_xp_needed = user.xp_needed
            return Response({"message": f"Congratulations! You leveled up to level {user.level}.", "xp" : user.xp, "level" : user.level, "xp_needed" : new_xp_needed}, status=status.HTTP_200_OK)
        else:
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)