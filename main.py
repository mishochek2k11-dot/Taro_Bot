from http.server import BaseHTTPRequestHandler
import json
import requests
import random
from datetime import datetime, timedelta
from vercel_kv import KV

# ===== НАСТРОЙКИ =====
BOT_TOKEN = "8279893361:AAF5MW-v6m-JIMI0-pWSXf1yZlY963j5Oyw"  # ВСТАВЬ СВОЙ ТОКЕН
ADMIN_ID = "6180185234"
FREE_ATTEMPTS = 3

# Подключаем KV базу данных
kv = KV()
# =====================

# --- ФУНКЦИИ ДЛЯ РАБОТЫ С KV ---
def is_admin(user_id):
    return str(user_id) == ADMIN_ID

def get_user(user_id):
    try:
        data = kv.get(f"user:{user_id}")
        if data:
            return json.loads(data)
        return None
    except:
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
    kv.set(f"user:{user_id}", json.dumps(user_data))
    return user_data

def update_user(user_id, data):
    user = get_user(user_id)
    if user:
        user.update(data)
        kv.set(f"user:{user_id}", json.dumps(user))

# --- ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ БОТА ---
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
    # --- ВСЕ 78 КАРТ ТАРО (полный список) ---
CARDS = [
    {"name": "Шут", "img": "00-TheFool.png", "description": "Новое начало, спонтанность, вера в лучшее."},
    {"name": "Маг", "img": "01-TheMagician.png", "description": "Сила воли, мастерство, концентрация."},
    {"name": "Верховная Жрица", "img": "02-TheHighPriestess.png", "description": "Интуиция, тайные знания."},
    {"name": "Императрица", "img": "03-TheEmpress.png", "description": "Изобилие, плодородие, материнство."},
    {"name": "Император", "img": "04-TheEmperor.png", "description": "Власть, структура, авторитет."},
    {"name": "Иерофант", "img": "05-TheHierophant.png", "description": "Традиции, духовность, наставничество."},
    {"name": "Влюблённые", "img": "06-TheLovers.png", "description": "Выбор, отношения, гармония."},
    {"name": "Колесница", "img": "07-TheChariot.png", "description": "Победа, воля, контроль."},
    {"name": "Сила", "img": "08-Strength.png", "description": "Внутренняя сила, терпение."},
    {"name": "Отшельник", "img": "09-TheHermit.png", "description": "Мудрость, уединение, поиск."},
    {"name": "Колесо Фортуны", "img": "10-WheelOfFortune.png", "description": "Перемены, судьба."},
    {"name": "Справедливость", "img": "11-Justice.png", "description": "Честность, закон, карма."},
    {"name": "Повешенный", "img": "12-TheHangedMan.png", "description": "Жертва, новый взгляд."},
    {"name": "Смерть", "img": "13-Death.png", "description": "Трансформация, завершение."},
    {"name": "Умеренность", "img": "14-Temperance.png", "description": "Баланс, терпение."},
    {"name": "Дьявол", "img": "15-TheDevil.png", "description": "Привязанность, искушение."},
    {"name": "Башня", "img": "16-TheTower.png", "description": "Крах, внезапные перемены."},
    {"name": "Звезда", "img": "17-TheStar.png", "description": "Надежда, вдохновение."},
    {"name": "Луна", "img": "18-TheMoon.png", "description": "Иллюзия, страх, интуиция."},
    {"name": "Солнце", "img": "19-TheSun.png", "description": "Радость, успех, энергия."},
    {"name": "Суд", "img": "20-Judgement.png", "description": "Возрождение, прощение."},
    {"name": "Мир", "img": "21-TheWorld.png", "description": "Завершение, достижение."},
    {"name": "Туз Жезлов", "img": "Wands01.png", "description": "Новая энергия, вдохновение, начало."},
    {"name": "Двойка Жезлов", "img": "Wands02.png", "description": "Планирование, выбор."},
    {"name": "Тройка Жезлов", "img": "Wands03.png", "description": "Прогресс, расширение."},
    {"name": "Четвёрка Жезлов", "img": "Wands04.png", "description": "Праздник, дом, стабильность."},
    {"name": "Пятёрка Жезлов", "img": "Wands05.png", "description": "Конфликт, конкуренция."},
    {"name": "Шестёрка Жезлов", "img": "Wands06.png", "description": "Победа, признание."},
    {"name": "Семёрка Жезлов", "img": "Wands07.png", "description": "Защита, стойкость."},
    {"name": "Восьмёрка Жезлов", "img": "Wands08.png", "description": "Скорость, движение, новости."},
    {"name": "Девятка Жезлов", "img": "Wands09.png", "description": "Стойкость, последний рубеж."},
    {"name": "Десятка Жезлов", "img": "Wands10.png", "description": "Бремя, ответственность."},
    {"name": "Паж Жезлов", "img": "Wands11.png", "description": "Энтузиазм, новости."},
    {"name": "Рыцарь Жезлов", "img": "Wands12.png", "description": "Страсть, путешествие."},
    {"name": "Королева Жезлов", "img": "Wands13.png", "description": "Уверенность, независимость."},
    {"name": "Король Жезлов", "img": "Wands14.png", "description": "Лидерство, видение."},
    {"name": "Туз Кубков", "img": "Cups01.png", "description": "Любовь, новое чувство."},
    {"name": "Двойка Кубков", "img": "Cups02.png", "description": "Союз, партнёрство."},
    {"name": "Тройка Кубков", "img": "Cups03.png", "description": "Дружба, радость, праздник."},
    {"name": "Четвёрка Кубков", "img": "Cups04.png", "description": "Апатия, размышление."},
    {"name": "Пятёрка Кубков", "img": "Cups05.png", "description": "Потеря, печаль, принятие."},
    {"name": "Шестёрка Кубков", "img": "Cups06.png", "description": "Ностальгия, прошлое, доброта."},
    {"name": "Семёрка Кубков", "img": "Cups07.png", "description": "Иллюзии, мечты, выбор."},
    {"name": "Восьмёрка Кубков", "img": "Cups08.png", "description": "Уход, оставление, поиск смысла."},
    {"name": "Девятка Кубков", "img": "Cups09.png", "description": "Исполнение желаний, удовлетворение."},
    {"name": "Десятка Кубков", "img": "Cups10.png", "description": "Счастье, гармония, семья."},
    {"name": "Паж Кубков", "img": "Cups11.png", "description": "Предложение, интуиция, вдохновение."},
    {"name": "Рыцарь Кубков", "img": "Cups12.png", "description": "Романтика, приглашение."},
    {"name": "Королева Кубков", "img": "Cups13.png", "description": "Сострадание, эмоциональная мудрость."},
    {"name": "Король Кубков", "img": "Cups14.png", "description": "Эмоциональный контроль, дипломатия."},
    {"name": "Туз Мечей", "img": "Swords01.png", "description": "Ясность, прорыв, новая идея."},
    {"name": "Двойка Мечей", "img": "Swords02.png", "description": "Тупик, выбор, отказ видеть правду."},
    {"name": "Тройка Мечей", "img": "Swords03.png", "description": "Боль, разбитое сердце, разочарование."},
    {"name": "Четвёрка Мечей", "img": "Swords04.png", "description": "Отдых, восстановление, медитация."},
    {"name": "Пятёрка Мечей", "img": "Swords05.png", "description": "Конфликт, поражение, пустая победа."},
    {"name": "Шестёрка Мечей", "img": "Swords06.png", "description": "Переход, исцеление, путешествие."},
    {"name": "Семёрка Мечей", "img": "Swords07.png", "description": "Обман, хитрость, стратегия."},
    {"name": "Восьмёрка Мечей", "img": "Swords08.png", "description": "Ограничения, страх, самоблокировка."},
    {"name": "Девятка Мечей", "img": "Swords09.png", "description": "Тревога, кошмары, беспокойство."},
    {"name": "Десятка Мечей", "img": "Swords10.png", "description": "Крах, завершение, дно."},
    {"name": "Паж Мечей", "img": "Swords11.png", "description": "Любопытство, бдительность, новый взгляд."},
    {"name": "Рыцарь Мечей", "img": "Swords12.png", "description": "Скорость, агрессия, решительность."},
    {"name": "Королева Мечей", "img": "Swords13.png", "description": "Честность, независимость, прямота."},
    {"name": "Король Мечей", "img": "Swords14.png", "description": "Интеллект, авторитет, истина."},
    {"name": "Туз Пентаклей", "img": "Pentacles01.png", "description": "Новая возможность, ресурс, начало."},
    {"name": "Двойка Пентаклей", "img": "Pentacles02.png", "description": "Баланс, многозадачность, приоритеты."},
    {"name": "Тройка Пентаклей", "img": "Pentacles03.png", "description": "Команда, мастерство, сотрудничество."},
    {"name": "Четвёрка Пентаклей", "img": "Pentacles04.png", "description": "Контроль, стабильность, жадность."},
    {"name": "Пятёрка Пентаклей", "img": "Pentacles05.png", "description": "Нехватка, трудности, потеря."},
    {"name": "Шестёрка Пентаклей", "img": "Pentacles06.png", "description": "Щедрость, помощь, баланс даяния."},
    {"name": "Семёрка Пентаклей", "img": "Pentacles07.png", "description": "Терпение, ожидание, оценка."},
    {"name": "Восьмёрка Пентаклей", "img": "Pentacles08.png", "description": "Усердие, мастерство, детали."},
    {"name": "Девятка Пентаклей", "img": "Pentacles09.png", "description": "Уют, самодостаточность, роскошь."},
    {"name": "Десятка Пентаклей", "img": "Pentacles10.png", "description": "Наследие, богатство, семья."},
    {"name": "Паж Пентаклей", "img": "Pentacles11.png", "description": "Обучение, новая работа, энтузиазм."},
    {"name": "Рыцарь Пентаклей", "img": "Pentacles12.png", "description": "Надёжность, упорство, рутина."},
    {"name": "Королева Пентаклей", "img": "Pentacles13.png", "description": "Забота, изобилие, природа."},
    {"name": "Король Пентаклей", "img": "Pentacles14.png", "description": "Успех, процветание, бизнес."}
]

