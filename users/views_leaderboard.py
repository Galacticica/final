from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import serializers as cereal
from .models import CustomUser

class LevelLeaderboardView(APIView):
    '''
    View to get the top 10 users by level.
    This view returns a list of the top 10 users sorted by their level in descending order.
    '''

    def get(self, request):
        users = CustomUser.objects.all().order_by('-level')
        users = users[:10]
        serializer = cereal.CustomUserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class MoneyLeaderboardView(APIView):
    '''
    View to get the top 10 users by money.
    This view returns a list of the top 10 users sorted by their level in descending order.
    '''

    def get(self, request):
        users = CustomUser.objects.all().order_by('-money')
        users = users[:10]
        serializer = cereal.CustomUserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)