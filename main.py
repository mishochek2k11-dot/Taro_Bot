from http.server import BaseHTTPRequestHandler
import json
import requests
import random
from datetime import datetime, timedelta
import os

BOT_TOKEN = "8279893361:AAF5MW-v6m-JIMI0-pWSXf1yZlY963j5Oyw"  
FREE_ATTEMPTS = 3
USERS_FILE = "/tmp/users.json"

# === РАБОТА С ФАЙЛОМ ПОЛЬЗОВАТЕЛЕЙ ===
def load_users():
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_users(data):
    try:
        with open(USERS_FILE, "w") as f:
            json.dump(data, f)
    except:
        pass

# === ВСЕ 78 КАРТ С ПОДРОБНЫМИ ОПИСАНИЯМИ ===
CARDS = [
    {"name": "Шут", "img": "fool.jpg", "description": "Тебя ждёт новое начало. Возможно, ты стоишь на пороге важного события. Не бойся рискнуть — удача на твоей стороне. Доверься интуиции и сделай первый шаг."},
    {"name": "Маг", "img": "magician.jpg", "description": "У тебя есть все ресурсы для достижения цели. Твои навыки и воля помогут воплотить задуманное. Сосредоточься и действуй — успех близок."},
    {"name": "Верховная Жрица", "img": "high_priestess.jpg", "description": "Сейчас важно прислушаться к внутреннему голосу. Ответы уже есть внутри тебя. Позволь себе побыть в тишине и доверься интуиции."},
    {"name": "Императрица", "img": "empress.jpg", "description": "Время созидания и заботы. Отношения будут развиваться, а в делах придёт плодотворный период. Окружай себя красотой и заботься о близких."},
    {"name": "Император", "img": "emperor.jpg", "description": "Нужна структура и порядок. Возьми контроль в свои руки, прояви твёрдость. Твоя решительность приведёт к стабильности и защите."},
    {"name": "Иерофант", "img": "hierophant.jpg", "description": "Обратись к традициям или наставнику. Возможно, тебе предстоит обучение или важный совет. Следуй проверенным путям."},
    {"name": "Влюблённые", "img": "lovers.jpg", "description": "Скоро придётся сделать важный выбор, особенно в отношениях. Слушай сердце, но не забывай о разуме. Этот выбор определит твой путь."},
    {"name": "Колесница", "img": "chariot.jpg", "description": "Победа близка, но нужна дисциплина. Управляй своими эмоциями и двигайся вперёд с уверенностью. Ты сможешь преодолеть препятствия."},
    {"name": "Сила", "img": "strength.jpg", "description": "Внутренняя сила поможет справиться с любыми трудностями. Прояви терпение и доброту — это принесёт больше пользы, чем агрессия."},
    {"name": "Отшельник", "img": "hermit.jpg", "description": "Пришло время уединения и размышлений. Отойди от суеты, чтобы найти истинные ответы внутри себя. Мудрость придёт через тишину."},
    {"name": "Колесо Фортуны", "img": "wheel_of_fortune.jpg", "description": "Жизнь готовит поворот. Скоро всё изменится, и не в твоей власти это контролировать. Прими перемены как возможность."},
    {"name": "Справедливость", "img": "justice.jpg", "description": "Всё вернётся. Будь честен с собой и другими. То, что ты заслуживаешь, придёт к тебе в нужный момент."},
    {"name": "Повешенный", "img": "hanged_man.jpg", "description": "Нужно отпустить ситуацию и посмотреть на неё под другим углом. Иногда жертва — это путь к новому пониманию."},
    {"name": "Смерть", "img": "death.jpg", "description": "Что-то заканчивается, чтобы освободить место для нового. Не бойся перемен — они принесут обновление."},
    {"name": "Умеренность", "img": "temperance.jpg", "description": "Найди баланс. Не спеши, позволь событиям развиваться естественно. Терпение и гармония приведут к цели."},
    {"name": "Дьявол", "img": "devil.jpg", "description": "Ты можешь быть привязан к тому, что тебе не служит. Освободись от зависимостей и посмотри на ситуацию трезво."},
    {"name": "Башня", "img": "tower.jpg", "description": "Ожидай неожиданного. Старые конструкции рушатся, но это освобождает место для истины. Прими это как очищение."},
    {"name": "Звезда", "img": "star.jpg", "description": "Надежда и вдохновение с тобой. Даже если сейчас темно, скоро зажжётся свет. Верь в лучшее."},
    {"name": "Луна", "img": "moon.jpg", "description": "Не всё так, как кажется. Доверяй интуиции, но не поддавайся страхам. Скоро всё прояснится."},
    {"name": "Солнце", "img": "sun.jpg", "description": "Радость, успех, тепло. Впереди светлый период. Наслаждайся моментом и делись счастьем с другими."},
    {"name": "Суд", "img": "judgement.jpg", "description": "Пришло время подвести итоги. Старое уходит, ты готов к новому этапу. Услышь свой внутренний призыв."},
    {"name": "Мир", "img": "world.jpg", "description": "Цикл завершён. Ты достигнешь цели, обретёшь целостность и гармонию. Это время наград и завершений."},
    # Жезлы
    {"name": "Туз Жезлов", "img": "ace_of_wands.jpg", "description": "Новая энергия врывается в твою жизнь. Страсть, вдохновение, начало проекта. Действуй!"},
    {"name": "Двойка Жезлов", "img": "two_of_wands.jpg", "description": "Планирование и выбор. Ты стоишь перед решением, которое определит твой путь. Взвесь варианты."},
    {"name": "Тройка Жезлов", "img": "three_of_wands.jpg", "description": "Прогресс и расширение. Твои усилия приносят первые плоды. Смотри вперёд с уверенностью."},
    {"name": "Четвёрка Жезлов", "img": "four_of_wands.jpg", "description": "Праздник и стабильность. Дом, семья, радость. Отпразднуй то, чего достиг."},
    {"name": "Пятёрка Жезлов", "img": "five_of_wands.jpg", "description": "Конфликт или конкуренция. Не избегай борьбы, но не позволяй ей разрушить важное."},
    {"name": "Шестёрка Жезлов", "img": "six_of_wands.jpg", "description": "Победа и признание. Твои заслуги будут замечены. Гордись собой."},
    {"name": "Семёрка Жезлов", "img": "seven_of_wands.jpg", "description": "Защита своих позиций. Придётся отстаивать своё мнение. Будь стоек."},
    {"name": "Восьмёрка Жезлов", "img": "eight_of_wands.jpg", "description": "Скорость и движение. События будут развиваться быстро. Будь готов к новостям."},
    {"name": "Девятка Жезлов", "img": "nine_of_wands.jpg", "description": "Ты почти у цели. Последнее усилие — и ты справишься. Не сдавайся."},
    {"name": "Десятка Жезлов", "img": "ten_of_wands.jpg", "description": "Ты взвалил на себя слишком много. Пора разделить ответственность или отпустить лишнее."},
    {"name": "Паж Жезлов", "img": "page_of_wands.jpg", "description": "Новые идеи и энтузиазм. Пора действовать, даже если план ещё не идеален."},
    {"name": "Рыцарь Жезлов", "img": "knight_of_wands.jpg", "description": "Страсть и импульс. Ты готов к приключениям, но не забывай о последствиях."},
    {"name": "Королева Жезлов", "img": "queen_of_wands.jpg", "description": "Уверенность и независимость. Ты привлекаешь людей своей энергией. Будь лидером."},
    {"name": "Король Жезлов", "img": "king_of_wands.jpg", "description": "Видение и лидерство. Ты способен вдохновить других. Действуй масштабно."},
    # Кубки (14)
    {"name": "Туз Кубков", "img": "ace_of_cups.jpg", "description": "Новое чувство или любовь. Открой сердце — оно приведёт к радости."},
    {"name": "Двойка Кубков", "img": "two_of_cups.jpg", "description": "Союз и партнёрство. Отношения будут гармоничными. Встречай близкого человека."},
    {"name": "Тройка Кубков", "img": "three_of_cups.jpg", "description": "Дружба и праздник. Время радости и встреч. Раздели счастье с близкими."},
    {"name": "Четвёрка Кубков", "img": "four_of_cups.jpg", "description": "Апатия и размышления. Возможно, ты упускаешь что-то важное. Оглянись."},
    {"name": "Пятёрка Кубков", "img": "five_of_cups.jpg", "description": "Потеря и печаль. Но не всё потеряно — сосредоточься на том, что осталось."},
    {"name": "Шестёрка Кубков", "img": "six_of_cups.jpg", "description": "Ностальгия и прошлое. Старые связи могут принести радость или уроки."},
    {"name": "Семёрка Кубков", "img": "seven_of_cups.jpg", "description": "Иллюзии и мечты. Отдели фантазии от реальности. Выбери один путь."},
    {"name": "Восьмёрка Кубков", "img": "eight_of_cups.jpg", "description": "Уход от того, что не приносит счастья. Пора двигаться дальше, даже если страшно."},
    {"name": "Девятка Кубков", "img": "nine_of_cups.jpg", "description": "Исполнение желаний. Ты получишь то, о чём мечтал. Наслаждайся."},
    {"name": "Десятка Кубков", "img": "ten_of_cups.jpg", "description": "Семейное счастье и гармония. Впереди мир и радость."},
    {"name": "Паж Кубков", "img": "page_of_cups.jpg", "description": "Предложение или новое чувство. Будь открыт к приятным сюрпризам."},
    {"name": "Рыцарь Кубков", "img": "knight_of_cups.jpg", "description": "Романтический порыв. Тебя ждёт приглашение или красивое признание."},
    {"name": "Королева Кубков", "img": "queen_of_cups.jpg", "description": "Сострадание и мудрость. Слушай своё сердце и заботься о других."},
    {"name": "Король Кубков", "img": "king_of_cups.jpg", "description": "Эмоциональная зрелость. Ты способен управлять чувствами и помогать другим."},
    # Мечи (14)
    {"name": "Туз Мечей", "img": "ace_of_swords.jpg", "description": "Ясность и прорыв. Правда выйдет наружу, и ты увидишь ситуацию чётко."},
    {"name": "Двойка Мечей", "img": "two_of_swords.jpg", "description": "Тупик и нежелание выбирать. Пора принять решение, даже если оно сложное."},
    {"name": "Тройка Мечей", "img": "three_of_swords.jpg", "description": "Боль и разочарование. Дай себе время исцелиться."},
    {"name": "Четвёрка Мечей", "img": "four_of_swords.jpg", "description": "Отдых и восстановление. Тебе нужна пауза. Отдохни, чтобы вернуться сильнее."},
    {"name": "Пятёрка Мечей", "img": "five_of_swords.jpg", "description": "Конфликт, в котором нет победителей. Иногда лучше отступить."},
    {"name": "Шестёрка Мечей", "img": "six_of_swords.jpg", "description": "Переход и исцеление. Ты оставляешь позади трудности и двигаешься к спокойствию."},
    {"name": "Семёрка Мечей", "img": "seven_of_swords.jpg", "description": "Хитрость или обман. Будь бдителен и не доверяй всему без проверки."},
    {"name": "Восьмёрка Мечей", "img": "eight_of_swords.jpg", "description": "Ограничения, которые ты сам создал. Ты сильнее, чем думаешь."},
    {"name": "Девятка Мечей", "img": "nine_of_swords.jpg", "description": "Тревога и страхи. Не позволяй мыслям управлять тобой."},
    {"name": "Десятка Мечей", "img": "ten_of_swords.jpg", "description": "Крах, но это конец страданий. После падения будет новый подъём."},
    {"name": "Паж Мечей", "img": "page_of_swords.jpg", "description": "Любопытство и бдительность. Узнавай новое, но будь осторожен."},
    {"name": "Рыцарь Мечей", "img": "knight_of_swords.jpg", "description": "Скорость и решительность. Действуй быстро, но не навреди."},
    {"name": "Королева Мечей", "img": "queen_of_swords.jpg", "description": "Честность и независимость. Будь прямым и защищай свои границы."},
    {"name": "Король Мечей", "img": "king_of_swords.jpg", "description": "Интеллект и авторитет. Принимай решения холодным умом."},
    # Пентакли (14)
    {"name": "Туз Пентаклей", "img": "ace_of_pentacles.jpg", "description": "Новая возможность, ресурс. Деньги или работа придут к тебе."},
    {"name": "Двойка Пентаклей", "img": "two_of_pentacles.jpg", "description": "Баланс между делами. Учись распределять энергию."},
    {"name": "Тройка Пентаклей", "img": "three_of_pentacles.jpg", "description": "Команда и мастерство. Работа в сотрудничестве принесёт плоды."},
    {"name": "Четвёрка Пентаклей", "img": "four_of_pentacles.jpg", "description": "Контроль и стабильность. Храни нажитое, но не зацикливайся."},
    {"name": "Пятёрка Пентаклей", "img": "five_of_pentacles.jpg", "description": "Трудности и нехватка. Не бойся просить помощи."},
    {"name": "Шестёрка Пентаклей", "img": "six_of_pentacles.jpg", "description": "Щедрость и помощь. Будь открыт к дару или поделись с другими."},
    {"name": "Семёрка Пентаклей", "img": "seven_of_pentacles.jpg", "description": "Терпение и ожидание. Посеянное скоро прорастёт. Не торопись."},
    {"name": "Восьмёрка Пентаклей", "img": "eight_of_pentacles.jpg", "description": "Усердие и мастерство. Учись и совершенствуй навыки."},
    {"name": "Девятка Пентаклей", "img": "nine_of_pentacles.jpg", "description": "Уют и самодостаточность. Ты создал себе комфорт. Наслаждайся."},
    {"name": "Десятка Пентаклей", "img": "ten_of_pentacles.jpg", "description": "Наследие и богатство. Семейные ценности и стабильность."},
    {"name": "Паж Пентаклей", "img": "page_of_pentacles.jpg", "description": "Обучение, новая работа. Впереди полезный опыт."},
    {"name": "Рыцарь Пентаклей", "img": "knight_of_pentacles.jpg", "description": "Надёжность и упорство. Двигайся к цели без спешки."},
    {"name": "Королева Пентаклей", "img": "queen_of_pentacles.jpg", "description": "Забота и изобилие. Умей создавать уют и помогать другим."},
    {"name": "Король Пентаклей", "img": "king_of_pentacles.jpg", "description": "Успех и процветание. Финансовая стабильность и мудрость."}
]

