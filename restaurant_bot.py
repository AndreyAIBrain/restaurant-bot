import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
import os
import time

# Инициализация бота
import os
TOKEN = os.getenv('TOKEN', "7634334499:AAFeR7PB0KTQHR74mPvehZlKaKFmRfk1fIM")
bot = telebot.TeleBot(TOKEN)

# Словарь для хранения корзин пользователей
user_carts = {}

# Словарь для отслеживания последних обработанных callback-запросов
processed_callbacks = {}

# Новый разделитель для callback-данных
CALLBACK_DELIM = "|||"

# Добавляем список для хранения id сообщений, отправленных ботом пользователю
user_message_ids = {}

# --- Новый словарь меню с id ---
CATEGORIES = {
    "soups": {"title": "🥣 Супы", "dishes": {
        "borscht": {"title": "🍜 Борщ", "img": "hot/Borscht Soup.jpg", "desc": "Борщ с говядиной — ароматный наваристый суп с сочными кусочками мяса, свежей капустой и свёклой, в насыщенном пряном бульоне. Подаётся со сметаной и зеленью. Настоящая классика русской кухни.", "price": 200, "emoji": "🥣"},
        "beetroot": {"title": "🥣 Свекольник", "img": "hot/Beetroot soup.jpg", "desc": "Свекольник классический — лёгкий и освежающий холодный суп на основе отварной свёклы, с хрустящими овощами и ароматной зеленью. Идеален для тёплой погоды. Подаётся со сметаной и яйцом.", "price": 150, "emoji": "🥣"},
        "okroshka": {"title": "🍲 Окрошка", "img": "hot/Okroshka soup.jpg", "desc": "Окрошка на кефире — лёгкий и освежающий холодный суп с хрустящими овощами, ароматной зеленью и нежным мясом. Идеальное блюдо для жаркого дня.", "price": 200, "emoji": "🥣"},
        "solyanka": {"title": "🫒 Солянка", "img": "hot/Solyanka soup.jpg", "desc": "Солянка с говядиной — густой пряный суп с нежными кусочками мяса, ароматом копчёностей, солёных огурцов и маслин. Богатый вкус с лёгкой остринкой. Подаётся с лимоном и сметаной. Настоящее удовольствие для ценителей русской кухни.", "price": 200, "emoji": "🥣"},
    }},
    "main": {"title": "🍖 Горячие блюда", "dishes": {
        "beef_goulash": {"title": "🥘 Говяжий гуляш", "img": "main/Beef goulash.jpg", "desc": "Гуляш из говядины — ароматное мясо в насыщенном соусе с пряностями, сытное и согревающее блюдо домашней кухни.", "price": 130, "emoji": "🍖"},
        "beef_patties": {"title": "🥩 Котлеты из говядины", "img": "main/Beef patties with gravy.jpg", "desc": "Нежнейшие котлеты из сочной говядины под ароматной подливой — сытное и домашнее блюдо, которое радует вкусом и уютом.", "price": 130, "emoji": "🍖"},
        "buckwheat_beef": {"title": "🥩 Гречка с говядиной", "img": "main/Buckwheat with beef patties and gravy.jpg", "desc": "Гречка с говяжьими котлетами и подливой — сытное и ароматное блюдо: рассыпчатая гречка, сочные котлеты из говядины и нежная домашняя подлива. Настоящая классика для вкусного обеда.", "price": 220, "emoji": "🍖"},
        "buckwheat_chicken": {"title": "🍗 Гречка с курицей", "img": "main/Buckwheat with chicken goulash.jpg", "desc": "Гречка с куриным гуляшом — нежное куриное филе в пряном соусе с рассыпчатой гречкой. Сытное и уютное блюдо для вкусного обеда.", "price": 220, "emoji": "🍗"},
        "mashed_beef": {"title": "🥩 Пюре с говядиной", "img": "main/Mashed potatoes with beef patties and gravy.jpg", "desc": "Картофельное пюре с котлетами из сочной говядины под нежной подливой — сытное и домашнее блюдо, которое дарит тепло и вкус детства.", "price": 220, "emoji": "🍖"},
        "mashed_chicken": {"title": "🍗 Пюре с курицей", "img": "main/Mashed potatoes with chicken goulash.jpg", "desc": "Пюре с куриным гуляшом — нежное картофельное пюре с сочным куриным филе в ароматном соусе. Вкусное и сытное блюдо домашней кухни.", "price": 220, "emoji": "🍗"},
        "mashed_gravy": {"title": "🥣 Пюре с подливой", "img": "main/Mashed potatoes with gravy.jpg", "desc": "Картофельное пюре с подливой из говядины — нежное пюре под насыщенным мясным соусом, согревающее и сытное блюдо домашней кухни.", "price": 220, "emoji": "🥣"},
        "mashed": {"title": "🥔 Пюре", "img": "main/Mashed potatoes.jpg", "desc": "Картофельное пюре — нежное и воздушное, приготовленное по классическому рецепту, идеальное дополнение к любому блюду.", "price": 100, "emoji": "🥔"},
        "buckwheat": {"title": "🌾 Гречка", "img": "main/Open buckwheat.jpg", "desc": "Гречка отварная — лёгкий и полезный гарнир с нежным вкусом и ароматом, идеально дополняющий любое блюдо.", "price": 100, "emoji": "🌾"},
        "spaghetti_beef": {"title": "🍝 Спагетти с говядиной", "img": "main/Spaghetti with beef patties and gravy.jpg", "desc": "Спагетти с сочными говяжьими котлетами и нежной подливой — сытное и аппетитное блюдо, которое дарит вкус домашнего уюта.", "price": 230, "emoji": "🍝"},
        "spaghetti_chicken": {"title": "🍗 Спагетти с курицей", "img": "main/Spaghetti with chicken goulash.jpg", "desc": "Спагетти с куриным гуляшом — нежная паста с сочным куриным филе в ароматном соусе. Сытное и аппетитное блюдо для настоящего домашнего обеда.", "price": 220, "emoji": "🍝"},
        "spaghetti_gravy": {"title": "🧆 Спагетти с подливой", "img": "main/Spaghetti with gravy (Спагетти с подливой из говядины).jpg", "desc": "Спагетти с подливой из говядины — нежная паста с насыщенным мясным соусом, сытное и вкусное блюдо домашнего уюта.", "price": 220, "emoji": "🍝"},
        "spaghetti": {"title": "🍝 Спагетти", "img": "main/Spaghetti.jpg", "desc": "Спагетти — нежные, идеально сваренные макароны, которые станут отличной основой для вашего любимого соуса или гарниром к любому блюду.", "price": 100, "emoji": "🍝"},
    }},
    "salads": {"title": "🥗 Салаты", "dishes": {
        "crab": {"title": "🦀 Крабовый салат", "img": "salads/Crab salad.jpg", "desc": "Крабовый салат — нежный и сочный, с крабовыми палочками, яйцом, кукурузой и свежим огурцом. Заправка придаёт блюду воздушную текстуру и тонкий вкус. Классика, которая всегда в удовольствии.", "price": 150, "emoji": "🥗"},
        "olivier": {"title": "🥚 Салат Оливье", "img": "salads/Olivier salad.jpg", "desc": "Салат Оливье с колбасой — аппетитный и сытный, с нежным картофелем, сочным огурчиком, зелёным горошком и ароматной колбасой. Классический вкус, знакомый и любимый с детства.", "price": 150, "emoji": "🥗"},
        "summer": {"title": "🥒 Летний салат", "img": "salads/Summer salad.jpg", "desc": "Летний салат с сладким луком, сочным перцем и спелыми томатами черри — свежий, яркий и ароматный. Лёгкая заправка подчёркивает натуральный вкус овощей. Настоящее наслаждение в каждом кусочке!", "price": 150, "emoji": "🥒"},
    }},
    "snacks": {"title": "🥪 Закуски", "dishes": {
        "nuggets": {"title": "🍗 Куриные наггетсы", "img": "snacks/Chicken nuggets.jpg", "desc": "Куриные наггетсы — хрустящие снаружи и сочные внутри, аппетитная закуска, любимая и взрослыми, и детьми.", "price": 100, "emoji": "🍗"},
        "greens": {"title": "🥬 Свежая зелень", "img": "snacks/Fresh greens.jpg", "desc": "Ассорти свежей зелени.", "price": 30, "emoji": "🥬"},
        "pickles": {"title": "🥒 Домашние солёные огурцы", "img": "snacks/Homemade pickled cucumbers.jpg", "desc": "Солёные огурцы собственного приготовления.", "price": 100, "emoji": "🥒"},
        "pancakes": {"title": "🥔 Драники", "img": "snacks/Potato pancakes.jpg", "desc": "Драники картофельные — золотистые, хрустящие снаружи и мягкие внутри, классические домашние лепёшки из тёртого картофеля.", "price": 100, "emoji": "🥔"},
    }},
    "drinks": {"title": "🥤 Напитки", "dishes": {
        "water": {"title": "💧 Вода", "img": "drinks/Water.jpg", "desc": "Питьевая вода без газа.", "price": 40, "emoji": "💧"},
        "coca_cola": {"title": "🥤 Кока-Кола", "img": "drinks/Coca-Cola.jpg", "desc": "Классическая Coca-Cola.", "price": 50, "emoji": "🥤"},
        "sprite": {"title": "🍐 Спрайт", "img": "drinks/Sprite.jpg", "desc": "Sprite", "price": 50, "emoji": "🥤"},
        "fanta": {"title": "🍊 Фанта", "img": "drinks/Fanta.jpg", "desc": "Fanta с апельсиновым вкусом.", "price": 50, "emoji": "🥤"},
        "mango_juice": {"title": "🥭 Манговый сок", "img": "drinks/MANGO JUICE.jpg", "desc": "Сок из манго.", "price": 140, "emoji": "🥭"},
        "passion_fruit_juice": {"title": "🥭 Сок маракуйи", "img": "drinks/PASSION FRUIT JUICE.jpg", "desc": "Сок из маракуйи.", "price": 140, "emoji": "🍹"},
        "tomato_juice": {"title": "🍅 Томатный сок", "img": "drinks/Tomato JUICE.jpg", "desc": "Томатный сок.", "price": 140, "emoji": "🍅"},
    }},
    "sauces": {"title": "🥫 Соусы", "dishes": {
        "ketchup": {"title": "🍅 Кетчуп", "img": "sauces/Ketchup.jpg", "desc": "Кетчуп томатный.", "price": 25, "emoji": "🥫"},
        "mayo": {"title": "🥚 Майонез", "img": "sauces/Mayonnaise.jpg", "desc": "Майонез классический.", "price": 25, "emoji": "🥛"},
        "sour_cream": {"title": "🥛 Сметана", "img": "sauces/Sour cream.jpg", "desc": "Сметана домашняя.", "price": 30, "emoji": "🥛"},
    }},
}

