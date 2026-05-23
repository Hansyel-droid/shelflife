from django.core.management.base import BaseCommand
from pantry.models import PantryItem
from datetime import date, timedelta

class Command(BaseCommand):
    help = 'Seeds the database with sample pantry items for testing'

    def handle(self, *args, **kwargs):
        today = date.today()
        items = [
            {'name': 'Whole Milk',     'category': 'dairy',   'expiry_date': today + timedelta(days=1),   'quantity': 1,   'unit': 'L'},
            {'name': 'Greek Yogurt',   'category': 'dairy',   'expiry_date': today,                       'quantity': 2,   'unit': 'cups'},
            {'name': 'Chicken Breast', 'category': 'meat',    'expiry_date': today + timedelta(days=3),   'quantity': 500, 'unit': 'g'},
            {'name': 'Spinach',        'category': 'produce', 'expiry_date': today + timedelta(days=2),   'quantity': 1,   'unit': 'bag'},
            {'name': 'Cheddar Cheese', 'category': 'dairy',   'expiry_date': today + timedelta(days=10),  'quantity': 200, 'unit': 'g'},
            {'name': 'Pasta',          'category': 'grains',  'expiry_date': today + timedelta(days=365), 'quantity': 500, 'unit': 'g'},
            {'name': 'Eggs',           'category': 'dairy',   'expiry_date': today + timedelta(days=14),  'quantity': 6,   'unit': 'pcs'},
            {'name': 'Tomatoes',       'category': 'produce', 'expiry_date': today + timedelta(days=5),   'quantity': 4,   'unit': 'pcs'},
        ]
        count = 0
        for i in items:
            _, created = PantryItem.objects.get_or_create(name=i['name'], defaults=i)
            if created:
                count += 1
        self.stdout.write(self.style.SUCCESS(f'Seeded {count} new items.'))