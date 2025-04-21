# core/management/commands/seed_data.py
from django.core.management.base import BaseCommand
from core.models import Admin, Category, Supplier, Item
from django.db import transaction
import random

class Command(BaseCommand):
    help = 'Seed database with initial data'

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')
        
        # Hapus data lama
        Admin.objects.all().delete()
        Category.objects.all().delete()
        Supplier.objects.all().delete()
        Item.objects.all().delete()
        
        # Buat admin
        admin1 = Admin.objects.create(
            username='admin1',
            password='pbkdf2_sha256$600000$admin1password',  # Gunakan fungsi hash untuk password asli
            email='admin1@example.com'
        )
        
        admin2 = Admin.objects.create(
            username='admin2',
            password='pbkdf2_sha256$600000$admin2password',
            email='admin2@example.com'
        )
        
        # Buat kategori
        electronics = Category.objects.create(
            name='Electronics',
            description='Electronic items and gadgets',
            created_by=admin1
        )
        
        clothing = Category.objects.create(
            name='Clothing',
            description='Clothing and apparel items',
            created_by=admin1
        )
        
        food = Category.objects.create(
            name='Food',
            description='Food and beverage items',
            created_by=admin2
        )
        
        # Buat supplier
        supplier1 = Supplier.objects.create(
            name='Tech Suppliers Inc.',
            contact_info='tech@suppliers.com, 123-456-7890',
            created_by=admin1
        )
        
        supplier2 = Supplier.objects.create(
            name='Fashion World',
            contact_info='info@fashionworld.com, 098-765-4321',
            created_by=admin1
        )
        
        supplier3 = Supplier.objects.create(
            name='Food Distributors Ltd.',
            contact_info='orders@fooddist.com, 555-123-4567',
            created_by=admin2
        )
        
        # Buat items
        items_data = [
            {
                'name': 'Laptop',
                'description': 'High-performance laptop',
                'price': 1200.00,
                'quantity': 15,
                'category': electronics,
                'supplier': supplier1,
                'created_by': admin1
            },
            {
                'name': 'Smartphone',
                'description': 'Latest smartphone model',
                'price': 800.00,
                'quantity': 25,
                'category': electronics,
                'supplier': supplier1,
                'created_by': admin1
            },
            {
                'name': 'Tablet',
                'description': '10-inch tablet with stylus',
                'price': 450.00,
                'quantity': 8,
                'category': electronics,
                'supplier': supplier1,
                'created_by': admin2
            },
            {
                'name': 'T-shirt',
                'description': 'Cotton t-shirt, various colors',
                'price': 20.00,
                'quantity': 100,
                'category': clothing,
                'supplier': supplier2,
                'created_by': admin1
            },
            {
                'name': 'Jeans',
                'description': 'Blue denim jeans',
                'price': 45.00,
                'quantity': 30,
                'category': clothing,
                'supplier': supplier2,
                'created_by': admin2
            },
            {
                'name': 'Sweater',
                'description': 'Warm winter sweater',
                'price': 55.00,
                'quantity': 20,
                'category': clothing,
                'supplier': supplier2,
                'created_by': admin1
            },
            {
                'name': 'Rice',
                'description': 'Premium white rice, 5kg',
                'price': 10.00,
                'quantity': 50,
                'category': food,
                'supplier': supplier3,
                'created_by': admin2
            },
            {
                'name': 'Coffee',
                'description': 'Ground coffee, 500g',
                'price': 8.50,
                'quantity': 40,
                'category': food,
                'supplier': supplier3,
                'created_by': admin2
            },
            {
                'name': 'Chocolate',
                'description': 'Dark chocolate bars, pack of 10',
                'price': 15.00,
                'quantity': 25,
                'category': food,
                'supplier': supplier3,
                'created_by': admin1
            },
            {
                'name': 'Headphones',
                'description': 'Noise-cancelling headphones',
                'price': 150.00,
                'quantity': 4,
                'category': electronics,
                'supplier': supplier1,
                'created_by': admin1
            }
        ]
        
        for item_data in items_data:
            Item.objects.create(**item_data)
        
        self.stdout.write(self.style.SUCCESS('Successfully seeded database!'))