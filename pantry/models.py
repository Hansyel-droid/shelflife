from django.db import models
from django.utils import timezone
from datetime import timedelta


class Category(models.TextChoices):
    DAIRY      = 'dairy',      'Dairy'
    MEAT       = 'meat',       'Meat & Seafood'
    PRODUCE    = 'produce',    'Produce'
    GRAINS     = 'grains',     'Grains & Bread'
    FROZEN     = 'frozen',     'Frozen'
    CANNED     = 'canned',     'Canned & Jarred'
    CONDIMENTS = 'condiments', 'Condiments & Sauces'
    BEVERAGES  = 'beverages',  'Beverages'
    SNACKS     = 'snacks',     'Snacks'
    OTHER      = 'other',      'Other'


class PantryItem(models.Model):
    name        = models.CharField(max_length=200)
    category    = models.CharField(max_length=50, choices=Category.choices, default=Category.OTHER)
    expiry_date = models.DateField()
    quantity    = models.DecimalField(max_digits=10, decimal_places=2)
    unit        = models.CharField(max_length=50, default='pcs')
    notes       = models.TextField(blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['expiry_date']

    def __str__(self):
        return f'{self.name} ({self.quantity} {self.unit})'

    @property
    def is_expiring_soon(self):
        return self.expiry_date <= timezone.now().date() + timedelta(hours=48)

    @property
    def is_expired(self):
        return self.expiry_date < timezone.now().date()

    @property
    def days_until_expiry(self):
        return (self.expiry_date - timezone.now().date()).days


class ShoppingList(models.Model):
    name          = models.CharField(max_length=200)
    category      = models.CharField(max_length=50, choices=Category.choices, default=Category.OTHER)
    unit          = models.CharField(max_length=50, default='pcs')
    notes         = models.TextField(blank=True)
    added_at      = models.DateTimeField(auto_now_add=True)
    purchased     = models.BooleanField(default=False)
    original_item = models.ForeignKey(
        PantryItem, null=True, blank=True,
        on_delete=models.SET_NULL, related_name='shopping_entries'
    )

    class Meta:
        ordering = ['-added_at']

    def __str__(self):
        return f'[Shopping] {self.name}'