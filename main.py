from http.server import BaseHTTPRequestHandler
import json
import requests
import random
from datetime import datetime, timedelta
import os

BOT_TOKEN = "8279893361:AAF5MW-v6m-JIMI0-pWSXf1yZlY963j5Oyw"  
FREE_ATTEMPTS = 3
ADMIN_ID = "6180185234"  

# Хранилище в памяти (временное, пока не настроишь базу)
users = {}

# === ВСЕ 78 КАРТ ===
CARDS = [
    {"name": "Шут", "img": "00-TheFool.png", "description": "Тебя ждёт новое начало. Не бойся рискнуть — удача на твоей стороне."},
    {"name": "Маг", "img": "01-TheMagician.png", "description": "У тебя есть все ресурсы для достижения цели. Действуй!"},
    {"name": "Верховная Жрица", "img": "02-TheHighPriestess.png", "description": "Прислушайся к интуиции. Ответы уже внутри тебя."},
    {"name": "Императрица", "img": "03-TheEmpress.png", "description": "Время созидания и заботы. Отношения и дела будут процветать."},
    {"name": "Император", "img": "04-TheEmperor.png", "description": "Нужна структура и порядок. Возьми контроль в свои руки."},
    {"name": "Иерофант", "img": "05-TheHierophant.png", "description": "Обратись к традициям или наставнику. Тебя ждёт важный урок."},
    {"name": "Влюблённые", "img": "06-TheLovers.png", "description": "Скоро придётся сделать важный выбор, особенно в отношениях."},
    {"name": "Колесница", "img": "07-TheChariot.png", "description": "Победа близка. Управляй эмоциями и двигайся вперёд."},
    {"name": "Сила", "img": "08-Strength.png", "description": "Внутренняя сила поможет справиться с любыми трудностями."},
    {"name": "Отшельник", "img": "09-TheHermit.png", "description": "Время уединения и размышлений. Мудрость придёт через тишину."},
    {"name": "Колесо Фортуны", "img": "10-WheelOfFortune.png", "description": "Жизнь готовит поворот. Прими перемены как возможность."},
    {"name": "Справедливость", "img": "11-Justice.png", "description": "Всё вернётся. Будь честен с собой и другими."},
    {"name": "Повешенный", "img": "12-TheHangedMan.png", "description": "Нужно отпустить ситуацию и посмотреть на неё под другим углом."},
    {"name": "Смерть", "img": "13-Death.png", "description": "Что-то заканчивается, чтобы освободить место для нового."},
    {"name": "Умеренность", "img": "14-Temperance.png", "description": "Найди баланс. Не спеши, позволь событиям развиваться."},
    {"name": "Дьявол", "img": "15-TheDevil.png", "description": "Ты можешь быть привязан к тому, что тебе не служит. Освободись."},
    {"name": "Башня", "img": "16-TheTower.png", "description": "Старые конструкции рушатся. Прими это как очищение."},
    {"name": "Звезда", "img": "17-TheStar.png", "description": "Надежда и вдохновение с тобой. Верь в лучшее."},
    {"name": "Луна", "img": "18-TheMoon.png", "description": "Не всё так, как кажется. Доверяй интуиции."},
    {"name": "Солнце", "img": "19-TheSun.png", "description": "Радость, успех, тепло. Наслаждайся моментом."},
    {"name": "Суд", "img": "20-Judgement.png", "description": "Пришло время подвести итоги. Ты готов к новому этапу."},
    {"name": "Мир", "img": "21-TheWorld.png", "description": "Цикл завершён. Ты достигнешь цели и обретёшь гармонию."},
    # Жезлы
    {"name": "Туз Жезлов", "img": "Wands01.png", "description": "Новая энергия врывается в твою жизнь. Действуй!"},
    {"name": "Двойка Жезлов", "img": "Wands02.png", "description": "Планирование и выбор. Взвесь варианты."},
    {"name": "Тройка Жезлов", "img": "Wands03.png", "description": "Прогресс и расширение. Твои усилия приносят плоды."},
    {"name": "Четвёрка Жезлов", "img": "Wands04.png", "description": "Праздник и стабильность. Отпразднуй то, чего достиг."},
    {"name": "Пятёрка Жезлов", "img": "Wands05.png", "description": "Конфликт или конкуренция. Не избегай борьбы."},
    {"name": "Шестёрка Жезлов", "img": "Wands06.png", "description": "Победа и признание. Гордись собой."},
    {"name": "Семёрка Жезлов", "img": "Wands07.png", "description": "Защита своих позиций. Будь стоек."},
    {"name": "Восьмёрка Жезлов", "img": "Wands08.png", "description": "Скорость и движение. Будь готов к новостям."},
    {"name": "Девятка Жезлов", "img": "Wands09.png", "description": "Ты почти у цели. Не сдавайся."},
    {"name": "Десятка Жезлов", "img": "Wands10.png", "description": "Ты взвалил слишком много. Пора разделить ответственность."},
    {"name": "Паж Жезлов", "img": "Wands11.png", "description": "Новые идеи и энтузиазм. Пора действовать."},
    {"name": "Рыцарь Жезлов", "img": "Wands12.png", "description": "Страсть и импульс. Будь осторожен."},
    {"name": "Королева Жезлов", "img": "Wands13.png", "description": "Уверенность и независимость. Будь лидером."},
    {"name": "Король Жезлов", "img": "Wands14.png", "description": "Видение и лидерство. Действуй масштабно."},
    # Кубки
    {"name": "Туз Кубков", "img": "Cups01.png", "description": "Новое чувство или любовь. Открой сердце."},
    {"name": "Двойка Кубков", "img": "Cups02.png", "description": "Союз и партнёрство. Отношения будут гармоничными."},
    {"name": "Тройка Кубков", "img": "Cups03.png", "description": "Дружба и праздник. Раздели счастье с близкими."},
    {"name": "Четвёрка Кубков", "img": "Cups04.png", "description": "Апатия и размышления. Возможно, ты упускаешь важное."},
    {"name": "Пятёрка Кубков", "img": "Cups05.png", "description": "Потеря и печаль. Но не всё потеряно."},
    {"name": "Шестёрка Кубков", "img": "Cups06.png", "description": "Ностальгия и прошлое. Старые связи могут принести радость."},
    {"name": "Семёрка Кубков", "img": "Cups07.png", "description": "Иллюзии и мечты. Отдели фантазии от реальности."},
    {"name": "Восьмёрка Кубков", "img": "Cups08.png", "description": "Уход от того, что не приносит счастья. Пора двигаться дальше."},
    {"name": "Девятка Кубков", "img": "Cups09.png", "description": "Исполнение желаний. Ты получишь то, о чём мечтал."},
    {"name": "Десятка Кубков", "img": "Cups10.png", "description": "Семейное счастье и гармония. Впереди мир и радость."},
    {"name": "Паж Кубков", "img": "Cups11.png", "description": "Предложение или новое чувство. Будь открыт."},
    {"name": "Рыцарь Кубков", "img": "Cups12.png", "description": "Романтический порыв. Тебя ждёт приглашение."},
    {"name": "Королева Кубков", "img": "Cups13.png", "description": "Сострадание и мудрость. Слушай своё сердце."},
    {"name": "Король Кубков", "img": "Cups14.png", "description": "Эмоциональная зрелость. Ты способен помогать другим."},
    # Мечи
    {"name": "Туз Мечей", "img": "Swords01.png", "description": "Ясность и прорыв. Правда выйдет наружу."},
    {"name": "Двойка Мечей", "img": "Swords02.png", "description": "Тупик и нежелание выбирать. Пора принять решение."},
    {"name": "Тройка Мечей", "img": "Swords03.png", "description": "Боль и разочарование. Дай себе время исцелиться."},
    {"name": "Четвёрка Мечей", "img": "Swords04.png", "description": "Отдых и восстановление. Тебе нужна пауза."},
    {"name": "Пятёрка Мечей", "img": "Swords05.png", "description": "Конфликт, в котором нет победителей. Иногда лучше отступить."},
    {"name": "Шестёрка Мечей", "img": "Swords06.png", "description": "Переход и исцеление. Ты оставляешь позади трудности."},
    {"name": "Семёрка Мечей", "img": "Swords07.png", "description": "Хитрость или обман. Будь бдителен."},
    {"name": "Восьмёрка Мечей", "img": "Swords08.png", "description": "Ограничения, которые ты сам создал. Ты сильнее, чем думаешь."},
    {"name": "Девятка Мечей", "img": "Swords09.png", "description": "Тревога и страхи. Не позволяй мыслям управлять тобой."},
    {"name": "Десятка Мечей", "img": "Swords10.png", "description": "Крах, но это конец страданий. После падения будет подъём."},
    {"name": "Паж Мечей", "img": "Swords11.png", "description": "Любопытство и бдительность. Будь осторожен."},
    {"name": "Рыцарь Мечей", "img": "Swords12.png", "description": "Скорость и решительность. Действуй быстро."},
    {"name": "Королева Мечей", "img": "Swords13.png", "description": "Честность и независимость. Защищай свои границы."},
    {"name": "Король Мечей", "img": "Swords14.png", "description": "Интеллект и авторитет. Принимай решения холодным умом."},
    # Пентакли
    {"name": "Туз Пентаклей", "img": "Pentacles01.png", "description": "Новая возможность, ресурс. Деньги или работа придут."},
    {"name": "Двойка Пентаклей", "img": "Pentacles02.png", "description": "Баланс между делами. Учись распределять энергию."},
    {"name": "Тройка Пентаклей", "img": "Pentacles03.png", "description": "Команда и мастерство. Работа в сотрудничестве принесёт плоды."},
    {"name": "Четвёрка Пентаклей", "img": "Pentacles04.png", "description": "Контроль и стабильность. Храни нажитое."},
    {"name": "Пятёрка Пентаклей", "img": "Pentacles05.png", "description": "Трудности и нехватка. Не бойся просить помощи."},
    {"name": "Шестёрка Пентаклей", "img": "Pentacles06.png", "description": "Щедрость и помощь. Будь открыт к дару."},
    {"name": "Семёрка Пентаклей", "img": "Pentacles07.png", "description": "Терпение и ожидание. Посеянное скоро прорастёт."},
    {"name": "Восьмёрка Пентаклей", "img": "Pentacles08.png", "description": "Усердие и мастерство. Учись и совершенствуй навыки."},
    {"name": "Девятка Пентаклей", "img": "Pentacles09.png", "description": "Уют и самодостаточность. Наслаждайся."},
    {"name": "Десятка Пентаклей", "img": "Pentacles10.png", "description": "Наследие и богатство. Семейные ценности."},
    {"name": "Паж Пентаклей", "img": "Pentacles11.png", "description": "Обучение, новая работа. Впереди полезный опыт."},
    {"name": "Рыцарь Пентаклей", "img": "Pentacles12.png", "description": "Надёжность и упорство. Двигайся к цели без спешки."},
    {"name": "Королева Пентаклей", "img": "Pentacles13.png", "description": "Забота и изобилие. Умей создавать уют."},
    {"name": "Король Пентаклей", "img": "Pentacles14.png", "description": "Успех и процветание. Финансовая стабильность."}
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
                
                # Обычный пользователь
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
                
                # Проверка премиума
                if u.get("premium") and u.get("premium_until"):
                    if now > datetime.fromisoformat(u["premium_until"]):
                        u["premium"] = False
                        u["premium_until"] = None
                
                # Сброс счётчика в начале месяца
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
