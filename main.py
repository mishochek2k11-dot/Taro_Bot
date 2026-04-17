from http.server import BaseHTTPRequestHandler
import json
import requests
import random
from datetime import datetime, timedelta
import os
from supabase import create_client, Client

# ===== ВСТАВЬ СВОИ ДАННЫЕ =====
BOT_TOKEN = "8279893361:AAF5MW-v6m-JIMI0-pWSXf1yZlY963j5Oyw"
ADMIN_ID = "6180185234"
# ==============================

FREE_ATTEMPTS = 3

# Supabase (переменные из Vercel)
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

# Проверяем, есть ли Supabase
USE_SUPABASE = SUPABASE_URL and SUPABASE_KEY
if USE_SUPABASE:
    try:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        # Тестовый запрос
        supabase.table("users").select("*").limit(1).execute()
        print("Supabase connected")
    except Exception as e:
        print(f"Supabase connection error: {e}")
        USE_SUPABASE = False
else:
    print("Supabase not configured, using memory storage")

# Хранилище в памяти (если Supabase не работает)
users = {}

CARDS = [
    {"name": "Шут", "img": "00-TheFool.png", "description": "Тебя ждёт новое начало."},
    {"name": "Маг", "img": "01-TheMagician.png", "description": "У тебя есть все ресурсы."},
    {"name": "Верховная Жрица", "img": "02-TheHighPriestess.png", "description": "Прислушайся к интуиции."},
    {"name": "Императрица", "img": "03-TheEmpress.png", "description": "Время созидания."},
    {"name": "Император", "img": "04-TheEmperor.png", "description": "Нужна структура."},
    {"name": "Иерофант", "img": "05-TheHierophant.png", "description": "Обратись к наставнику."},
    {"name": "Влюблённые", "img": "06-TheLovers.png", "description": "Важный выбор."},
    {"name": "Колесница", "img": "07-TheChariot.png", "description": "Победа близка."},
    {"name": "Сила", "img": "08-Strength.png", "description": "Внутренняя сила."},
    {"name": "Отшельник", "img": "09-TheHermit.png", "description": "Время уединения."},
    {"name": "Колесо Фортуны", "img": "10-WheelOfFortune.png", "description": "Жизнь готовит поворот."},
    {"name": "Справедливость", "img": "11-Justice.png", "description": "Всё вернётся."},
    {"name": "Повешенный", "img": "12-TheHangedMan.png", "description": "Отпусти ситуацию."},
    {"name": "Смерть", "img": "13-Death.png", "description": "Конец и новое начало."},
    {"name": "Умеренность", "img": "14-Temperance.png", "description": "Найди баланс."},
    {"name": "Дьявол", "img": "15-TheDevil.png", "description": "Освободись."},
    {"name": "Башня", "img": "16-TheTower.png", "description": "Крах старого."},
    {"name": "Звезда", "img": "17-TheStar.png", "description": "Надежда."},
    {"name": "Луна", "img": "18-TheMoon.png", "description": "Не всё так, как кажется."},
    {"name": "Солнце", "img": "19-TheSun.png", "description": "Радость и успех."},
    {"name": "Суд", "img": "20-Judgement.png", "description": "Подведи итоги."},
    {"name": "Мир", "img": "21-TheWorld.png", "description": "Цикл завершён."},
    {"name": "Туз Жезлов", "img": "Wands01.png", "description": "Новая энергия."},
    {"name": "Двойка Жезлов", "img": "Wands02.png", "description": "Планирование."},
    {"name": "Тройка Жезлов", "img": "Wands03.png", "description": "Прогресс."},
    {"name": "Четвёрка Жезлов", "img": "Wands04.png", "description": "Праздник."},
    {"name": "Пятёрка Жезлов", "img": "Wands05.png", "description": "Конфликт."},
    {"name": "Шестёрка Жезлов", "img": "Wands06.png", "description": "Победа."},
    {"name": "Семёрка Жезлов", "img": "Wands07.png", "description": "Защита."},
    {"name": "Восьмёрка Жезлов", "img": "Wands08.png", "description": "Скорость."},
    {"name": "Девятка Жезлов", "img": "Wands09.png", "description": "Почти у цели."},
    {"name": "Десятка Жезлов", "img": "Wands10.png", "description": "Перегрузка."},
    {"name": "Паж Жезлов", "img": "Wands11.png", "description": "Новые идеи."},
    {"name": "Рыцарь Жезлов", "img": "Wands12.png", "description": "Страсть."},
    {"name": "Королева Жезлов", "img": "Wands13.png", "description": "Уверенность."},
    {"name": "Король Жезлов", "img": "Wands14.png", "description": "Лидерство."},
    {"name": "Туз Кубков", "img": "Cups01.png", "description": "Новая любовь."},
    {"name": "Двойка Кубков", "img": "Cups02.png", "description": "Союз."},
    {"name": "Тройка Кубков", "img": "Cups03.png", "description": "Дружба."},
    {"name": "Четвёрка Кубков", "img": "Cups04.png", "description": "Апатия."},
    {"name": "Пятёрка Кубков", "img": "Cups05.png", "description": "Потеря."},
    {"name": "Шестёрка Кубков", "img": "Cups06.png", "description": "Ностальгия."},
    {"name": "Семёрка Кубков", "img": "Cups07.png", "description": "Иллюзии."},
    {"name": "Восьмёрка Кубков", "img": "Cups08.png", "description": "Уход."},
    {"name": "Девятка Кубков", "img": "Cups09.png", "description": "Исполнение желаний."},
    {"name": "Десятка Кубков", "img": "Cups10.png", "description": "Счастье."},
    {"name": "Паж Кубков", "img": "Cups11.png", "description": "Предложение."},
    {"name": "Рыцарь Кубков", "img": "Cups12.png", "description": "Романтика."},
    {"name": "Королева Кубков", "img": "Cups13.png", "description": "Мудрость."},
    {"name": "Король Кубков", "img": "Cups14.png", "description": "Зрелость."},
    {"name": "Туз Мечей", "img": "Swords01.png", "description": "Ясность."},
    {"name": "Двойка Мечей", "img": "Swords02.png", "description": "Тупик."},
    {"name": "Тройка Мечей", "img": "Swords03.png", "description": "Боль."},
    {"name": "Четвёрка Мечей", "img": "Swords04.png", "description": "Отдых."},
    {"name": "Пятёрка Мечей", "img": "Swords05.png", "description": "Конфликт."},
    {"name": "Шестёрка Мечей", "img": "Swords06.png", "description": "Переход."},
    {"name": "Семёрка Мечей", "img": "Swords07.png", "description": "Хитрость."},
    {"name": "Восьмёрка Мечей", "img": "Swords08.png", "description": "Ограничения."},
    {"name": "Девятка Мечей", "img": "Swords09.png", "description": "Тревога."},
    {"name": "Десятка Мечей", "img": "Swords10.png", "description": "Крах."},
    {"name": "Паж Мечей", "img": "Swords11.png", "description": "Любопытство."},
    {"name": "Рыцарь Мечей", "img": "Swords12.png", "description": "Решительность."},
    {"name": "Королева Мечей", "img": "Swords13.png", "description": "Честность."},
    {"name": "Король Мечей", "img": "Swords14.png", "description": "Интеллект."},
    {"name": "Туз Пентаклей", "img": "Pentacles01.png", "description": "Ресурсы."},
    {"name": "Двойка Пентаклей", "img": "Pentacles02.png", "description": "Баланс."},
    {"name": "Тройка Пентаклей", "img": "Pentacles03.png", "description": "Мастерство."},
    {"name": "Четвёрка Пентаклей", "img": "Pentacles04.png", "description": "Контроль."},
    {"name": "Пятёрка Пентаклей", "img": "Pentacles05.png", "description": "Трудности."},
    {"name": "Шестёрка Пентаклей", "img": "Pentacles06.png", "description": "Помощь."},
    {"name": "Семёрка Пентаклей", "img": "Pentacles07.png", "description": "Терпение."},
    {"name": "Восьмёрка Пентаклей", "img": "Pentacles08.png", "description": "Усердие."},
    {"name": "Девятка Пентаклей", "img": "Pentacles09.png", "description": "Уют."},
    {"name": "Десятка Пентаклей", "img": "Pentacles10.png", "description": "Богатство."},
    {"name": "Паж Пентаклей", "img": "Pentacles11.png", "description": "Обучение."},
    {"name": "Рыцарь Пентаклей", "img": "Pentacles12.png", "description": "Упорство."},
    {"name": "Королева Пентаклей", "img": "Pentacles13.png", "description": "Забота."},
    {"name": "Король Пентаклей", "img": "Pentacles14.png", "description": "Процветание."}
]

