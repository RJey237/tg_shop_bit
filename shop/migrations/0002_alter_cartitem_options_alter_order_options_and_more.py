# Generated by Django 5.2.3 on 2025-06-16 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cartitem',
            options={'verbose_name': 'Savatchadagi mahsulot', 'verbose_name_plural': 'Savatchadagi mashsulotlar'},
        ),
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': 'Buyurtma', 'verbose_name_plural': 'Buyurtmalar'},
        ),
        migrations.AlterModelOptions(
            name='telegramuser',
            options={'verbose_name': 'Telegram foydalanuvchisi', 'verbose_name_plural': 'Telegram foydalanuvchilari'},
        ),
        migrations.AlterModelOptions(
            name='variantimage',
            options={'verbose_name': "Variant sur'ati", 'verbose_name_plural': "Variant sur'atlari"},
        ),
        migrations.AlterField(
            model_name='product',
            name='main_image',
            field=models.ImageField(blank=True, null=True, upload_to='products/main/', verbose_name='Asosiy rasm'),
        ),
    ]
