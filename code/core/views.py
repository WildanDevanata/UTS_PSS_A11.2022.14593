from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Sum, Avg, Count, F, ExpressionWrapper, DecimalField
from .models import Admin, Category, Supplier, Item
from .serializers import AdminSerializer, CategorySerializer, SupplierSerializer, ItemSerializer

class AdminViewSet(viewsets.ModelViewSet):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

@api_view(['GET'])
def stock_summary(request):
    """
    Menampilkan ringkasan stok barang termasuk stok total, total nilai stok, dan rata-rata harga
    """
    total_items = Item.objects.count()
    total_stock = Item.objects.aggregate(total=Sum('quantity'))['total'] or 0
    
    total_value = Item.objects.annotate(
        value=ExpressionWrapper(F('price') * F('quantity'), output_field=DecimalField())
    ).aggregate(total=Sum('value'))['total'] or 0
    
    avg_price = Item.objects.aggregate(avg=Avg('price'))['avg'] or 0
    
    return Response({
        'total_items': total_items,
        'total_stock': total_stock,
        'total_value': total_value,
        'average_price': avg_price
    })

@api_view(['GET'])
def low_stock_items(request):
    """
    Menampilkan daftar barang yang stoknya di bawah ambang batas tertentu
    """
    threshold = int(request.query_params.get('threshold', 5))
    items = Item.objects.filter(quantity__lt=threshold)
    serializer = ItemSerializer(items, many=True)
    
    return Response({
        'threshold': threshold,
        'items_count': items.count(),
        'items': serializer.data
    })

@api_view(['GET'])
def items_by_category(request, category_id=None):
    """
    Menampilkan laporan barang berdasarkan kategori tertentu
    """
    if category_id:
        try:
            category = Category.objects.get(id=category_id)
            items = Item.objects.filter(category=category)
            serializer = ItemSerializer(items, many=True)
            
            return Response({
                'category': CategorySerializer(category).data,
                'items_count': items.count(),
                'items': serializer.data
            })
        except Category.DoesNotExist:
            return Response({'error': f'Category with id {category_id} does not exist'}, 
                           status=status.HTTP_404_NOT_FOUND)
    else:
        categories = Category.objects.all()
        result = []
        
        for category in categories:
            items = Item.objects.filter(category=category)
            result.append({
                'category': CategorySerializer(category).data,
                'items_count': items.count(),
                'items': ItemSerializer(items, many=True).data
            })
        
        return Response(result)

@api_view(['GET'])
def category_summary(request):
    """
    Menampilkan ringkasan per kategori
    """
    categories = Category.objects.all()
    result = []
    
    for category in categories:
        items = Item.objects.filter(category=category)
        items_count = items.count()
        
        total_value = items.annotate(
            value=ExpressionWrapper(F('price') * F('quantity'), output_field=DecimalField())
        ).aggregate(total=Sum('value'))['total'] or 0
        
        avg_price = items.aggregate(avg=Avg('price'))['avg'] or 0
        
        result.append({
            'category_id': category.id,
            'category_name': category.name,
            'items_count': items_count,
            'total_value': total_value,
            'average_price': avg_price
        })
    
    return Response(result)

@api_view(['GET'])
def supplier_summary(request):
    """
    Menampilkan ringkasan barang per pemasok
    """
    suppliers = Supplier.objects.all()
    result = []
    
    for supplier in suppliers:
        items = Item.objects.filter(supplier=supplier)
        items_count = items.count()
        
        total_value = items.annotate(
            value=ExpressionWrapper(F('price') * F('quantity'), output_field=DecimalField())
        ).aggregate(total=Sum('value'))['total'] or 0
        
        result.append({
            'supplier_id': supplier.id,
            'supplier_name': supplier.name,
            'items_count': items_count,
            'total_value': total_value
        })
    
    return Response(result)

@api_view(['GET'])
def system_summary(request):
    """
    Menampilkan ringkasan keseluruhan sistem
    """
    total_items = Item.objects.count()
    total_categories = Category.objects.count()
    total_suppliers = Supplier.objects.count()
    
    total_stock = Item.objects.aggregate(total=Sum('quantity'))['total'] or 0
    
    total_value = Item.objects.annotate(
        value=ExpressionWrapper(F('price') * F('quantity'), output_field=DecimalField())
    ).aggregate(total=Sum('value'))['total'] or 0
    
    return Response({
        'total_items': total_items,
        'total_categories': total_categories,
        'total_suppliers': total_suppliers,
        'total_stock': total_stock,
        'total_inventory_value': total_value
    })