# --- Состояния пользователей для оформления заказа ---
user_states = {}
user_order_data = {}

# --- Вспомогательная функция для подсчёта суммы заказа ---
def get_cart_total(user_id):
    cart = get_user_cart(user_id)
    total = 0
    for item in cart:
        dish = CATEGORIES[item['cat_id']]['dishes'][item['dish_id']]
        if 'price' in dish:
            total += dish['price'] * item.get('count', 1)
    return total

# --- Современные inline-кнопки для каждого шага ---
def get_main_menu_inline():
    markup = InlineKeyboardMarkup(row_width=1)
    for cat_id, cat in CATEGORIES.items():
        markup.add(InlineKeyboardButton(cat['title'], callback_data=f"cat_{cat_id}"))
    markup.add(InlineKeyboardButton("────────────", callback_data="ignore"))
    markup.add(InlineKeyboardButton("🛒 Корзина", callback_data="view_cart"))
    markup.add(InlineKeyboardButton("◀️ Назад", callback_data="back_to_start"))
    return markup

def get_category_inline(cat_id):
    markup = InlineKeyboardMarkup(row_width=1)
    for dish_id, dish in CATEGORIES[cat_id]['dishes'].items():
        button_text = dish['title']
        markup.add(InlineKeyboardButton(button_text, callback_data=f"dish_{cat_id}_{dish_id}"))
    markup.add(InlineKeyboardButton("────────────", callback_data="ignore"))
    markup.add(InlineKeyboardButton("🛒 Корзина", callback_data="view_cart"))
    markup.add(InlineKeyboardButton("◀️ Назад", callback_data="back_to_main"))
    return markup

