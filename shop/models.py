from django.db import models

class TelegramUser(models.Model):
    user_id = models.BigIntegerField(unique=True, verbose_name="Telegram User ID")
    first_name = models.CharField(max_length=255, verbose_name="Ism")
    username = models.CharField(max_length=255, null=True, blank=True, verbose_name="Telegram Username")
    phone_number = models.CharField(max_length=20, null=True, blank=True, verbose_name="Telefon raqami")
    language_code = models.CharField(max_length=2, default='uz', choices=(('uz', "O'zbek"), ('ru', 'Русский')))
    is_active = models.BooleanField(default=True, verbose_name="Aktiv")

    def __str__(self):
        return self.first_name
    
    class Meta:
        verbose_name = "Telegram foydalanuvchisi"
        verbose_name_plural = "Telegram foydalanuvchilari"

class Category(models.Model):
    name_uz = models.CharField(max_length=255, verbose_name="Nomi (UZ)")
    name_ru = models.CharField(max_length=255, verbose_name="Nomi (RU)")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories')

    def __str__(self):
        return self.name_uz
    
    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"

class Product(models.Model):
    name_uz = models.CharField(max_length=255, verbose_name="Nomi (UZ)")
    name_ru = models.CharField(max_length=255, verbose_name="Nomi (RU)")
    categories = models.ManyToManyField(Category, related_name='products', verbose_name="Kategoriyalar")
    main_image = models.ImageField(upload_to='products/main/', verbose_name="Asosiy rasm",blank=True,null=True)

    def __str__(self):
        return self.name_uz

    class Meta:
        verbose_name = "Mahsulot"
        verbose_name_plural = "Mahsulotlar"

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    color_name_uz = models.CharField(max_length=100, verbose_name="Rang nomi (UZ)")
    color_name_ru = models.CharField(max_length=100, verbose_name="Rang nomi (RU)")
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Narx")

    def __str__(self):
        return f"{self.product.name_uz} - {self.color_name_uz}"

    class Meta:
        verbose_name = "Mahsulot varianti (rang)"
        verbose_name_plural = "Mahsulot variantlari (ranglar)"

class VariantImage(models.Model):
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/variants/')

    def __str__(self):
        return f"Rasm: {self.variant}"
    
    class Meta:
        verbose_name = "Variant sur'ati"
        verbose_name_plural = "Variant sur'atlari"

class CartItem(models.Model):
    user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE, related_name='cart_items')
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.user.first_name} savatchasi: {self.variant}"
    
    class Meta:
        verbose_name = "Savatchadagi mahsulot"
        verbose_name_plural = "Savatchadagi mashsulotlar"

class Order(models.Model):
    user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    is_processed = models.BooleanField(default=False)

    def __str__(self):
        return f"Buyurtma #{self.id} - {self.user.first_name}"
    
    class Meta:
        verbose_name = "Buyurtma"
        verbose_name_plural = "Buyurtmalar"
    
    