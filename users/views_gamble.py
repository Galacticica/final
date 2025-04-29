"""
File: gamble_views.py
Author: Reagan Zierke
Date: 2025-04-27
Description: Views for the Users app.
This file contains the views for gambling-related operations such as coin flip betting.
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import serializers as cereal
import random




class CoinFlipBetView(APIView):
    '''
    View to place a bet on a coin flip.
    This view requires a discord_id, bet amount, and side (heads or tails) in the request data.
    It checks if the user has enough money to place the bet and updates their balance accordingly.
    '''

    def post(self, request):
        discord_id = request.data.get('discord_id')

        if not discord_id:
            return Response({"error": "discord_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = cereal.CoinFlipBetSerializer(data=request.data)
        if serializer.is_valid():
            bet = serializer.data.get('bet')
            side = serializer.data.get('side')

            result = random.choice(["heads", "tails"])
            if result == side.lower():
                serializer.user.money += bet  
                message = f"You won! The coin landed on {result}. Your new balance is {serializer.user.money}."
            else:
                serializer.user.money -= bet 
                message = f"You lost! The coin landed on {result}. Your new balance is {serializer.user.money}."

            serializer.user.save()

            return Response({"message": message, "balance": serializer.user.money}, status=status.HTTP_200_OK)

        else:
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)