def get_dish_inline(cat_id, dish_id):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton("➕ Добавить в корзину", callback_data=f"add_{cat_id}_{dish_id}"))
    markup.add(InlineKeyboardButton("🛒 Корзина", callback_data="view_cart"))
    markup.add(InlineKeyboardButton("◀️ Назад", callback_data=f"back_from_photo_{cat_id}"))
    return markup

def get_cart_inline(user_id):
    markup = InlineKeyboardMarkup(row_width=1)
    cart = get_user_cart(user_id)
    if cart:
        markup.add(InlineKeyboardButton("✅ Оформить заказ", callback_data="place_order"))
        markup.add(InlineKeyboardButton("🗑️ Очистить корзину", callback_data="clear_cart"))
    markup.add(InlineKeyboardButton("◀️ Назад", callback_data="back_to_main"))
    return markup

def get_confirm_order_inline():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton("✅ Подтвердить заказ", callback_data="confirm_order"))
    markup.add(InlineKeyboardButton("⬅️ Назад", callback_data="view_cart"))
    return markup

def show_or_replace_message(bot, chat_id, message_id, text, reply_markup=None):
    try:
        bot.edit_message_text(text, chat_id, message_id, reply_markup=reply_markup)
    except Exception:
        try:
            bot.delete_message(chat_id, message_id)
        except Exception:
            pass
        sent = bot.send_message(chat_id, text, reply_markup=reply_markup)
        # Сохраняем id
        if chat_id not in user_message_ids:
            user_message_ids[chat_id] = []
        user_message_ids[chat_id].append(sent.message_id)

