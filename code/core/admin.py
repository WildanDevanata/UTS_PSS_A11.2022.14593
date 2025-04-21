# core/admin.py
from django.contrib import admin
from .models import Admin, Category, Supplier, Item

@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'created_at')
    search_fields = ('username', 'email')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by', 'created_at')
    search_fields = ('name',)

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_info', 'created_by', 'created_at')
    search_fields = ('name', 'contact_info')

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'category', 'supplier', 'created_by', 'created_at')
    list_filter = ('category', 'supplier')
    search_fields = ('name', 'description')