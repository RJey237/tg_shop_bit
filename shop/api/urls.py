from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TelegramUserViewSet, CategoryViewSet, ProductViewSet, OrderViewSet,ProductVariantViewSet

router = DefaultRouter()

router.register(r'users', TelegramUserViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'variants', ProductVariantViewSet)

urlpatterns = [
    path('', include(router.urls)),
]