# Аналогично для send_photo:
def send_photo_and_save_id(chat_id, photo, caption, reply_markup=None):
    sent = bot.send_photo(chat_id, photo, caption=caption, reply_markup=reply_markup)
    if chat_id not in user_message_ids:
        user_message_ids[chat_id] = []
    user_message_ids[chat_id].append(sent.message_id)
    return sent

# --- Всплывающее уведомление для устаревших кнопок ---
def notify_stale_callback(call):
    bot.answer_callback_query(call.id, "Пожалуйста, используйте последние кнопки в чате!")

# --- Обновляем все callback-обработчики: если не удалось обработать (например, нет нужных данных), показываем уведомление ---
@bot.callback_query_handler(func=lambda call: call.data == "main_menu")
def show_main_menu_inline(call):
    show_or_replace_message(
        bot,
        call.message.chat.id,
        call.message.message_id,
        "Выберите категорию:",
        get_main_menu_inline()
    )
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data.startswith("cat_"))
def show_category_inline(call):
    delete_user_messages(call.message.chat.id)
    cat_id = call.data[4:]
    if cat_id in CATEGORIES:
        show_or_replace_message(
            bot,
            call.message.chat.id,
            call.message.message_id,
            f"Выберите блюдо из категории '{CATEGORIES[cat_id]['title']}':",
            get_category_inline(cat_id)
        )
        bot.answer_callback_query(call.id)
    else:
        bot.answer_callback_query(call.id, "Категория не найдена")

