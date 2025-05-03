from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import serializers as cereal
from .models import Gear

class ShopListView(APIView):
    """
    View to list all gear items.
    """
    
    def get(self, request):
        """
        List all gear items.
        """

        gear_items = Gear.objects.all()
        serializer = cereal.ShopListSerializer(gear_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class GearDetailView(APIView):
    '''
    View to get details of a specific gear item.
    This view requires a gear_name in the request data.
    '''

    def get(self, request):
        gear_name = request.data.get('gear_name').title()
        if not gear_name:
            return Response({"error": "gear_name is required"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = cereal.GearDetailSerializer(data=request.data)
        
        if serializer.is_valid():
            json_serializer = cereal.ShopListSerializer
            print(serializer.validated_data)
            gear = serializer.validated_data['gear']
            serialized_gear = json_serializer(gear)
            return Response(serialized_gear.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class GearPurchaseView(APIView):
    '''
    View to handle gear purchase.
    This view requires a gear_name in the request data.
    '''

    def post(self, request):
        gear_name = request.data.get('gear_name').title()
        discord_id = request.data.get('discord_id')

        if not gear_name or not discord_id:
            return Response({"error": "gear_name and discord_id are required"}, status=status.HTTP_400_BAD_REQUEST)
    
        serializer = cereal.GearPurchaseSerializer(data=request.data)

        if serializer.is_valid():
            ...
