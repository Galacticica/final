"""
File: views.py
Author: Reagan Zierke
Date: 2025-04-27
Description: Views for the Users app.
This file contains the views for non-admin user-related operations such as giving money, coin flip betting, etc.
"""



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser
from . import serializers as cereal
import random


class GetOrCreateUserView(APIView):
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
    
class GiveMoneyView(APIView):
    '''
    View to give money to a user.
    This view requires a discord_id and amount in the request data.
    Admin command
    '''

    def post(self, request):
        discord_id = request.data.get('discord_id')
        amount = request.data.get('amount')

        if not discord_id or not amount:
            return Response({"error": "discord_id and amount are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            amount = int(amount)
            if amount <= 0:
                return Response({"error": "Amount must be a positive integer."}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({"error": "Amount must be an integer."}, status=status.HTTP_400_BAD_REQUEST)

        user = CustomUser.objects.filter(discord_id=discord_id).first()
        if not user:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        user.money += amount
        user.save()

        return Response({"message": f"Successfully added {amount} money to {user.username}'s account.", "balance": user.money}, status=status.HTTP_200_OK)
    
class GiveXPView(APIView):
    '''
    View to give XP to a user.
    This view requires a discord_id and amount in the request data.
    Admin command
    '''

    def post(self, request):
        discord_id = request.data.get('discord_id')
        amount = request.data.get('amount')

        if not discord_id or not amount:
            return Response({"error": "discord_id and amount are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            amount = int(amount)
            if amount <= 0:
                return Response({"error": "Amount must be a positive integer."}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({"error": "Amount must be an integer."}, status=status.HTTP_400_BAD_REQUEST)

        user = CustomUser.objects.filter(discord_id=discord_id).first()
        if not user:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        user.xp += amount
        user.save()

        return Response({"message": f"Successfully added {amount} xp to {user.username}'s account.", "xp": user.xp}, status=status.HTTP_200_OK)

class DeleteUserView(APIView):
    '''
    View to delete a user.
    This view requires a discord_id in the request data.
    Admin command
    '''

    def delete(self, request):
        discord_id = request.data.get('discord_id')

        if not discord_id:
            return Response({"error": "discord_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        user = CustomUser.objects.filter(discord_id=discord_id).first()
        if not user:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        user.delete()
        return Response({"message": "User successfully deleted."}, status=status.HTTP_200_OK)