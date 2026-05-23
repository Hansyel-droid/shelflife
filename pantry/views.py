from rest_framework import viewsets
from .models import PantryItem, ShoppingList
from .serializers import PantryItemSerializer, ShoppingListSerializer
import requests
from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets, permissions

class PantryItemViewSet(viewsets.ModelViewSet):
    serializer_class = PantryItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = PantryItem.objects.filter(user=self.request.user)
        category = self.request.query_params.get('category')
        search = self.request.query_params.get('search')
        if category: qs = qs.filter(category=category)
        if search: qs = qs.filter(name__icontains=search)
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ShoppingListViewSet(viewsets.ModelViewSet):
    serializer_class = ShoppingListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ShoppingList.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@api_view(['GET'])
def expiring_soon(request):
    deadline = timezone.now().date() + timedelta(hours=48)
    items = PantryItem.objects.filter(
        user=request.user,          # add this
        expiry_date__lte=deadline,
        expiry_date__gte=timezone.now().date(),
        quantity__gt=0
    )
    serializer = PantryItemSerializer(items, many=True)
    return Response({
        'count': items.count(),
        'deadline': str(deadline),
        'items': serializer.data,
    })
 
@api_view(['GET'])
def suggest_recipes(request):
    items = PantryItem.objects.filter(user=request.user, quantity__gt=0)
    if not items.exists():
        return Response({'error': 'Pantry is empty. Add items first.'}, status=400)

    ingredient_names = list(items.values_list('name', flat=True))
    api_key = settings.SPOONACULAR_API_KEY

    if not api_key:
        return Response({
            'note': 'Set SPOONACULAR_API_KEY in .env for live results.',
            'pantry_ingredients': ingredient_names,
            'recipes': [
                {'id': 1, 'title': 'Mock Stir Fry', 'usedIngredientCount': 3, 'missedIngredientCount': 1,
                 'missedIngredients': [{'name': 'soy sauce'}], 'usedIngredients': [{'name': n} for n in ingredient_names[:3]], 'image': ''},
                {'id': 2, 'title': 'Mock Pasta', 'usedIngredientCount': 2, 'missedIngredientCount': 2,
                 'missedIngredients': [{'name': 'pasta'}, {'name': 'olive oil'}], 'usedIngredients': [{'name': n} for n in ingredient_names[:2]], 'image': ''},
            ]
        })

    try:
        resp = requests.get(
            'https://api.spoonacular.com/recipes/findByIngredients',
            params={'apiKey': api_key, 'ingredients': ',+'.join(ingredient_names), 'number': 5, 'ranking': 1},
            timeout=10
        )
        resp.raise_for_status()
        return Response({'pantry_ingredients': ingredient_names, 'recipes': resp.json()})
    except requests.exceptions.Timeout:
        return Response({'error': 'Spoonacular timed out.'}, status=503)
    except requests.exceptions.HTTPError as e:
        return Response({'error': str(e)}, status=502)


    