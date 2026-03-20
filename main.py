from http.server import BaseHTTPRequestHandler
import json
import requests
import random
from datetime import datetime, timedelta

BOT_TOKEN = "8279893361:AAF5MW-v6m-JIMI0-pWSXf1yZlY963j5Oyw"  
FREE_ATTEMPTS = 3

users = {}

# === ВСЕ 78 КАРТ ТАРО ===
CARDS = [
    # 0-21 Старшие Арканы
    {"name": "Шут", "img": "fool.jpg", "meaning": "Новые начинания, спонтанность, вера в лучшее"},
    {"name": "Маг", "img": "magician.jpg", "meaning": "Сила воли, мастерство, концентрация"},
    {"name": "Верховная Жрица", "img": "high_priestess.jpg", "meaning": "Интуиция, тайные знания"},
    {"name": "Императрица", "img": "empress.jpg", "meaning": "Изобилие, плодородие, материнство"},
    {"name": "Император", "img": "emperor.jpg", "meaning": "Власть, структура, авторитет"},
    {"name": "Иерофант", "img": "hierophant.jpg", "meaning": "Традиции, духовность, наставничество"},
    {"name": "Влюблённые", "img": "lovers.jpg", "meaning": "Выбор, отношения, гармония"},
    {"name": "Колесница", "img": "chariot.jpg", "meaning": "Победа, воля, контроль"},
    {"name": "Сила", "img": "strength.jpg", "meaning": "Внутренняя сила, терпение"},
    {"name": "Отшельник", "img": "hermit.jpg", "meaning": "Мудрость, уединение, поиск"},
    {"name": "Колесо Фортуны", "img": "wheel_of_fortune.jpg", "meaning": "Перемены, судьба"},
    {"name": "Справедливость", "img": "justice.jpg", "meaning": "Честность, закон, карма"},
    {"name": "Повешенный", "img": "hanged_man.jpg", "meaning": "Жертва, новый взгляд"},
    {"name": "Смерть", "img": "death.jpg", "meaning": "Трансформация, завершение"},
    {"name": "Умеренность", "img": "temperance.jpg", "meaning": "Баланс, терпение"},
    {"name": "Дьявол", "img": "devil.jpg", "meaning": "Привязанность, искушение"},
    {"name": "Башня", "img": "tower.jpg", "meaning": "Крах, внезапные перемены"},
    {"name": "Звезда", "img": "star.jpg", "meaning": "Надежда, вдохновение"},
    {"name": "Луна", "img": "moon.jpg", "meaning": "Иллюзия, страх, интуиция"},
    {"name": "Солнце", "img": "sun.jpg", "meaning": "Радость, успех, энергия"},
    {"name": "Суд", "img": "judgement.jpg", "meaning": "Возрождение, прощение"},
    {"name": "Мир", "img": "world.jpg", "meaning": "Завершение, достижение"},
    # Жезлы (14)
    {"name": "Туз Жезлов", "img": "ace_of_wands.jpg", "meaning": "Новая энергия, вдохновение"},
    {"name": "Двойка Жезлов", "img": "two_of_wands.jpg", "meaning": "Планирование, выбор"},
    {"name": "Тройка Жезлов", "img": "three_of_wands.jpg", "meaning": "Прогресс, расширение"},
    {"name": "Четвёрка Жезлов", "img": "four_of_wands.jpg", "meaning": "Праздник, дом, стабильность"},
    {"name": "Пятёрка Жезлов", "img": "five_of_wands.jpg", "meaning": "Конфликт, конкуренция"},
    {"name": "Шестёрка Жезлов", "img": "six_of_wands.jpg", "meaning": "Победа, признание"},
    {"name": "Семёрка Жезлов", "img": "seven_of_wands.jpg", "meaning": "Защита, стойкость"},
    {"name": "Восьмёрка Жезлов", "img": "eight_of_wands.jpg", "meaning": "Скорость, движение"},
    {"name": "Девятка Жезлов", "img": "nine_of_wands.jpg", "meaning": "Стойкость, последний рубеж"},
    {"name": "Десятка Жезлов", "img": "ten_of_wands.jpg", "meaning": "Бремя, ответственность"},
    {"name": "Паж Жезлов", "img": "page_of_wands.jpg", "meaning": "Энтузиазм, новости"},
    {"name": "Рыцарь Жезлов", "img": "knight_of_wands.jpg", "meaning": "Страсть, путешествие"},
    {"name": "Королева Жезлов", "img": "queen_of_wands.jpg", "meaning": "Уверенность, независимость"},
    {"name": "Король Жезлов", "img": "king_of_wands.jpg", "meaning": "Лидерство, видение"},
    # Кубки (14)
    {"name": "Туз Кубков", "img": "ace_of_cups.jpg", "meaning": "Любовь, новое чувство"},
    {"name": "Двойка Кубков", "img": "two_of_cups.jpg", "meaning": "Союз, партнёрство"},
    {"name": "Тройка Кубков", "img": "three_of_cups.jpg", "meaning": "Дружба, радость"},
    {"name": "Четвёрка Кубков", "img": "four_of_cups.jpg", "meaning": "Апатия, размышление"},
    {"name": "Пятёрка Кубков", "img": "five_of_cups.jpg", "meaning": "Потеря, печаль"},
    {"name": "Шестёрка Кубков", "img": "six_of_cups.jpg", "meaning": "Ностальгия, прошлое"},
    {"name": "Семёрка Кубков", "img": "seven_of_cups.jpg", "meaning": "Иллюзии, мечты"},
    {"name": "Восьмёрка Кубков", "img": "eight_of_cups.jpg", "meaning": "Уход, поиск смысла"},
    {"name": "Девятка Кубков", "img": "nine_of_cups.jpg", "meaning": "Исполнение желаний"},
    {"name": "Десятка Кубков", "img": "ten_of_cups.jpg", "meaning": "Счастье, семья"},
    {"name": "Паж Кубков", "img": "page_of_cups.jpg", "meaning": "Предложение, интуиция"},
    {"name": "Рыцарь Кубков", "img": "knight_of_cups.jpg", "meaning": "Романтика, приглашение"},
    {"name": "Королева Кубков", "img": "queen_of_cups.jpg", "meaning": "Сострадание, мудрость"},
    {"name": "Король Кубков", "img": "king_of_cups.jpg", "meaning": "Эмоциональный контроль"},
    # Мечи (14)
    {"name": "Туз Мечей", "img": "ace_of_swords.jpg", "meaning": "Ясность, прорыв"},
    {"name": "Двойка Мечей", "img": "two_of_swords.jpg", "meaning": "Тупик, выбор"},
    {"name": "Тройка Мечей", "img": "three_of_swords.jpg", "meaning": "Боль, разбитое сердце"},
    {"name": "Четвёрка Мечей", "img": "four_of_swords.jpg", "meaning": "Отдых, восстановление"},
    {"name": "Пятёрка Мечей", "img": "five_of_swords.jpg", "meaning": "Конфликт, поражение"},
    {"name": "Шестёрка Мечей", "img": "six_of_swords.jpg", "meaning": "Переход, исцеление"},
    {"name": "Семёрка Мечей", "img": "seven_of_swords.jpg", "meaning": "Обман, хитрость"},
    {"name": "Восьмёрка Мечей", "img": "eight_of_swords.jpg", "meaning": "Ограничения, страх"},
    {"name": "Девятка Мечей", "img": "nine_of_swords.jpg", "meaning": "Тревога, кошмары"},
    {"name": "Десятка Мечей", "img": "ten_of_swords.jpg", "meaning": "Крах, завершение"},
    {"name": "Паж Мечей", "img": "page_of_swords.jpg", "meaning": "Любопытство, бдительность"},
    {"name": "Рыцарь Мечей", "img": "knight_of_swords.jpg", "meaning": "Скорость, агрессия"},
    {"name": "Королева Мечей", "img": "queen_of_swords.jpg", "meaning": "Честность, независимость"},
    {"name": "Король Мечей", "img": "king_of_swords.jpg", "meaning": "Интеллект, авторитет"},
    # Пентакли (14)
    {"name": "Туз Пентаклей", "img": "ace_of_pentacles.jpg", "meaning": "Новая возможность, ресурс"},
    {"name": "Двойка Пентаклей", "img": "two_of_pentacles.jpg", "meaning": "Баланс, многозадачность"},
    {"name": "Тройка Пентаклей", "img": "three_of_pentacles.jpg", "meaning": "Команда, мастерство"},
    {"name": "Четвёрка Пентаклей", "img": "four_of_pentacles.jpg", "meaning": "Контроль, стабильность"},
    {"name": "Пятёрка Пентаклей", "img": "five_of_pentacles.jpg", "meaning": "Нехватка, трудности"},
    {"name": "Шестёрка Пентаклей", "img": "six_of_pentacles.jpg", "meaning": "Щедрость, помощь"},
    {"name": "Семёрка Пентаклей", "img": "seven_of_pentacles.jpg", "meaning": "Терпение, ожидание"},
    {"name": "Восьмёрка Пентаклей", "img": "eight_of_pentacles.jpg", "meaning": "Усердие, мастерство"},
    {"name": "Девятка Пентаклей", "img": "nine_of_pentacles.jpg", "meaning": "Уют, самодостаточность"},
    {"name": "Десятка Пентаклей", "img": "ten_of_pentacles.jpg", "meaning": "Наследие, богатство"},
    {"name": "Паж Пентаклей", "img": "page_of_pentacles.jpg", "meaning": "Обучение, новая работа"},
    {"name": "Рыцарь Пентаклей", "img": "knight_of_pentacles.jpg", "meaning": "Надёжность, упорство"},
    {"name": "Королева Пентаклей", "img": "queen_of_pentacles.jpg", "meaning": "Забота, изобилие"},
    {"name": "Король Пентаклей", "img": "king_of_pentacles.jpg", "meaning": "Успех, процветание"},
]

