from rest_framework import viewsets
from .models import PantryItem, ShoppingList
from .serializers import PantryItemSerializer, ShoppingListSerializer

class PantryItemViewSet(viewsets.ModelViewSet):
    queryset = PantryItem.objects.all()
    serializer_class = PantryItemSerializer

class ShoppingListViewSet(viewsets.ModelViewSet):
    queryset = ShoppingList.objects.all()
    serializer_class = ShoppingListSerializer