def get_card():
    return random.choice(CARDS)

# --- ОСНОВНОЙ ОБРАБОТЧИК С КОМАНДАМИ И КНОПКАМИ ---
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

            # --- ОБРАБОТКА СООБЩЕНИЙ (КОМАНД) ---
            if "message" in update:
                chat_id = update["message"]["chat"]["id"]
                text = update["message"].get("text", "")
                user_id = str(update["message"]["from"]["id"])

                # АДМИН
                if is_admin(user_id):
                    if text == "/start":
                        keyboard = [
                            [{"text": "🔮 Расклад на жизнь", "callback_data": "life"}],
                            [{"text": "❤️ Расклад на отношения", "callback_data": "love"}],
                            [{"text": "💼 Расклад на работу", "callback_data": "work"}],
                            [{"text": "🛒 Магазин", "callback_data": "shop"}],
                            [{"text": "📊 Статус", "callback_data": "status"}]
                        ]
                        send_message(chat_id, "✨ Админ-режим. Безлимит.", keyboard)
                    elif text == "/buy":
                        keyboard = [
                            [{"text": "📦 5 попыток — 20 ⭐️", "callback_data": "buy_5"}],
                            [{"text": "📦 10 попыток — 45 ⭐️", "callback_data": "buy_10"}],
                            [{"text": "🌟 Премиум на месяц — 75 ⭐️", "callback_data": "buy_premium"}],
                            [{"text": "🔙 Назад", "callback_data": "back"}]
                        ]
                        send_message(chat_id, "🛒 **МАГАЗИН**\n\nВыбери вариант:", keyboard)
                    elif text == "/status":
                        send_message(chat_id, "📊 **СТАТУС АДМИНА**\n\n🌟 Безлимитные расклады")
                    elif text == "/stats":
                        send_message(chat_id, "📈 **СТАТИСТИКА АДМИНА**\n\nСоздатель бота, безлимит.")
                    else:
                        send_message(chat_id, "❌ Неизвестная команда. /start")
                    return

                # --- ОБЫЧНЫЙ ПОЛЬЗОВАТЕЛЬ ---
                user = get_user(user_id)
                if not user:
                    user = create_user(user_id)

                now = datetime.now()
                current_month = now.strftime("%Y-%m")
                if user.get("premium") and user.get("premium_until"):
                    if now > datetime.fromisoformat(user["premium_until"]):
                        update_user(user_id, {"premium": False, "premium_until": None})
                        user["premium"] = False

                if user.get("month") != current_month and not user.get("premium"):
                    update_user(user_id, {"attempts": 0, "month": current_month})
                    user["attempts"] = 0

                if text == "/start":
                    keyboard = [
                        [{"text": "🔮 Расклад на жизнь", "callback_data": "life"}],
                        [{"text": "❤️ Расклад на отношения", "callback_data": "love"}],
                        [{"text": "💼 Расклад на работу", "callback_data": "work"}],
                        [{"text": "🛒 Магазин", "callback_data": "shop"}],
                        [{"text": "📊 Статус", "callback_data": "status"}]
                    ]
                    welcome_text = (
                        "✨ **ДОБРО ПОЖАЛОВАТЬ В БОТА ТАРО!** ✨\n\n"
                        "📋 **Доступные команды:**\n"
                        "/start — показать это сообщение\n"
                        "/buy — открыть магазин попыток и премиум\n"
                        "/status — проверить статус подписки и остаток попыток\n"
                        "/stats — посмотреть статистику (сколько раскладов сделано)\n\n"
                        f"🔥 У тебя {FREE_ATTEMPTS} бесплатных расклада в МЕСЯЦ.\n"
                        "🌟 Премиум-подписка даёт безлимит.\n\n"
                        "👇 **ВЫБЕРИ ТЕМУ РАСКЛАДА:**"
                    )
                    send_message(chat_id, welcome_text, keyboard)
                elif text == "/buy":
                    keyboard = [
                        [{"text": "📦 5 попыток — 20 ⭐️", "callback_data": "buy_5"}],
                        [{"text": "📦 10 попыток — 45 ⭐️", "callback_data": "buy_10"}],
                        [{"text": "🌟 Премиум на месяц — 75 ⭐️", "callback_data": "buy_premium"}],
                        [{"text": "🔙 Назад", "callback_data": "back"}]
                    ]
                    send_message(chat_id, "🛒 **МАГАЗИН**\n\nВыбери вариант:", keyboard)
                elif text == "/status":
                    if user.get("premium"):
                        until = user["premium_until"].split("T")[0] if user.get("premium_until") else "неизвестно"
                        text_status = f"🌟 ПРЕМИУМ до {until}\n♾️ Безлимит"
                    else:
                        remaining = FREE_ATTEMPTS - user.get("attempts", 0) + user.get("extra", 0)
                        text_status = f"🆓 Бесплатных: {FREE_ATTEMPTS - user.get('attempts', 0)} из {FREE_ATTEMPTS}\n📦 Куплено: {user.get('extra', 0)}\n📊 Доступно: {remaining}"
                    send_message(chat_id, f"📊 **СТАТУС**\n\n{text_status}")
                elif text == "/stats":
                    send_message(chat_id, f"📈 **ВАША СТАТИСТИКА**\n\nВсего раскладов сделано: {user.get('total_readings', 0)}\nПопыток осталось: {FREE_ATTEMPTS - user.get('attempts', 0) + user.get('extra', 0)}")
                else:
                    send_message(chat_id, "❌ Неизвестная команда. /start")

            # --- ОБРАБОТКА НАЖАТИЙ НА КНОПКИ (CALLBACK) ---
            elif "callback_query" in update:
                query = update["callback_query"]
                chat_id = query["message"]["chat"]["id"]
                message_id = query["message"]["message_id"]
                data_cb = query["data"]
                user_id = str(query["from"]["id"])

                # АДМИН
                if is_admin(user_id):
                    if data_cb in ["life", "love", "work"]:
                        card = get_card()
                        title = "Расклад на жизнь" if data_cb == "life" else "Расклад на отношения" if data_cb == "love" else "Расклад на работу"
                        send_photo(chat_id, card["img"], title, card["description"])
                    elif data_cb == "status":
                        edit_message(chat_id, message_id, "📊 **Статус админа**\n\n🌟 Безлимит", [[{"text": "🔙 Назад", "callback_data": "back"}]])
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
                        edit_message(chat_id, message_id, "✨ ВЫБЕРИ ТЕМУ РАСКЛАДА:", keyboard)
                    requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/answerCallbackQuery", json={"callback_query_id": query["id"]})
                    return

                # --- ОБЫЧНЫЙ ПОЛЬЗОВАТЕЛЬ ---
                user = get_user(user_id)
                if not user:
                    user = create_user(user_id)

                now = datetime.now()
                current_month = now.strftime("%Y-%m")
                if user.get("premium") and user.get("premium_until"):
                    if now > datetime.fromisoformat(user["premium_until"]):
                        update_user(user_id, {"premium": False, "premium_until": None})
                        user["premium"] = False

                if user.get("month") != current_month and not user.get("premium"):
                    update_user(user_id, {"attempts": 0, "month": current_month})
                    user["attempts"] = 0

                def can_use():
                    if user.get("premium"):
                        return True
                    return user.get("attempts", 0) < FREE_ATTEMPTS or user.get("extra", 0) > 0

                def use_attempt():
                    if user.get("premium"):
                        return
                    if user.get("attempts", 0) < FREE_ATTEMPTS:
                        user["attempts"] = user.get("attempts", 0) + 1
                        update_user(user_id, {"attempts": user["attempts"]})
                    elif user.get("extra", 0) > 0:
                        user["extra"] = user.get("extra", 0) - 1
                        update_user(user_id, {"extra": user["extra"]})

                if data_cb == "status":
                    if user.get("premium"):
                        until = user["premium_until"].split("T")[0] if user.get("premium_until") else "неизвестно"
                        text = f"🌟 ПРЕМИУМ до {until}\n♾️ Безлимит"
                    else:
                        remaining = FREE_ATTEMPTS - user.get("attempts", 0) + user.get("extra", 0)
                        text = f"🆓 Бесплатных: {FREE_ATTEMPTS - user.get('attempts', 0)} из {FREE_ATTEMPTS}\n📦 Куплено: {user.get('extra', 0)}\n📊 Доступно: {remaining}"
                    edit_message(chat_id, message_id, f"📊 **СТАТУС**\n\n{text}", [[{"text": "🔙 Назад", "callback_data": "back"}]])

                elif data_cb == "shop":
                    keyboard = [
                        [{"text": "📦 5 попыток — 20 ⭐️", "callback_data": "buy_5"}],
                        [{"text": "📦 10 попыток — 45 ⭐️", "callback_data": "buy_10"}],
                        [{"text": "🌟 Премиум на месяц — 75 ⭐️", "callback_data": "buy_premium"}],
                        [{"text": "🔙 Назад", "callback_data": "back"}]
                    ]
                    edit_message(chat_id, message_id, "🛒 **МАГАЗИН**\n\nВыбери вариант:", keyboard)

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
                    edit_message(chat_id, message_id, "✨ ВЫБЕРИ ТЕМУ РАСКЛАДА:", keyboard)

                elif data_cb in ["life", "love", "work"]:
                    if not can_use():
                        edit_message(chat_id, message_id, f"❌ ЛИМИТ ИСЧЕРПАН.\nБесплатных попыток: {FREE_ATTEMPTS}\nКупленных: {user.get('extra', 0)}", [[{"text": "🛒 МАГАЗИН", "callback_data": "shop"}]])
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
                    remaining = FREE_ATTEMPTS - user.get("attempts", 0)
                    send_message(chat_id, f"📊 Осталось бесплатных раскладов: {remaining}")

                requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/answerCallbackQuery", json={"callback_query_id": query["id"]})

            # --- ОБРАБОТКА ПЛАТЕЖЕЙ ---
            elif "pre_checkout_query" in update:
                query = update["pre_checkout_query"]
                requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/answerPreCheckoutQuery", json={"pre_checkout_query_id": query["id"], "ok": True})

            elif "message" in update and "successful_payment" in update["message"]:
                user_id = str(update["message"]["from"]["id"])
                payload = update["message"]["successful_payment"]["payload"]
                user = get_user(user_id) or create_user(user_id)
                if payload == "extra_5":
                    update_user(user_id, {"extra": user.get("extra", 0) + 5})
                    send_message(update["message"]["chat"]["id"], "✅ +5 ДОПОЛНИТЕЛЬНЫХ ПОПЫТОК!")
                elif payload == "extra_10":
                    update_user(user_id, {"extra": user.get("extra", 0) + 10})
                    send_message(update["message"]["chat"]["id"], "✅ +10 ДОПОЛНИТЕЛЬНЫХ ПОПЫТОК!")
                elif payload == "premium_month":
                    update_user(user_id, {"premium": True, "premium_until": (datetime.now() + timedelta(days=30)).isoformat()})
                    send_message(update["message"]["chat"]["id"], "✅ ПРЕМИУМ-ПОДПИСКА АКТИВИРОВАНА НА 30 ДНЕЙ!")
                send_message(update["message"]["chat"]["id"], "🛍️ СПАСИБО ЗА ПОКУПКУ! /status")

        except Exception as e:
            print(f"Error: {e}")

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"ok")