@bot.callback_query_handler(func=lambda call: call.data.startswith("dish_"))
def show_dish_inline(call):
    # Удаляем только меню категории (текущее сообщение)
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except Exception:
        pass
    _, cat_id, dish_id = call.data.split("_", 2)
    if cat_id in CATEGORIES and dish_id in CATEGORIES[cat_id]['dishes']:
        dish = CATEGORIES[cat_id]['dishes'][dish_id]
        full_path = os.path.join(os.getcwd(), dish['img'])
        if os.path.exists(full_path):
            caption = f"🍽️ {dish['title']}"
            if 'desc' in dish:
                caption += f"\n\n{dish['desc']}"
            if 'price' in dish:
                caption += f"\n\nЦена: {dish['price']} бат"
            with open(full_path, 'rb') as photo:
                markup = get_dish_inline(cat_id, dish_id)
                send_photo_and_save_id(call.message.chat.id, photo, caption=caption, reply_markup=markup)
        else:
            bot.answer_callback_query(call.id, f"Фото для блюда '{dish['title']}' не найдено")
    else:
        bot.answer_callback_query(call.id, "Блюдо не найдено")

@bot.callback_query_handler(func=lambda call: call.data == "view_cart")
def show_cart_inline(call):
    cart_text = get_cart_text(call.message.chat.id)
    markup = get_cart_inline(call.message.chat.id)
    show_or_replace_message(bot, call.message.chat.id, call.message.message_id, cart_text, markup)
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == "clear_cart")
def clear_cart_inline(call):
    clear_cart(call.message.chat.id)
    markup = get_cart_inline(call.message.chat.id)
    show_or_replace_message(bot, call.message.chat.id, call.message.message_id, "🛒 Ваша корзина пуста", markup)
    bot.answer_callback_query(call.id, "🗑️ Корзина очищена!")

@bot.callback_query_handler(func=lambda call: call.data == "place_order")
def place_order_inline(call):
    cart = get_user_cart(call.message.chat.id)
    if not cart:
        bot.answer_callback_query(call.id, "Корзина пуста!")
        return
    order_text = "📋 Ваш заказ:\n\n"
    total = 0
    total_count = 0
    for i, item in enumerate(cart, 1):
        cat = CATEGORIES[item['cat_id']]['title']
        dish = CATEGORIES[item['cat_id']]['dishes'][item['dish_id']]['title']
        price = CATEGORIES[item['cat_id']]['dishes'][item['dish_id']].get('price', 0)
        count = item.get('count', 1)
        subtotal = price * count
        total += subtotal
        total_count += count
        order_text += f"{i}. {dish} ({cat}) — {count} шт. × {price} = {subtotal} бат\n"
    order_text += f"\nВсего позиций: {len(cart)}"
    order_text += f"\nВсего блюд: {total_count}"
    order_text += f"\nИтого: {total} бат"
    markup = get_confirm_order_inline()
    show_or_replace_message(bot, call.message.chat.id, call.message.message_id, order_text, markup)
    bot.answer_callback_query(call.id)
    user_states[call.message.chat.id] = 'awaiting_confirm'

@bot.callback_query_handler(func=lambda call: call.data == "confirm_order")
def confirm_order_inline(call):
    # Удаляем все сообщения, кроме текущего
    chat_id = call.message.chat.id
    for msg_id in user_message_ids.get(chat_id, []):
        try:
            bot.delete_message(chat_id, msg_id)
        except Exception:
            pass
    user_message_ids[chat_id] = []
    user_states[chat_id] = 'awaiting_name'
    user_order_data[chat_id] = {}
    sent = bot.send_message(chat_id, "Пожалуйста, введите ваше имя:")
    user_message_ids[chat_id].append(sent.message_id)
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == "back_to_main")
def back_to_main_inline(call):
    delete_user_messages(call.message.chat.id)
    show_or_replace_message(
        bot,
        call.message.chat.id,
        call.message.message_id,
        "Выберите категорию:",
        get_main_menu_inline()
    )
    bot.answer_callback_query(call.id)

