from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Adventure
from . import serializers as cereal

class GetAdventuresView(APIView):
    def get(self, request):
        serializer = cereal.AdventureSerializer
        adventures = Adventure.objects.all()
        serialized_adventures = serializer(adventures, many=True)
        return Response(serialized_adventures.data, status=status.HTTP_200_OK)