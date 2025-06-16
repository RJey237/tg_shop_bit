from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from .messages import get_text

def language_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="🇺🇿 O'zbekcha", callback_data='lang_uz')
    builder.button(text="🇷🇺 Русский", callback_data='lang_ru')
    builder.adjust(2)
    return builder.as_markup()

def phone_keyboard(lang):
    builder = ReplyKeyboardBuilder()
    button_text = get_text('ask_phone', lang).split("'")[1] if "'" in get_text('ask_phone', lang) else "📞 Telefon raqamni yuborish"
    builder.button(text=button_text, request_contact=True)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)

def main_menu_keyboard(lang):
    builder = ReplyKeyboardBuilder()
    builder.button(text=get_text('catalog', lang))
    builder.button(text=get_text('cart', lang))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

def categories_keyboard(categories, lang, parent_id=None):
    builder = InlineKeyboardBuilder()
    for category in categories:
        name = category.name_uz if lang == 'uz' else category.name_ru
        builder.button(text=name, callback_data=f"cat:{category.id}")
    builder.adjust(2)
    back_button_data = f"back_cat:{parent_id}" if parent_id else "main_menu"
    builder.row(InlineKeyboardButton(text=get_text('back', lang), callback_data=back_button_data))
    return builder.as_markup()

def products_keyboard(products, lang, parent_category_id=None):
    builder = InlineKeyboardBuilder()
    for product in products:
        name = product.name_uz if lang == 'uz' else product.name_ru
        builder.button(text=name, callback_data=f"prod:{product.id}")
    builder.adjust(1)
    back_button_data = f"back_cat:{parent_category_id}" if parent_category_id is not None else "back_cat:None"
    builder.row(InlineKeyboardButton(text=get_text('back', lang), callback_data=back_button_data))
    return builder.as_markup()

def product_variant_keyboard(variants, lang, back_to_category_id=None):
    builder = InlineKeyboardBuilder()
    for variant in variants:
        name = variant.color_name_uz if lang == 'uz' else variant.color_name_ru
        price = f"{variant.price:,.0f} UZS".replace(',', ' ')
        builder.button(text=f"{name} - {price}", callback_data=f"view_variant:{variant.id}")
    builder.adjust(1)
    back_button_data = f"back_prod:{back_to_category_id}" if back_to_category_id else "main_menu"
    builder.row(InlineKeyboardButton(text=get_text('back', lang), callback_data=back_button_data))
    return builder.as_markup()

def variant_confirmation_keyboard(variant_id, product_id, lang):
    builder = InlineKeyboardBuilder()
    builder.button(
        text=get_text('add_to_cart', lang),
        callback_data=f"confirm_add:{variant_id}"
    )
    builder.row(InlineKeyboardButton(
        text=get_text('back', lang),
        callback_data=f"prod:{product_id}"
    ))
    return builder.as_markup()

def cart_keyboard(cart_items, lang):
    builder = InlineKeyboardBuilder()
    for item in cart_items:
        variant = item.variant
        prod_name = variant.product.name_uz if lang == 'uz' else variant.product.name_ru
        color_name = variant.color_name_uz if lang == 'uz' else variant.color_name_ru
        label = f"❌ {prod_name} ({color_name})"
        builder.button(text=label, callback_data=f"del_cart:{item.id}")
    builder.adjust(1)
    if cart_items:
        builder.row(InlineKeyboardButton(text=get_text('start_order', lang), callback_data="start_order"))
    builder.row(InlineKeyboardButton(text=get_text('back', lang), callback_data="main_menu"))
    return builder.as_markup()