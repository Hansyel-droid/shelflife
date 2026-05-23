from django.contrib import admin
from .models import PantryItem, ShoppingList

@admin.register(PantryItem)
class PantryItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'quantity', 'unit', 'expiry_date', 'days_left']
    list_filter = ['category']
    search_fields = ['name']
    ordering = ['expiry_date']

    @admin.display(description='Days Left')
    def days_left(self, obj):
        return obj.days_until_expiry

@admin.register(ShoppingList)
class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'unit', 'purchased', 'added_at']
    list_filter = ['purchased', 'category']
    search_fields = ['name']