def get_card():
    return random.choice(CARDS)

def send_photo(chat_id, image_name, caption, description):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    image_url = f"https://raw.githubusercontent.com/mishochek2k11-dot/Taro_Bot/main/images/{image_name}"
    full_text = f"🔮 **{caption}**\n\n{description}"
    requests.post(url, json={"chat_id": chat_id, "photo": image_url, "caption": full_text, "parse_mode": "Markdown"})

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
            users = load_users()
            
            if "message" in update:
                chat_id = update["message"]["chat"]["id"]
                text = update["message"].get("text", "")
                user_id = str(update["message"]["from"]["id"])
                
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
                
                save_users(users)
            
            elif "callback_query" in update:
                query = update["callback_query"]
                chat_id = query["message"]["chat"]["id"]
                message_id = query["message"]["message_id"]
                data_cb = query["data"]
                user_id = str(query["from"]["id"])
                
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
                        save_users(users)
                        return
                    
                    card = get_card()
                    if data_cb == "life":
                        emoji = "🔮"
                        title = "Расклад на жизнь"
                    elif data_cb == "love":
                        emoji = "❤️"
                        title = "Расклад на отношения"
                    else:
                        emoji = "💼"
                        title = "Расклад на работу"
                    
                    send_photo(chat_id, card["img"], title, card["description"])
                    use_attempt()
                    
                    if not u["premium"]:
                        remaining = FREE_ATTEMPTS - u["attempts"] + u["extra_attempts"]
                        send_message(chat_id, f"Осталось доступных раскладов: {remaining}")
                
                save_users(users)
                answer_url = f"https://api.telegram.org/bot{BOT_TOKEN}/answerCallbackQuery"
                requests.post(answer_url, json={"callback_query_id": query["id"]})
            
            elif "pre_checkout_query" in update:
                query = update["pre_checkout_query"]
                answer_url = f"https://api.telegram.org/bot{BOT_TOKEN}/answerPreCheckoutQuery"
                requests.post(answer_url, json={"pre_checkout_query_id": query["id"], "ok": True})
            
            elif "message" in update and "successful_payment" in update["message"]:
                user_id = str(update["message"]["from"]["id"])
                payload = update["message"]["successful_payment"]["payload"]
                
                now = datetime.now().strftime("%Y-%m")
                if user_id not in users:
                    users[user_id] = {"attempts": 0, "premium": False, "premium_until": None, "extra_attempts": 0, "month": now}
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
                
                save_users(users)
        
        except Exception as e:
            print(f"Error: {e}")
        
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"ok")
