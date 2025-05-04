from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import serializers as cereal
from users.models import OwnedItem

class ShopListView(APIView):
    """
    View to list all gear items.
    """
    
    def get(self, request):
        """
        List all gear items.
        """

        discord_id = request.data.get('discord_id')

        if not discord_id:
            return Response({"error": "discord_id required"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = cereal.UnownedGearSerializer(data=request.data)
        if serializer.is_valid():
            gear = serializer.validated_data['gear']
            gear = sorted(gear, key=lambda item: item.cost)
            serialized_gear = cereal.ShopListSerializer(gear, many=True)
            return Response(serialized_gear.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
    
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
            user = serializer.user
            gear = serializer.validated_data['gear']

            user.money -= gear.cost
            user.save()

            OwnedItem.objects.create(user=user, item=gear)

            gear_serializer = cereal.ShopListSerializer(gear)
            return Response(gear_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class OwnedGearView(APIView):
    '''
    View to list all gear items owned by the user.
    This view requires a discord_id in the request data.
    '''

    def get(self, request):
        discord_id = request.data.get('discord_id')

        if not discord_id:
            return Response({"error": "discord_id required"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = cereal.OwnedGearSerializer(data=request.data)
        if serializer.is_valid():
            serialized_items = cereal.ShopListSerializer(serializer.validated_data['gear'], many=True)
            return Response(serialized_items.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BestGearView(APIView):
    '''
    View to list all gear items owned by the user.
    This view requires a discord_id in the request data.
    '''

    def get(self, request):
        discord_id = request.data.get('discord_id')

        if not discord_id:
            return Response({"error": "discord_id required"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = cereal.BestGearSerializer(data=request.data)
        if serializer.is_valid():
            best_gear_xp = cereal.ShopListSerializer(serializer.validated_data['best_gear_xp'])
            best_gear_money = cereal.ShopListSerializer(serializer.validated_data['best_gear_money'])
            best_gear_time = cereal.ShopListSerializer(serializer.validated_data['best_gear_time'])

            return Response({
                "best_gear_xp": best_gear_xp.data,
                "best_gear_money": best_gear_money.data,
                "best_gear_time": best_gear_time.data
            }, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