def get_card():
    return random.choice(CARDS)

def send_photo(chat_id, image_name, caption):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    image_url = f"https://taro-bot-rho.vercel.app/images/{image_name}"
    requests.post(url, json={"chat_id": chat_id, "photo": image_url, "caption": caption, "parse_mode": "Markdown"})

def send_message(chat_id, text, keyboard=None):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    if keyboard:
        data["reply_markup"] = json.dumps({"inline_keyboard": keyboard})
    requests.post(url, json=data)

def edit_message(chat_id, message_id, text, keyboard=None):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/editMessageText"
    data = {"chat_id": chat_id, "message_id": message_id, "text": text, "parse_mode": "Markdown"}
    if keyboard:
        data["reply_markup"] = json.dumps({"inline_keyboard": keyboard})
    requests.post(url, json=data)

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
                user_id = update["message"]["from"]["id"]
                
                now = datetime.now().strftime("%Y-%m")
                if user_id not in users:
                    users[user_id] = {"attempts": 0, "premium": False, "premium_until": None, "extra_attempts": 0, "month": now}
                
                u = users[user_id]
                
                if u["premium"] and u["premium_until"]:
                    if datetime.now() > datetime.fromisoformat(u["premium_until"]):
                        u["premium"] = False
                        u["premium_until"] = None
                
                if u["month"] != now and not u["premium"]:
                    u["attempts"] = 0
                    u["month"] = now
                
                if text == "/start":
                    keyboard = [
                        [{"text": "🔮 Расклад на жизнь", "callback_data": "life"}],
                        [{"text": "❤️ Расклад на отношения", "callback_data": "love"}],
                        [{"text": "💼 Расклад на работу", "callback_data": "work"}],
                        [{"text": "🛒 Магазин попыток", "callback_data": "shop"}],
                        [{"text": "📊 Статус", "callback_data": "status"}]
                    ]
                    send_message(chat_id, "✨ Привет! Выбери тему расклада:", keyboard)
                else:
                    send_message(chat_id, "❌ Неизвестная команда. Используй /start")
            
            elif "callback_query" in update:
                query = update["callback_query"]
                chat_id = query["message"]["chat"]["id"]
                message_id = query["message"]["message_id"]
                data_cb = query["data"]
                user_id = query["from"]["id"]
                
                now = datetime.now().strftime("%Y-%m")
                if user_id not in users:
                    users[user_id] = {"attempts": 0, "premium": False, "premium_until": None, "extra_attempts": 0, "month": now}
                u = users[user_id]
                
                if u["premium"] and u["premium_until"]:
                    if datetime.now() > datetime.fromisoformat(u["premium_until"]):
                        u["premium"] = False
                        u["premium_until"] = None
                
                if u["month"] != now and not u["premium"]:
                    u["attempts"] = 0
                    u["month"] = now
                
                def can_use():
                    if u["premium"]:
                        return True
                    return u["attempts"] < FREE_ATTEMPTS or u["extra_attempts"] > 0
                
                def use_attempt():
                    if u["premium"]:
                        return
                    if u["attempts"] < FREE_ATTEMPTS:
                        u["attempts"] += 1
                    elif u["extra_attempts"] > 0:
                        u["extra_attempts"] -= 1
                
                if data_cb == "status":
                    if u["premium"]:
                        until = u["premium_until"].split("T")[0] if u["premium_until"] else "неизвестно"
                        text = f"🌟 Премиум активна до {until}\n♾️ Безлимитные расклады"
                    else:
                        remaining = FREE_ATTEMPTS - u["attempts"] + u["extra_attempts"]
                        text = f"🆓 Бесплатных: {FREE_ATTEMPTS - u['attempts']} из {FREE_ATTEMPTS}\n📦 Куплено попыток: {u['extra_attempts']}\n📊 Доступно всего: {remaining}"
                    edit_message(chat_id, message_id, f"📊 **Ваш статус**\n\n{text}", [[{"text": "🔙 Назад", "callback_data": "back"}]])
                
                elif data_cb == "shop":
                    keyboard = [
                        [{"text": "📦 5 попыток — 20 ⭐️", "callback_data": "buy_5"}],
                        [{"text": "📦 10 попыток — 45 ⭐️", "callback_data": "buy_10"}],
                        [{"text": "🌟 Премиум на месяц — 75 ⭐️", "callback_data": "buy_premium"}],
                        [{"text": "🔙 Назад", "callback_data": "back"}]
                    ]
                    edit_message(chat_id, message_id, "🛒 **Магазин попыток**\n\nВыбери вариант:", keyboard)
                
                elif data_cb == "buy_5":
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
                    requests.post(invoice_url, json=invoice_data)
                
                elif data_cb == "buy_10":
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
                    requests.post(invoice_url, json=invoice_data)
                
                elif data_cb == "buy_premium":
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
                    requests.post(invoice_url, json=invoice_data)
                
                elif data_cb == "back":
                    keyboard = [
                        [{"text": "🔮 Расклад на жизнь", "callback_data": "life"}],
                        [{"text": "❤️ Расклад на отношения", "callback_data": "love"}],
                        [{"text": "💼 Расклад на работу", "callback_data": "work"}],
                        [{"text": "🛒 Магазин попыток", "callback_data": "shop"}],
                        [{"text": "📊 Статус", "callback_data": "status"}]
                    ]
                    edit_message(chat_id, message_id, "✨ Выбери тему расклада:", keyboard)
                
                elif data_cb in ["life", "love", "work"]:
                    if not can_use():
                        shop_keyboard = [[{"text": "🛒 Магазин попыток", "callback_data": "shop"}]]
                        edit_message(chat_id, message_id, f"❌ Лимит исчерпан. Купи дополнительные попытки или премиум:", shop_keyboard)
                        return
                    
                    card = get_card()
                    emoji = {"life": "🔮", "love": "❤️", "work": "💼"}
                    title = {"life": "Расклад на жизнь", "love": "Расклад на отношения", "work": "Расклад на работу"}
                    caption = f"{emoji[data_cb]} **{title[data_cb]}**\n\n**{card['name']}**\n\n{card['meaning']}"
                    send_photo(chat_id, card["img"], caption)
                    use_attempt()
                    
                    if not u["premium"]:
                        remaining = FREE_ATTEMPTS - u["attempts"] + u["extra_attempts"]
                        send_message(chat_id, f"Осталось доступных раскладов: {remaining}")
                
                answer_url = f"https://api.telegram.org/bot{BOT_TOKEN}/answerCallbackQuery"
                requests.post(answer_url, json={"callback_query_id": query["id"]})
            
            elif "pre_checkout_query" in update:
                query = update["pre_checkout_query"]
                answer_url = f"https://api.telegram.org/bot{BOT_TOKEN}/answerPreCheckoutQuery"
                requests.post(answer_url, json={"pre_checkout_query_id": query["id"], "ok": True})
            
            elif "message" in update and "successful_payment" in update["message"]:
                user_id = update["message"]["from"]["id"]
                payload = update["message"]["successful_payment"]["payload"]
                
                if user_id not in users:
                    users[user_id] = {"attempts": 0, "premium": False, "premium_until": None, "extra_attempts": 0, "month": datetime.now().strftime("%Y-%m")}
                u = users[user_id]
                
                if payload == "extra_5":
                    u["extra_attempts"] += 5
                    send_message(update["message"]["chat"]["id"], "✅ Куплено 5 дополнительных попыток!")
                elif payload == "extra_10":
                    u["extra_attempts"] += 10
                    send_message(update["message"]["chat"]["id"], "✅ Куплено 10 дополнительных попыток!")
                elif payload == "premium_month":
                    u["premium"] = True
                    u["premium_until"] = (datetime.now() + timedelta(days=30)).isoformat()
                    send_message(update["message"]["chat"]["id"], "✅ Премиум-подписка активирована на 30 дней!")
        
        except Exception as e:
            print(f"Error: {e}")
        
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"ok")
