from rest_framework import serializers
from .models import Admin, Category, Supplier, Item

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ['id', 'username', 'email', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'created_by', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['id', 'name', 'contact_info', 'created_by', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class ItemSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    supplier_name = serializers.ReadOnlyField(source='supplier.name')
    
    class Meta:
        model = Item
        fields = ['id', 'name', 'description', 'price', 'quantity', 'category', 'category_name', 
                 'supplier', 'supplier_name', 'created_by', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']