def get_card():
    return random.choice(CARDS)

def send_photo(chat_id, image_name, caption, description):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    image_url = f"https://raw.githubusercontent.com/mishochek2k11-dot/Taro_Bot/main/images/{image_name}"
    full_text = f"🔮 **{caption}**\n\n{description}"
    requests.post(url, json={"chat_id": chat_id, "photo": image_url, "caption": full_text, "parse_mode": "Markdown"}, timeout=10)

def send_message(chat_id, text, keyboard=None):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    if keyboard:
        data["reply_markup"] = json.dumps({"inline_keyboard": keyboard})
    requests.post(url, json=data, timeout=10)

def edit_message(chat_id, message_id, text, keyboard=None):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/editMessageText"
    data = {"chat_id": chat_id, "message_id": message_id, "text": text, "parse_mode": "Markdown"}
    if keyboard:
        data["reply_markup"] = json.dumps({"inline_keyboard": keyboard})
    requests.post(url, json=data, timeout=10)

def is_admin(user_id):
    return str(user_id) == ADMIN_ID

def get_user(user_id):
    if not USE_SUPABASE:
        return users.get(user_id)
    try:
        result = supabase.table("users").select("*").eq("user_id", user_id).execute()
        return result.data[0] if result.data else None
    except Exception as e:
        print(f"Supabase get error: {e}")
        return None

