from rest_framework import serializers
from .models import PantryItem, ShoppingList

class PantryItemSerializer(serializers.ModelSerializer):
    is_expiring_soon = serializers.ReadOnlyField()
    is_expired = serializers.ReadOnlyField()
    days_until_expiry = serializers.ReadOnlyField()

    class Meta:
        model = PantryItem
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

class ShoppingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingList
        fields = '__all__'
        read_only_fields = ['added_at']