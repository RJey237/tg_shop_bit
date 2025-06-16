import os
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, FSInputFile, InputMediaPhoto
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

from .states import Registration
from .messages import get_text
from .keyboards import (
    language_keyboard, phone_keyboard, main_menu_keyboard,
    categories_keyboard, products_keyboard, product_variant_keyboard,
    variant_confirmation_keyboard, cart_keyboard
)
from .db_helpers import (
    get_or_create_user, update_user_language, update_user_info, get_user_lang,
    get_root_categories, get_category_details, get_product_details, get_variant_details,
    add_to_cart, get_cart_items, delete_cart_item, create_order_and_clear_cart
)

router = Router()


# --- HELPER FUNCTIONS ---
async def show_category_content(bot: Bot, chat_id: int, message_id: int, cat_id: int, lang: str, is_edit: bool = True):
    details = await get_category_details(cat_id)
    if not details:
        return

    category, subcategories, products, parent_id = details.values()
    text = category.name_uz if lang == 'uz' else category.name_ru
    
    if subcategories:
        markup = categories_keyboard(subcategories, lang, parent_id=category.id)
    elif products:
        markup = products_keyboard(products, lang, parent_category_id=parent_id)
    else:
        markup = categories_keyboard([], lang, parent_id=parent_id)
        text += "\n(bo'sh)"
    
    if is_edit:
        try:
            await bot.edit_message_text(text=text, chat_id=chat_id, message_id=message_id, reply_markup=markup)
        except TelegramBadRequest: pass
    else:
        await bot.send_message(chat_id, text, reply_markup=markup)


# --- REGISTRATION AND MAIN MENU ---
@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    user, created = await get_or_create_user(message.from_user)
    if created or not user.phone_number:
        await message.answer(get_text('welcome'), reply_markup=language_keyboard())
        await state.set_state(Registration.choosing_language)
    else:
        await show_main_menu(message, user.language_code)

@router.callback_query(Registration.choosing_language, F.data.startswith('lang_'))
async def process_lang_select(callback: CallbackQuery, state: FSMContext):
    lang_code = callback.data.split('_')[1]
    await update_user_language(callback.from_user.id, lang_code)
    try:
        await callback.message.edit_text(get_text('ask_name', lang_code))
    except TelegramBadRequest: pass
    await state.set_state(Registration.entering_name)
    await callback.answer()

@router.message(Registration.entering_name)
async def process_get_name(message: Message, state: FSMContext):
    lang = await get_user_lang(message.from_user.id)
    await update_user_info(message.from_user.id, first_name=message.text)
    await message.answer(get_text('ask_phone', lang), reply_markup=phone_keyboard(lang))
    await state.set_state(Registration.entering_phone)

@router.message(Registration.entering_phone, F.contact)
async def process_get_phone(message: Message, state: FSMContext):
    user = await update_user_info(message.from_user.id, phone_number=message.contact.phone_number)
    await state.clear()
    await show_main_menu(message, user.language_code)

async def show_main_menu(message: Message, lang: str):
    await message.answer(get_text('main_menu', lang), reply_markup=main_menu_keyboard(lang))


# --- CATALOG AND NAVIGATION ---
@router.message(F.text.in_([get_text('catalog', 'uz'), get_text('catalog', 'ru')]))
async def process_catalog(message: Message):
    lang = await get_user_lang(message.from_user.id)
    categories = await get_root_categories()
    await message.answer(get_text('choose_category', lang), reply_markup=categories_keyboard(categories, lang))