def create_user(user_id):
    now = datetime.now()
    current_month = now.strftime("%Y-%m")
    user_data = {
        "user_id": user_id,
        "attempts": 0,
        "extra": 0,
        "premium": False,
        "premium_until": None,
        "month": current_month,
        "total_readings": 0
    }
    if not USE_SUPABASE:
        users[user_id] = user_data
        return user_data
    try:
        supabase.table("users").insert(user_data).execute()
        return user_data
    except Exception as e:
        print(f"Supabase create error: {e}")
        return None

def update_user(user_id, data):
    if not USE_SUPABASE:
        if user_id in users:
            users[user_id].update(data)
        return
    try:
        supabase.table("users").update(data).eq("user_id", user_id).execute()
    except Exception as e:
        print(f"Supabase update error: {e}")

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is alive")
    
    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        data = self.rfile.read(length)
        
        try:
            update = json.loads(data)
            
            if "message" in update:
                chat_id = update["message"]["chat"]["id"]
                text = update["message"].get("text", "")
                user_id = str(update["message"]["from"]["id"])
                
                if is_admin(user_id):
                    if text == "/start":
                        keyboard = [
                            [{"text": "🔮 Расклад на жизнь", "callback_data": "life"}],
                            [{"text": "❤️ Расклад на отношения", "callback_data": "love"}],
                            [{"text": "💼 Расклад на работу", "callback_data": "work"}],
                            [{"text": "🛒 Магазин", "callback_data": "shop"}],
                            [{"text": "📊 Статус", "callback_data": "status"}]
                        ]
                        send_message(chat_id, "✨ Привет, создатель! Режим админа — безлимитные расклады.", keyboard)
                    elif text == "/buy":
                        keyboard = [
                            [{"text": "📦 5 попыток — 20 ⭐️", "callback_data": "buy_5"}],
                            [{"text": "📦 10 попыток — 45 ⭐️", "callback_data": "buy_10"}],
                            [{"text": "🌟 Премиум на месяц — 75 ⭐️", "callback_data": "buy_premium"}],
                            [{"text": "🔙 Назад", "callback_data": "back"}]
                        ]
                        send_message(chat_id, "🛒 **Магазин**\n\nВыбери вариант:", keyboard)
                    elif text == "/status":
                        send_message(chat_id, "📊 **Статус админа**\n\n🌟 Безлимитные расклады")
                    elif text == "/stats":
                        send_message(chat_id, "📈 **Статистика админа**\n\nСоздатель бота, безлимит.")
                    else:
                        send_message(chat_id, "❌ Неизвестная команда. Используй /start")
                    return
                
                user = get_user(user_id)
                if not user:
                    user = create_user(user_id)
                
                if not user:
                    send_message(chat_id, "❌ Ошибка базы данных. Попробуй позже.")
                    return
                
                now = datetime.now()
                current_month = now.strftime("%Y-%m")
                
                if user.get("premium") and user.get("premium_until"):
                    if now > datetime.fromisoformat(user["premium_until"]):
                        update_user(user_id, {"premium": False, "premium_until": None})
                        user["premium"] = False
                        user["premium_until"] = None
                
                if user.get("month") != current_month and not user.get("premium"):
                    update_user(user_id, {"attempts": 0, "month": current_month})
                    user["attempts"] = 0
                    user["month"] = current_month
                
                if text == "/start":
                    keyboard = [
                        [{"text": "🔮 Расклад на жизнь", "callback_data": "life"}],
                        [{"text": "❤️ Расклад на отношения", "callback_data": "love"}],
                        [{"text": "💼 Расклад на работу", "callback_data": "work"}],
                        [{"text": "🛒 Магазин", "callback_data": "shop"}],
                        [{"text": "📊 Статус", "callback_data": "status"}]
                    ]
                    welcome_text = (
                        "✨ **Добро пожаловать в бота Таро!** ✨\n\n"
                        "📋 **Доступные команды:**\n"
                        "/start — показать это сообщение\n"
                        "/buy — открыть магазин попыток и премиум\n"
                        "/status — проверить статус подписки и остаток попыток\n"
                        "/stats — посмотреть статистику (сколько раскладов сделано)\n\n"
                        "🔥 У тебя 3 бесплатных расклада в месяц.\n"
                        "🌟 Премиум-подписка даёт безлимит.\n\n"
                        "👇 **Выбери тему расклада:**"
                    )
                    send_message(chat_id, welcome_text, keyboard)
                
                elif text == "/buy":
                    keyboard = [
                        [{"text": "📦 5 попыток — 20 ⭐️", "callback_data": "buy_5"}],
                        [{"text": "📦 10 попыток — 45 ⭐️", "callback_data": "buy_10"}],
                        [{"text": "🌟 Премиум на месяц — 75 ⭐️", "callback_data": "buy_premium"}],
                        [{"text": "🔙 Назад", "callback_data": "back"}]
                    ]
                    send_message(chat_id, "🛒 **Магазин**\n\nВыбери вариант:", keyboard)
                
                elif text == "/status":
                    if user.get("premium"):
                        until = user["premium_until"].split("T")[0] if user.get("premium_until") else "неизвестно"
                        text_status = f"🌟 Премиум до {until}\n♾️ Безлимит"
                    else:
                        remaining = FREE_ATTEMPTS - user.get("attempts", 0) + user.get("extra", 0)
                        text_status = f"🆓 Бесплатных: {FREE_ATTEMPTS - user.get('attempts', 0)} из {FREE_ATTEMPTS}\n📦 Куплено: {user.get('extra', 0)}\n📊 Доступно: {remaining}"
                    send_message(chat_id, f"📊 **Статус**\n\n{text_status}")
                
                elif text == "/stats":
                    send_message(chat_id, f"📈 **Ваша статистика**\n\nВсего раскладов сделано: {user.get('total_readings', 0)}\nПопыток осталось: {FREE_ATTEMPTS - user.get('attempts', 0) + user.get('extra', 0)}")
                
                else:
                    send_message(chat_id, "❌ Неизвестная команда. Используй /start")
            
            elif "callback_query" in update:
                query = update["callback_query"]
                chat_id = query["message"]["chat"]["id"]
                message_id = query["message"]["message_id"]
                data_cb = query["data"]
                user_id = str(query["from"]["id"])
                
                if is_admin(user_id):
                    if data_cb in ["life", "love", "work"]:
                        card = get_card()
                        title = "Расклад на жизнь" if data_cb == "life" else "Расклад на отношения" if data_cb == "love" else "Расклад на работу"
                        send_photo(chat_id, card["img"], title, card["description"])
                    elif data_cb == "status":
                        edit_message(chat_id, message_id, "📊 **Статус админа**\n\n🌟 Безлимитные расклады", [[{"text": "🔙 Назад", "callback_data": "back"}]])
                    elif data_cb == "shop":
                        edit_message(chat_id, message_id, "🛒 **Магазин**\n\nДля админа попытки не нужны", [[{"text": "🔙 Назад", "callback_data": "back"}]])
                    elif data_cb == "back":
                        keyboard = [
                            [{"text": "🔮 Расклад на жизнь", "callback_data": "life"}],
                            [{"text": "❤️ Расклад на отношения", "callback_data": "love"}],
                            [{"text": "💼 Расклад на работу", "callback_data": "work"}],
                            [{"text": "🛒 Магазин", "callback_data": "shop"}],
                            [{"text": "📊 Статус", "callback_data": "status"}]
                        ]
                        edit_message(chat_id, message_id, "✨ Выбери тему расклада:", keyboard)
                    answer_url = f"https://api.telegram.org/bot{BOT_TOKEN}/answerCallbackQuery"
                    requests.post(answer_url, json={"callback_query_id": query["id"]}, timeout=5)
                    return
                
                user = get_user(user_id)
                if not user:
                    user = create_user(user_id)
                
                if not user:
                    edit_message(chat_id, message_id, "❌ Ошибка базы данных. Попробуй позже.")
                    return
                
                now = datetime.now()
                current_month = now.strftime("%Y-%m")
                
                if user.get("premium") and user.get("premium_until"):
                    if now > datetime.fromisoformat(user["premium_until"]):
                        update_user(user_id, {"premium": False, "premium_until": None})
                        user["premium"] = False
                        user["premium_until"] = None
                
                if user.get("month") != current_month and not user.get("premium"):
                    update_user(user_id, {"attempts": 0, "month": current_month})
                    user["attempts"] = 0
                    user["month"] = current_month
                
                def can_use():
                    if user.get("premium"):
                        return True
                    return user.get("attempts", 0) < FREE_ATTEMPTS or user.get("extra", 0) > 0
                
                def use_attempt():
                    if user.get("premium"):
                        return
                    if user.get("attempts", 0) < FREE_ATTEMPTS:
                        update_user(user_id, {"attempts": user.get("attempts", 0) + 1})
                        user["attempts"] = user.get("attempts", 0) + 1
                    elif user.get("extra", 0) > 0:
                        update_user(user_id, {"extra": user.get("extra", 0) - 1})
                        user["extra"] = user.get("extra", 0) - 1
                
                if data_cb == "status":
                    if user.get("premium"):
                        until = user["premium_until"].split("T")[0] if user.get("premium_until") else "неизвестно"
                        text = f"🌟 Премиум до {until}\n♾️ Безлимит"
                    else:
                        remaining = FREE_ATTEMPTS - user.get("attempts", 0) + user.get("extra", 0)
                        text = f"🆓 Бесплатных: {FREE_ATTEMPTS - user.get('attempts', 0)} из {FREE_ATTEMPTS}\n📦 Куплено: {user.get('extra', 0)}\n📊 Доступно: {remaining}"
                    edit_message(chat_id, message_id, f"📊 **Статус**\n\n{text}", [[{"text": "🔙 Назад", "callback_data": "back"}]])
                
                elif data_cb == "shop":
                    keyboard = [
                        [{"text": "📦 5 попыток — 20 ⭐️", "callback_data": "buy_5"}],
                        [{"text": "📦 10 попыток — 45 ⭐️", "callback_data": "buy_10"}],
                        [{"text": "🌟 Премиум на месяц — 75 ⭐️", "callback_data": "buy_premium"}],
                        [{"text": "🔙 Назад", "callback_data": "back"}]
                    ]
                    edit_message(chat_id, message_id, "🛒 **Магазин**\n\nВыбери вариант:", keyboard)
                
                elif data_cb == "buy_5":
                    send_message(chat_id, "🔄 Оформление заказа на 5 попыток...")
                    invoice_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendInvoice"
                    invoice_data = {
                        "chat_id": chat_id,
                        "title": "5 дополнительных попыток",
                        "description": "Попытки не сгорают в конце месяца",
                        "payload": "extra_5",
                        "provider_token": "",
                        "currency": "XTR",
                        "prices": [{"label": "5 попыток", "amount": 20}],
                        "start_parameter": "buy_5"
                    }
                    requests.post(invoice_url, json=invoice_data, timeout=10)
                
                elif data_cb == "buy_10":
                    send_message(chat_id, "🔄 Оформление заказа на 10 попыток...")
                    invoice_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendInvoice"
                    invoice_data = {
                        "chat_id": chat_id,
                        "title": "10 дополнительных попыток",
                        "description": "Попытки не сгорают в конце месяца",
                        "payload": "extra_10",
                        "provider_token": "",
                        "currency": "XTR",
                        "prices": [{"label": "10 попыток", "amount": 45}],
                        "start_parameter": "buy_10"
                    }
                    requests.post(invoice_url, json=invoice_data, timeout=10)
                
                elif data_cb == "buy_premium":
                    send_message(chat_id, "🔄 Оформление премиум-подписки...")
                    invoice_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendInvoice"
                    invoice_data = {
                        "chat_id": chat_id,
                        "title": "Премиум-подписка",
                        "description": "Безлимитные расклады на 30 дней",
                        "payload": "premium_month",
                        "provider_token": "",
                        "currency": "XTR",
                        "prices": [{"label": "Премиум на месяц", "amount": 75}],
                        "start_parameter": "premium"
                    }
                    requests.post(invoice_url, json=invoice_data, timeout=10)
                
                elif data_cb == "back":
                    keyboard = [
                        [{"text": "🔮 Расклад на жизнь", "callback_data": "life"}],
                        [{"text": "❤️ Расклад на отношения", "callback_data": "love"}],
                        [{"text": "💼 Расклад на работу", "callback_data": "work"}],
                        [{"text": "🛒 Магазин", "callback_data": "shop"}],
                        [{"text": "📊 Статус", "callback_data": "status"}]
                    ]
                    edit_message(chat_id, message_id, "✨ Выбери тему расклада:", keyboard)
                
                elif data_cb in ["life", "love", "work"]:
                    if not can_use():
                        edit_message(chat_id, message_id, f"❌ Лимит исчерпан. Зайди в магазин", [[{"text": "🛒 Магазин", "callback_data": "shop"}]])
                        return
                    
                    card = get_card()
                    if data_cb == "life":
                        title = "Расклад на жизнь"
                    elif data_cb == "love":
                        title = "Расклад на отношения"
                    else:
                        title = "Расклад на работу"
                    
                    send_photo(chat_id, card["img"], title, card["description"])
                    use_attempt()
                    update_user(user_id, {"total_readings": user.get("total_readings", 0) + 1})
                    
                    if not user.get("premium"):
                        remaining = FREE_ATTEMPTS - user.get("attempts", 0) + user.get("extra", 0)
                        send_message(chat_id, f"Осталось раскладов: {remaining}")
                
                answer_url = f"https://api.telegram.org/bot{BOT_TOKEN}/answerCallbackQuery"
                requests.post(answer_url, json={"callback_query_id": query["id"]}, timeout=5)
            
            elif "pre_checkout_query" in update:
                query = update["pre_checkout_query"]
                answer_url = f"https://api.telegram.org/bot{BOT_TOKEN}/answerPreCheckoutQuery"
                requests.post(answer_url, json={"pre_checkout_query_id": query["id"], "ok": True}, timeout=5)
            
            elif "message" in update and "successful_payment" in update["message"]:
                user_id = str(update["message"]["from"]["id"])
                payload = update["message"]["successful_payment"]["payload"]
                
                user = get_user(user_id)
                if not user:
                    user = create_user(user_id)
                
                if user:
                    if payload == "extra_5":
                        update_user(user_id, {"extra": user.get("extra", 0) + 5})
                        send_message(update["message"]["chat"]["id"], "✅ +5 дополнительных попыток!")
                    elif payload == "extra_10":
                        update_user(user_id, {"extra": user.get("extra", 0) + 10})
                        send_message(update["message"]["chat"]["id"], "✅ +10 дополнительных попыток!")
                    elif payload == "premium_month":
                        update_user(user_id, {"premium": True, "premium_until": (datetime.now() + timedelta(days=30)).isoformat()})
                        send_message(update["message"]["chat"]["id"], "✅ Премиум-подписка активирована на 30 дней!")
                    
                    send_message(update["message"]["chat"]["id"], "🛍️ Спасибо за покупку! Используй /status для проверки.")
        
        except Exception as e:
            print(f"Error: {e}")
        
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"ok")
