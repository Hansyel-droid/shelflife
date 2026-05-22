from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PantryItem, ShoppingList
 
@receiver(post_save, sender=PantryItem)
def move_to_shopping_list_when_empty(sender, instance, **kwargs):
    """
    Automatically creates a ShoppingList entry whenever a
    PantryItem's quantity is saved as 0 or below.
    Prevents duplicate entries.
    """
    if instance.quantity <= 0:
        already_listed = ShoppingList.objects.filter(
            name=instance.name, purchased=False
        ).exists()
        if not already_listed:
            ShoppingList.objects.create(
                name=instance.name,
                category=instance.category,
                unit=instance.unit,
                notes=f"Auto-added: '{instance.name}' ran out of stock.",
                original_item=instance,
            )