def send_add_to_cart_notification(call, dish_name, count, subtotal):
    bot.answer_callback_query(
        call.id,
        f"{dish_name} — {count} шт. в корзине (на {subtotal} бат)"
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith("add_"))
def add_to_cart_inline(call):
    # Не удаляем сообщения при добавлении блюда!
    _, cat_id, dish_id = call.data.split("_", 2)
    if cat_id in CATEGORIES and dish_id in CATEGORIES[cat_id]['dishes']:
        dish = CATEGORIES[cat_id]['dishes'][dish_id]
        dish_name = dish['title']
        add_to_cart(call.message.chat.id, cat_id, dish_id)
        cart = get_user_cart(call.message.chat.id)
        count = 1
        for item in cart:
            if item['cat_id'] == cat_id and item['dish_id'] == dish_id:
                count = item.get('count', 1)
                break
        price = dish.get('price', 0)
        subtotal = price * count
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(InlineKeyboardButton("➕ Добавить ещё", callback_data=f"add_{cat_id}_{dish_id}"))
        markup.add(InlineKeyboardButton("🛒 Корзина", callback_data="view_cart"))
        markup.add(InlineKeyboardButton("◀️ Назад", callback_data=f"back_from_photo_{cat_id}"))
        try:
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=markup)
        except Exception as e:
            pass  # Игнорируем ошибку, если разметка не изменилась
        bot.answer_callback_query(
            call.id,
            f"{dish_name} — {count} шт. в корзине (на {subtotal} бат)"
        )
    else:
        bot.answer_callback_query(call.id, "Ошибка при добавлении в корзину")

# --- Callback-обработчики для возврата назад из карточки блюда ---
@bot.callback_query_handler(func=lambda call: call.data.startswith("back_from_photo_"))
def back_from_photo_inline(call):
    # Удаляем только карточку блюда (текущее сообщение)
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except Exception:
        pass
    cat_id = call.data.replace("back_from_photo_", "")
    if cat_id in CATEGORIES:
        show_or_replace_message(
            bot,
            call.message.chat.id,
            call.message.message_id,
            f"Выберите блюдо из категории '{CATEGORIES[cat_id]['title']}':",
            get_category_inline(cat_id)
        )
        bot.answer_callback_query(call.id)
    else:
        bot.answer_callback_query(call.id, "Категория не найдена")

def get_menu_inline():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton("🍽️ Меню", callback_data="main_menu"))
    return markup

welcome_message_ids = {}

@bot.message_handler(commands=['start'])
def start(message):
    welcome_text = (
        "👋 Добро пожаловать!\n"
        "Ты в месте, где главное — вкус и уют домашней кухни.\n"
        "У нас тёплая атмосфера, щедрые порции и забота в каждом заказе 😋\n\n"
        "Спасибо, что выбрали нас! 🫶\n\n"
        "Нажмите кнопку Меню, чтобы посмотреть блюда!"
    )
    old_msg_id = welcome_message_ids.get(message.chat.id)
    if old_msg_id:
        try:
            bot.delete_message(message.chat.id, old_msg_id)
        except Exception:
            pass
    sent = bot.send_message(message.chat.id, welcome_text, reply_markup=get_menu_inline())
    welcome_message_ids[message.chat.id] = sent.message_id

@bot.callback_query_handler(func=lambda call: call.data == "back_to_start")
def back_to_start_inline(call):
    delete_user_messages(call.message.chat.id)
    welcome_text = (
        "👋 Добро пожаловать!\n"
        "Ты в месте, где главное — вкус и уют домашней кухни.\n"
        "У нас тёплая атмосфера, щедрые порции и забота в каждом заказе 😋\n\n"
        "Нажмите кнопку Меню, чтобы посмотреть блюда!"
    )
    show_or_replace_message(bot, call.message.chat.id, call.message.message_id, welcome_text, get_menu_inline())
    bot.answer_callback_query(call.id)

