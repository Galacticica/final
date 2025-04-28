"""
File: views.py
Author: Reagan Zierke
Date: 2025-04-27
Description: Views for the Users app.
This file contains the views for user-related operations such as getting or creating a user,
giving money, coin flip betting, and deleting a user.
"""



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser
from . import serializers as cereal
import random


class GetOrCreateUserView(APIView):
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

class CoinFlipBetView(APIView):
    def post(self, request):
        s = cereal.CoinFlipBetSerializer(data=request.data)
        if s.is_valid():
            bet = s.data.get('bet')
            side = s.data.get('side')

            result = random.choice(["heads", "tails"])
            if result == side.lower():
                s.user.money += bet  
                message = f"You won! The coin landed on {result}. Your new balance is {s.user.money}."
            else:
                s.user.money -= bet 
                message = f"You lost! The coin landed on {result}. Your new balance is {s.user.money}."

            s.user.save()

            return Response({"message": message, "balance": s.user.money}, status=status.HTTP_200_OK)

        else:
            return Response({"error": s.errors}, status=status.HTTP_400_BAD_REQUEST)

class DeleteUserView(APIView):
    def delete(self, request):
        discord_id = request.data.get('discord_id')

        if not discord_id:
            return Response({"error": "discord_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        user = CustomUser.objects.filter(discord_id=discord_id).first()
        if not user:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        user.delete()
        return Response({"message": "User successfully deleted."}, status=status.HTTP_200_OK)


