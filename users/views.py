from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser
from .serializers import CustomUserSerializer


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
