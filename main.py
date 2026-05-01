from http.server import BaseHTTPRequestHandler
import json
import requests
import random
from datetime import datetime, timedelta

BOT_TOKEN = "8279893361:AAF5MW-v6m-JIMI0-pWSXf1yZlY963j5Oyw"
ADMIN_ID = "6180185234"
FREE_ATTEMPTS = 3

users = {}

CARDS = [
    {"name": "Шут", "img": "00-TheFool.png", "description": "Новое начало, спонтанность, вера в лучшее."},
    # Добавь остальные 77 карт по образцу (или оставь одну для теста)
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
                
                if user_id not in users:
                    now = datetime.now()
                    users[user_id] = {
                        "attempts": 0,
                        "extra": 0,
                        "premium": False,
                        "premium_until": None,
                        "month": now.strftime("%Y-%m"),
                        "total_readings": 0
                    }
                
                u = users[user_id]
                now = datetime.now()
                current_month = now.strftime("%Y-%m")
                
                if u.get("premium") and u.get("premium_until"):
                    if now > datetime.fromisoformat(u["premium_until"]):
                        u["premium"] = False
                        u["premium_until"] = None
                
                if u.get("month") != current_month and not u.get("premium"):
                    u["attempts"] = 0
                    u["month"] = current_month
                
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
                    if u.get("premium"):
                        until = u["premium_until"].split("T")[0] if u.get("premium_until") else "неизвестно"
                        text_status = f"🌟 Премиум до {until}\n♾️ Безлимит"
                    else:
                        remaining = FREE_ATTEMPTS - u.get("attempts", 0) + u.get("extra", 0)
                        text_status = f"🆓 Бесплатных: {FREE_ATTEMPTS - u.get('attempts', 0)} из {FREE_ATTEMPTS}\n📦 Куплено: {u.get('extra', 0)}\n📊 Доступно: {remaining}"
                    send_message(chat_id, f"📊 **Статус**\n\n{text_status}")
                
                elif text == "/stats":
                    send_message(chat_id, f"📈 **Ваша статистика**\n\nВсего раскладов сделано: {u.get('total_readings', 0)}\nПопыток осталось: {FREE_ATTEMPTS - u.get('attempts', 0) + u.get('extra', 0)}")
                
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
                
                if user_id not in users:
                    now = datetime.now()
                    users[user_id] = {
                        "attempts": 0,
                        "extra": 0,
                        "premium": False,
                        "premium_until": None,
                        "month": now.strftime("%Y-%m"),
                        "total_readings": 0
                    }
                
                u = users[user_id]
                now = datetime.now()
                current_month = now.strftime("%Y-%m")
                
                if u.get("premium") and u.get("premium_until"):
                    if now > datetime.fromisoformat(u["premium_until"]):
                        u["premium"] = False
                        u["premium_until"] = None
                
                if u.get("month") != current_month and not u.get("premium"):
                    u["attempts"] = 0
                    u["month"] = current_month
                
                def can_use():
                    if u.get("premium"):
                        return True
                    return u.get("attempts", 0) < FREE_ATTEMPTS or u.get("extra", 0) > 0
                
                def use_attempt():
                    if u.get("premium"):
                        return
                    if u.get("attempts", 0) < FREE_ATTEMPTS:
                        u["attempts"] = u.get("attempts", 0) + 1
                    elif u.get("extra", 0) > 0:
                        u["extra"] = u.get("extra", 0) - 1
                
                if data_cb == "status":
                    if u.get("premium"):
                        until = u["premium_until"].split("T")[0] if u.get("premium_until") else "неизвестно"
                        text = f"🌟 Премиум до {until}\n♾️ Безлимит"
                    else:
                        remaining = FREE_ATTEMPTS - u.get("attempts", 0) + u.get("extra", 0)
                        text = f"🆓 Бесплатных: {FREE_ATTEMPTS - u.get('attempts', 0)} из {FREE_ATTEMPTS}\n📦 Куплено: {u.get('extra', 0)}\n📊 Доступно: {remaining}"
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
                    u["total_readings"] = u.get("total_readings", 0) + 1
                    
                    if not u.get("premium"):
                        remaining = FREE_ATTEMPTS - u.get("attempts", 0) + u.get("extra", 0)
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
                
                if user_id not in users:
                    now = datetime.now()
                    users[user_id] = {
                        "attempts": 0,
                        "extra": 0,
                        "premium": False,
                        "premium_until": None,
                        "month": now.strftime("%Y-%m"),
                        "total_readings": 0
                    }
                u = users[user_id]
                
                if payload == "extra_5":
                    u["extra"] = u.get("extra", 0) + 5
                    send_message(update["message"]["chat"]["id"], "✅ +5 дополнительных попыток!")
                elif payload == "extra_10":
                    u["extra"] = u.get("extra", 0) + 10
                    send_message(update["message"]["chat"]["id"], "✅ +10 дополнительных попыток!")
                elif payload == "premium_month":
                    u["premium"] = True
                    u["premium_until"] = (datetime.now() + timedelta(days=30)).isoformat()
                    send_message(update["message"]["chat"]["id"], "✅ Премиум-подписка активирована на 30 дней!")
                
                send_message(update["message"]["chat"]["id"], "🛍️ Спасибо за покупку! Используй /status для проверки.")
        
        except Exception as e:
            print(f"Error: {e}")
        
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"ok")
