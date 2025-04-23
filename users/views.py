from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser
from .serializers import CustomUserSerializer
import random


class GetOrCreateUserView(APIView):
    def post(self, request):
        discord_id = request.data.get('discord_id')
        username = request.data.get('username')
        if not discord_id:
            return Response({"error": "discord_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        user, created = CustomUser.objects.get_or_create(
            discord_id= discord_id,
            username = username,
            defaults={
                "level": 1,
                "xp": 0,
                "money": 100,
            }
        )

        serializer = CustomUserSerializer(user)
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
        discord_id = request.data.get('discord_id')
        username = request.data.get('username')
        bet = request.data.get('bet')
        side = request.data.get('side')

        if not discord_id or not bet or not side:
            return Response({"error": "discord_id, bet, and side are required"}, status=status.HTTP_400_BAD_REQUEST)

        if side.lower() not in ["heads", "tails"]:
            return Response({"error": "Invalid side. Choose 'heads' or 'tails'."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            bet = int(bet)
            if bet <= 0:
                return Response({"error": "Bet must be a positive integer."}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({"error": "Bet must be an integer."}, status=status.HTTP_400_BAD_REQUEST)

        # Get or create the user
        user, created = CustomUser.objects.get_or_create(
            discord_id=discord_id,
            defaults={
                "username": username,
                "level": 1,
                "xp": 0,
                "money": 100,
            }
        )

        if user.money < bet:
            return Response({"error": "Insufficient funds."}, status=status.HTTP_400_BAD_REQUEST)

        result = random.choice(["heads", "tails"])
        if result == side.lower():
            user.money += bet  
            message = f"You won! The coin landed on {result}. Your new balance is {user.money}."
        else:
            user.money -= bet 
            message = f"You lost! The coin landed on {result}. Your new balance is {user.money}."

        user.save()

        return Response({"message": message, "balance": user.money}, status=status.HTTP_200_OK)
