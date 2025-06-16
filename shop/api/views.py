from rest_framework import viewsets
from shop.models import TelegramUser, Category, Product, Order,ProductVariant
from .serializers import TelegramUserSerializer, CategorySerializer, ProductSerializer, OrderSerializer,ProductVariantSerializer

class TelegramUserViewSet(viewsets.ModelViewSet):
    queryset = TelegramUser.objects.all()
    serializer_class = TelegramUserSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.prefetch_related('variants__images', 'categories').all()
    serializer_class = ProductSerializer

class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Order.objects.select_related('user').all()
    serializer_class = OrderSerializer

class ProductVariantViewSet(viewsets.ModelViewSet):
    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializer