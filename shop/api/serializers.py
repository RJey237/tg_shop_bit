from rest_framework import serializers
from shop.models import TelegramUser, Category, Product, ProductVariant, VariantImage, Order

class TelegramUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramUser
        fields = ['id', 'user_id', 'first_name', 'username', 'phone_number', 'language_code', 'is_active']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name_uz', 'name_ru', 'parent']

class VariantImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariantImage
        fields = ['id', 'image']

class ProductVariantSerializer(serializers.ModelSerializer):
    images = VariantImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = ProductVariant
        fields = ['id', 'product', 'color_name_uz', 'color_name_ru', 'price', 'images']

class ProductSerializer(serializers.ModelSerializer):
    variants = ProductVariantSerializer(many=True, read_only=True)
    categories = serializers.PrimaryKeyRelatedField(many=True, queryset=Category.objects.all())

    class Meta:
        model = Product
        fields = ['id', 'name_uz', 'name_ru', 'categories', 'main_image', 'variants']

class OrderSerializer(serializers.ModelSerializer):
    user = TelegramUserSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'created_at', 'is_processed']