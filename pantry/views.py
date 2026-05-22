from rest_framework import viewsets
from .models import PantryItem, ShoppingList
from .serializers import PantryItemSerializer, ShoppingListSerializer

class PantryItemViewSet(viewsets.ModelViewSet):
    queryset = PantryItem.objects.all()
    serializer_class = PantryItemSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        category = self.request.query_params.get('category')
        search = self.request.query_params.get('search')
        if category:
            qs = qs.filter(category=category)
        if search:
            qs = qs.filter(name__icontains=search)
        return qs

class ShoppingListViewSet(viewsets.ModelViewSet):
    queryset = ShoppingList.objects.all()
    serializer_class = ShoppingListSerializer