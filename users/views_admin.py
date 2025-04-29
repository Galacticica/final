"""
File: admin_views.py
Author: Reagan Zierke
Date: 2025-04-27
Description: Admin views for the Users app.
This file contains views for admin-related operations such as giving money, giving XP, and deleting users.
"""



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser

    
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