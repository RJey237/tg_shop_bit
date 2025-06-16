from asgiref.sync import sync_to_async
from shop.models import TelegramUser, Category, Product, CartItem, Order, ProductVariant

@sync_to_async
def get_or_create_user(user_data):
    user, created = TelegramUser.objects.get_or_create(
        user_id=user_data.id,
        defaults={'first_name': user_data.first_name, 'username': user_data.username}
    )
    return user, created

@sync_to_async
def update_user_language(user_id, lang_code):
    TelegramUser.objects.filter(user_id=user_id).update(language_code=lang_code)

@sync_to_async
def update_user_info(user_id, first_name=None, phone_number=None):
    user = TelegramUser.objects.get(user_id=user_id)
    if first_name:
        user.first_name = first_name
    if phone_number:
        user.phone_number = phone_number
    user.save()
    return user

@sync_to_async
def get_user_lang(user_id):
    return TelegramUser.objects.get(user_id=user_id).language_code

@sync_to_async
def get_root_categories():
    return list(Category.objects.filter(parent__isnull=True))

@sync_to_async
def get_category_details(cat_id):
    try:
        category = Category.objects.select_related('parent').get(id=cat_id)
        subcategories = list(category.subcategories.all())
        products = list(category.products.all())
        return {
            "category": category,
            "subcategories": subcategories,
            "products": products,
            "parent_id": category.parent.id if category.parent else None
        }
    except Category.DoesNotExist:
        return None

@sync_to_async
def get_product_details(prod_id):
    try:
        product = Product.objects.prefetch_related('variants', 'categories').get(id=prod_id)
        variants = list(product.variants.all())
        first_category = product.categories.first()
        return {
            "product": product,
            "variants": variants,
            "first_category_id": first_category.id if first_category else None
        }
    except Product.DoesNotExist:
        return None

@sync_to_async
def get_variant_details(variant_id):
    try:
        variant = ProductVariant.objects.select_related('product').prefetch_related('images').get(id=variant_id)
        images = list(variant.images.all())
        return {
            "variant": variant,
            "images": images
        }
    except ProductVariant.DoesNotExist:
        return None

@sync_to_async
def add_to_cart(user_id, variant_id):
    user = TelegramUser.objects.get(user_id=user_id)
    variant = ProductVariant.objects.get(id=variant_id)
    cart_item, created = CartItem.objects.get_or_create(user=user, variant=variant)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

@sync_to_async
def get_cart_items(user_id):
    from django.db.models import F, Sum
    user = TelegramUser.objects.get(user_id=user_id)
    items = list(CartItem.objects.filter(user=user).select_related('variant__product'))
    total = CartItem.objects.filter(user=user).aggregate(total=Sum(F('quantity') * F('variant__price')))['total']
    return items, total

@sync_to_async
def delete_cart_item(user_id, item_id):
    user = TelegramUser.objects.get(user_id=user_id)
    CartItem.objects.filter(id=item_id, user=user).delete()

@sync_to_async
def create_order_and_clear_cart(user_id):
    user = TelegramUser.objects.get(user_id=user_id)
    if CartItem.objects.filter(user=user).exists():
        Order.objects.create(user=user)
        CartItem.objects.filter(user=user).delete()
        return True
    return False