# --- Сбор данных пользователя после подтверждения заказа ---
@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == 'awaiting_name')
def get_name(message):
    user_order_data[message.chat.id]['name'] = message.text.strip()
    user_states[message.chat.id] = 'awaiting_location'
    # Кнопка для отправки геолокации + подсказка
    geo_markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    geo_markup.add(KeyboardButton('📍 Отправить геолокацию', request_location=True))
    bot.send_message(
        message.chat.id,
        "Пожалуйста, отправьте геолокацию доставки или напишите адрес текстом:\n\nЕсли не хотите отправлять геолокацию, просто напишите адрес текстом.",
        reply_markup=geo_markup
    )

@bot.message_handler(content_types=['location'])
def get_location(message):
    if user_states.get(message.chat.id) == 'awaiting_location':
        user_order_data[message.chat.id]['location'] = message.location
        user = message.from_user
        user_order_data[message.chat.id]['telegram_username'] = user.username or "Не указан"
        user_order_data[message.chat.id]['telegram_name'] = f"{user.first_name} {user.last_name or ''}".strip()
        name = user_order_data[message.chat.id].get('name', '-')
        telegram_username = user_order_data[message.chat.id].get('telegram_username', '-')
        telegram_name = user_order_data[message.chat.id].get('telegram_name', '-')
        location = user_order_data[message.chat.id].get('location', None)
        total = get_cart_total(message.chat.id)
        admin_ids = [7024016148, 6066191329]  # Список ID админов
        order_info = f"Новый заказ!\n\nИмя: {name}\nTelegram: @{telegram_username}\nПолное имя: {telegram_name}\n"
        cart = get_user_cart(message.chat.id)
        if cart:
            order_info += "\nСостав заказа:\n"
            for i, item in enumerate(cart, 1):
                cat = CATEGORIES[item['cat_id']]['title']
                dish = CATEGORIES[item['cat_id']]['dishes'][item['dish_id']]['title']
                price = CATEGORIES[item['cat_id']]['dishes'][item['dish_id']].get('price', 0)
                count = item.get('count', 1)
                subtotal = price * count
                order_info += f"{i}. {dish} ({cat}) — {count} шт. × {price} = {subtotal} бат\n"
            order_info += f"\nИтого: {total} бат"
        if location:
            order_info += f"\nГеолокация: {location.latitude}, {location.longitude}"
        clear_cart(message.chat.id)
        user_states.pop(message.chat.id, None)
        user_order_data.pop(message.chat.id, None)
        # Сначала благодарность, потом меню
        bot.send_message(
            message.chat.id,
            "Спасибо за заказ!\nСвяжемся с вами, для уточнения времени.\n\nПриятного аппетита!😋🤌🏼"
        )
        bot.send_message(
            message.chat.id,
            "Меню:",
            reply_markup=get_main_menu_inline()
        )
        for admin_id in admin_ids:
            bot.send_message(admin_id, order_info)
            if location:
                bot.send_location(admin_id, location.latitude, location.longitude)