@router.callback_query()
async def process_callbacks(callback: CallbackQuery, bot: Bot):
    user_id = callback.from_user.id
    lang = await get_user_lang(user_id)
    data = callback.data
    
    if data == "main_menu":
        await callback.answer()
        try: await callback.message.delete()
        except TelegramBadRequest: pass
        await show_main_menu(callback.message, lang)
        return

    elif data.startswith("cat:"):
        await callback.answer()
        cat_id = int(data.split(":")[1])
        await show_category_content(bot, user_id, callback.message.message_id, cat_id, lang)
        return

    elif data.startswith("back_cat:"):
        await callback.answer()
        parent_id_str = data.split(":")[1]
        if parent_id_str == 'None':
            text = get_text('choose_category', lang)
            markup = categories_keyboard(await get_root_categories(), lang, parent_id=None)
            try: await callback.message.edit_text(text, reply_markup=markup)
            except TelegramBadRequest: pass
        else:
            await show_category_content(bot, user_id, callback.message.message_id, int(parent_id_str), lang)
        return

    elif data.startswith("prod:"):
        await callback.answer()
        prod_id = int(data.split(":")[1])
        details = await get_product_details(prod_id)
        if not details: return
        
        product, variants, cat_id = details.values()
        text = product.name_uz if lang == 'uz' else product.name_ru
        markup = product_variant_keyboard(variants, lang, back_to_category_id=cat_id)
        
        try: await callback.message.delete()
        except TelegramBadRequest: pass
        if product.main_image and os.path.exists(product.main_image.path):
             await bot.send_photo(user_id, FSInputFile(product.main_image.path), caption=text, reply_markup=markup)
        else:
            await bot.send_message(user_id, text, reply_markup=markup)
        return

    elif data.startswith("view_variant:"):
        await callback.answer()
        variant_id = int(data.split(":")[1])
        details = await get_variant_details(variant_id)
        if not details: return

        variant, images = details.values()
        product = variant.product
        color_name = variant.color_name_uz if lang == 'uz' else variant.color_name_ru
        price = f"{variant.price:,.0f} UZS".replace(',', ' ')
        text = f"<b>{product.name_uz if lang == 'uz' else product.name_ru}</b>\n\nRang: {color_name}\nNarx: {price}"
        markup = variant_confirmation_keyboard(variant.id, product.id, lang)
        
        try: await callback.message.delete()
        except TelegramBadRequest: pass

        photo_to_send = None
        if images:
            for img in images:
                if os.path.exists(img.image.path):
                    photo_to_send = FSInputFile(img.image.path)
                    break
        
        if not photo_to_send and product.main_image and os.path.exists(product.main_image.path):
            photo_to_send = FSInputFile(product.main_image.path)

        if photo_to_send:
            await bot.send_photo(user_id, photo_to_send, caption=text, reply_markup=markup, parse_mode="HTML")
        else:
            await bot.send_message(user_id, text, reply_markup=markup, parse_mode="HTML")
        return

    elif data.startswith("back_prod:"):
        await callback.answer()
        cat_id = int(data.split(":")[1])
        try: await callback.message.delete()
        except TelegramBadRequest: pass
        await show_category_content(bot, user_id, 0, cat_id, lang, is_edit=False)
        return

    elif data.startswith("confirm_add:"):
        variant_id = int(data.split(":")[1])
        await add_to_cart(user_id, variant_id)
        await callback.answer(text=get_text('added_to_cart', lang), show_alert=True)
        return

    elif data.startswith("del_cart:"):
        await callback.answer()
        await delete_cart_item(user_id, int(data.split(":")[1]))
        await process_cart(callback, is_callback=True)
        return
    
    elif data == "start_order":
        created = await create_order_and_clear_cart(user_id)
        if created:
            await callback.answer(text=get_text('order_started', lang), show_alert=True)
            try: await callback.message.delete()
            except TelegramBadRequest: pass
            await show_main_menu(callback.message, lang)
        else:
            await callback.answer(text=get_text('cart_is_empty', lang), show_alert=True)
        return
    
    await callback.answer()


@router.message(F.text.in_([get_text('cart', 'uz'), get_text('cart', 'ru')]))
async def process_cart(message: Message | CallbackQuery, is_callback=False):
    if isinstance(message, CallbackQuery):
        user_id, msg_to_edit = message.from_user.id, message.message
    else:
        user_id, msg_to_edit = message.from_user.id, message
    
    lang = await get_user_lang(user_id)
    cart_items, total_price = await get_cart_items(user_id)

    if not cart_items:
        text, markup = get_text('cart_is_empty', lang), cart_keyboard([], lang)
    else:
        text_parts = [f"{get_text('cart', lang)}:\n"]
        for item in cart_items:
            prod_name = item.variant.product.name_uz if lang == 'uz' else item.variant.product.name_ru
            color_name = item.variant.color_name_uz if lang == 'uz' else item.variant.color_name_ru
            price = f"{item.variant.price:,.0f} UZS".replace(',', ' ')
            text_parts.append(f"🔹 {prod_name} ({color_name}) - {item.quantity} x {price}")
        text = "\n".join(text_parts)
        if total_price:
            text += f"\n\nJami: {f'{total_price:,.0f} UZS'.replace(',', ' ')}"
        markup = cart_keyboard(cart_items, lang)
    
    if is_callback:
        try: await msg_to_edit.edit_text(text, reply_markup=markup)
        except TelegramBadRequest: pass 
    else:
        await msg_to_edit.answer(text, reply_markup=markup)