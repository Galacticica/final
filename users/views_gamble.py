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
                win = True
            else:
                serializer.user.money -= bet 
                win= False

            serializer.user.save()

            return Response({"win": win, "balance": serializer.user.money, "result": result}, status=status.HTTP_200_OK)

        else:
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        

class SlotsView(APIView):
    '''
    View to play a slot machine game.
    This view requires a discord_id and bet amount in the request data.
    It checks if the user has enough money to place the bet and updates their balance accordingly.
    The slot machine uses a weighted random choice for the third slot to increase the chances of winning.
    '''

    def post(self, request):
        discord_id = request.data.get('discord_id')

        if not discord_id:
            return Response({"error": "discord_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = cereal.SlotsSerializer(data=request.data)
        if serializer.is_valid():
            bet = serializer.data.get('bet')
            emojis = ['🍒', '🍋', '🍉', '🔔', '💎', '7️⃣']
            weights = [0.25, 0.25, 0.25, 0.18, 0.06, 0.01]

            slot1 = random.choice(emojis)
            slot2 = random.choice(emojis)
            slot3 = random.choices(emojis, weights=weights, k=1)[0] 

            winning_combinations = {
                ('7️⃣', '7️⃣', '7️⃣'): 10,
                ('💎', '💎', '💎'): 5,
                ('🔔', '🔔', '🔔'): 4,
                ('🍉', '🍉', '🍉'): 3,
                ('🍋', '🍋', '🍋'): 3,
                ('🍒', '🍒', '🍒'): 3,
                ('🍒', '🍒'): 2,
            }

            if (slot1, slot2, slot3) in winning_combinations:
                win = True
                multiplier = winning_combinations[(slot1, slot2, slot3)]
            elif (slot1, slot2) in winning_combinations:
                win = True
                multiplier = winning_combinations[(slot1, slot2)]
            elif slot1 == slot2:
                win = True
                multiplier = 1.5
            else:
                win = False

            if win:
                serializer.user.money += int(bet * multiplier)
                serializer.user.save()
                message = f"Congratulations! You won {int(bet * multiplier)} coins!"
            else:
                serializer.user.money -= bet
                serializer.user.save()
                message = f"Sorry, you lost {bet} coins."
            
            print(f"User {discord_id} played slots: {slot1}, {slot2}, {slot3}. Result: {message}")
            return Response({"slots": [slot1, slot2, slot3], "message": message, "balance": serializer.user.money, "emojis": emojis, "win" : win}, status=status.HTTP_200_OK)

            

            
            