# --- Новый обработчик для текстового адреса ---
@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == 'awaiting_location')
def get_text_address(message):
    user_order_data[message.chat.id]['address'] = message.text.strip()
    user = message.from_user
    user_order_data[message.chat.id]['telegram_username'] = user.username or "Не указан"
    user_order_data[message.chat.id]['telegram_name'] = f"{user.first_name} {user.last_name or ''}".strip()
    name = user_order_data[message.chat.id].get('name', '-')
    telegram_username = user_order_data[message.chat.id].get('telegram_username', '-')
    telegram_name = user_order_data[message.chat.id].get('telegram_name', '-')
    address = user_order_data[message.chat.id].get('address', '-')
    total = get_cart_total(message.chat.id)
    admin_ids = [7024016148, 6066191329]
    order_info = f"Новый заказ!\n\nИмя: {name}\nTelegram: @{telegram_username}\nПолное имя: {telegram_name}\n"
    cart = get_user_cart(message.chat.id)
    if cart:
        order_info += "\nСостав заказа:\n"
        for i, item in enumerate(cart, 1):
            cat = CATEGORIES[item['cat_id']]['title']
            dish = CATEGORIES[item['cat_id']]['dishes'][item['dish_id']]['title']
            price = CATEGORIES[item['cat_id']]['dishes'][item['dish_id']].get('price', 0)
            count = item.get('count', 1)
            subtotal = price * count
            order_info += f"{i}. {dish} ({cat}) — {count} шт. × {price} = {subtotal} бат\n"
        order_info += f"\nИтого: {total} бат"
    if address:
        order_info += f"\nАдрес: {address}"
    clear_cart(message.chat.id)
    user_states.pop(message.chat.id, None)
    user_order_data.pop(message.chat.id, None)
    bot.send_message(
        message.chat.id,
        "Спасибо за заказ!\nСвяжемся с вами, для уточнения времени.\n\nПриятного аппетита!😋🤌🏼"
    )
    bot.send_message(
        message.chat.id,
        "Меню:",
        reply_markup=get_main_menu_inline()
    )
    for admin_id in admin_ids:
        bot.send_message(admin_id, order_info)

# --- Удаление старых сообщений с меню/блюдом ---
def delete_user_messages(chat_id):
    for msg_id in user_message_ids.get(chat_id, []):
        try:
            bot.delete_message(chat_id, msg_id)
        except Exception:
            pass
    user_message_ids[chat_id] = []

# --- Корзина с поддержкой количества ---
def get_user_cart(user_id):
    if user_id not in user_carts:
        user_carts[user_id] = []
    return user_carts[user_id]

def add_to_cart(user_id, cat_id, dish_id):
    cart = get_user_cart(user_id)
    for item in cart:
        if item['cat_id'] == cat_id and item['dish_id'] == dish_id:
            item['count'] += 1
            user_carts[user_id] = cart
            return True
    cart.append({'cat_id': cat_id, 'dish_id': dish_id, 'count': 1})
    user_carts[user_id] = cart
    return True

def clear_cart(user_id):
    user_carts[user_id] = []

def get_cart_text(user_id):
    cart = get_user_cart(user_id)
    if not cart:
        return "🛒 Ваша корзина пуста"
    text = "🛒 Ваша корзина:\n\n"
    total = 0
    total_count = 0
    for i, item in enumerate(cart, 1):
        cat = CATEGORIES[item['cat_id']]['title']
        dish = CATEGORIES[item['cat_id']]['dishes'][item['dish_id']]['title']
        price = CATEGORIES[item['cat_id']]['dishes'][item['dish_id']].get('price', 0)
        count = item.get('count', 1)
        subtotal = price * count
        total += subtotal
        total_count += count
        text += f"{i}. {dish} ({cat}) — {count} шт. × {price} = {subtotal} бат\n"
    text += f"\nВсего позиций: {len(cart)}"
    text += f"\nВсего блюд: {total_count}"
    text += f"\nИтого: {total} бат"
    return text

# --- Запуск бота ---
if __name__ == "__main__":
    print("🍽️ Ресторанный бот запущен...")
    
    # Очищаем webhook перед запуском
    try:
        bot.delete_webhook()
        print("✅ Webhook очищен")
    except Exception as e:
        print(f"❌ Ошибка при очистке webhook: {e}")
    
    # Добавляем задержку перед запуском
    time.sleep(3)
    
    print("🚀 Запускаем бота в режиме polling...")
    
    # Простой запуск с обработкой ошибок
    try:
        bot.polling(none_stop=True, timeout=60)
    except KeyboardInterrupt:
        print("🛑 Бот остановлен пользователем")
    except Exception as e:
        error_msg = str(e)
        print(f"❌ Ошибка: {error_msg}")
        
        