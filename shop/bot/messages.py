TEXTS = {
    'welcome': {
        'uz': "Assalomu alaykum! Iltimos, tilni tanlang.",
        'ru': "Здравствуйте! Пожалуйста, выберите язык."
    },
    'ask_name': {
        'uz': "Ismingizni kiriting:",
        'ru': "Введите ваше имя:"
    },
    'ask_phone': {
        'uz': "Telefon raqamingizni yuboring. Buning uchun '📞 Telefon raqamni yuborish' tugmasini bosing.",
        'ru': "Отправьте свой номер телефона. Для этого нажмите кнопку '📞 Отправить номер телефона'."
    },
    'main_menu': {
        'uz': "Bosh menyu",
        'ru': "Главное меню"
    },
    'catalog': {
        'uz': "Katalog 🛍️",
        'ru': "Каталог 🛍️"
    },
    'cart': {
        'uz': "Savatcha 🛒",
        'ru': "Корзина 🛒"
    },
    'back': {
        'uz': "⬅️ Ortga",
        'ru': "⬅️ Назад"
    },
    'choose_category': {
        'uz': "Kategoriyani tanlang:",
        'ru': "Выберите категорию:"
    },
    'add_to_cart': {
        'uz': "🛒 Savatchaga qo'shish",
        'ru': "🛒 Добавить в корзину"
    },
    'added_to_cart': {
        'uz': "✅ Mahsulot savatchaga qo'shildi!",
        'ru': "✅ Товар добавлен в корзину!"
    },
    'cart_is_empty': {
        'uz': "Sizning savatchangiz bo'sh.",
        'ru': "Ваша корзина пуста."
    },
    'start_order': {
        'uz': "✅ Buyurtmani boshlash",
        'ru': "✅ Начать оформление заказа"
    },
    'order_started': {
        'uz': "✅ Buyurtmangiz qabul qilindi! Tez orada operatorimiz siz bilan bog'lanadi.",
        'ru': "✅ Ваш заказ принят! Наш оператор скоро свяжется с вами."
    }
}

def get_text(key, lang_code='uz'):
    return TEXTS.get(key, {}).get(lang_code, f"No text for '{key}' in '{lang_code}'")