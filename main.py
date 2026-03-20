from http.server import BaseHTTPRequestHandler
import json
import requests
import random
from datetime import datetime, timedelta
import os

BOT_TOKEN = "8279893361:AAF5MW-v6m-JIMI0-pWSXf1yZlY963j5Oyw"  
FREE_ATTEMPTS = 3
USERS_FILE = "/tmp/users.json"

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
    {"name": "Шут", "img": "00-TheFool.png", "description": "Тебя ждёт новое начало. Не бойся рискнуть — удача на твоей стороне. Доверься интуиции и сделай первый шаг."},
    {"name": "Маг", "img": "01-TheMagician.png", "description": "У тебя есть все ресурсы для достижения цели. Твои навыки и воля помогут воплотить задуманное. Сосредоточься и действуй — успех близок."},
    {"name": "Верховная Жрица", "img": "02-TheHighPriestess.png", "description": "Сейчас важно прислушаться к внутреннему голосу. Ответы уже есть внутри тебя. Позволь себе побыть в тишине и доверься интуиции."},
    {"name": "Императрица", "img": "03-TheEmpress.png", "description": "Время созидания и заботы. Отношения будут развиваться, а в делах придёт плодотворный период. Окружай себя красотой и заботой о близких."},
    {"name": "Император", "img": "04-TheEmperor.png", "description": "Нужна структура и порядок. Возьми контроль в свои руки, прояви твёрдость. Твоя решительность приведёт к стабильности и защите."},
    {"name": "Иерофант", "img": "05-TheHierophant.png", "description": "Обратись к традициям или наставнику. Возможно, тебе предстоит обучение или важный совет. Следуй проверенным путям."},
    {"name": "Влюблённые", "img": "06-TheLovers.png", "description": "Скоро придётся сделать важный выбор, особенно в отношениях. Слушай сердце, но не забывай о разуме. Этот выбор определит твой путь."},
    {"name": "Колесница", "img": "07-TheChariot.png", "description": "Победа близка, но нужна дисциплина. Управляй своими эмоциями и двигайся вперёд с уверенностью. Ты сможешь преодолеть препятствия."},
    {"name": "Сила", "img": "08-Strength.png", "description": "Внутренняя сила поможет справиться с любыми трудностями. Прояви терпение и доброту — это принесёт больше пользы, чем агрессия."},
    {"name": "Отшельник", "img": "09-TheHermit.png", "description": "Пришло время уединения и размышлений. Отойди от суеты, чтобы найти истинные ответы внутри себя. Мудрость придёт через тишину."},
    {"name": "Колесо Фортуны", "img": "10-WheelOfFortune.png", "description": "Жизнь готовит поворот. Скоро всё изменится, и не в твоей власти это контролировать. Прими перемены как возможность."},
    {"name": "Справедливость", "img": "11-Justice.png", "description": "Всё вернётся. Будь честен с собой и другими. То, что ты заслуживаешь, придёт к тебе в нужный момент."},
    {"name": "Повешенный", "img": "12-TheHangedMan.png", "description": "Нужно отпустить ситуацию и посмотреть на неё под другим углом. Иногда жертва — это путь к новому пониманию."},
    {"name": "Смерть", "img": "13-Death.png", "description": "Что-то заканчивается, чтобы освободить место для нового. Не бойся перемен — они принесут обновление."},
    {"name": "Умеренность", "img": "14-Temperance.png", "description": "Найди баланс. Не спеши, позволь событиям развиваться естественно. Терпение и гармония приведут к цели."},
    {"name": "Дьявол", "img": "15-TheDevil.png", "description": "Ты можешь быть привязан к тому, что тебе не служит. Освободись от зависимостей и посмотри на ситуацию трезво."},
    {"name": "Башня", "img": "16-TheTower.png", "description": "Ожидай неожиданного. Старые конструкции рушатся, но это освобождает место для истины. Прими это как очищение."},
    {"name": "Звезда", "img": "17-TheStar.png", "description": "Надежда и вдохновение с тобой. Даже если сейчас темно, скоро зажжётся свет. Верь в лучшее."},
    {"name": "Луна", "img": "18-TheMoon.png", "description": "Не всё так, как кажется. Доверяй интуиции, но не поддавайся страхам. Скоро всё прояснится."},
    {"name": "Солнце", "img": "19-TheSun.png", "description": "Радость, успех, тепло. Впереди светлый период. Наслаждайся моментом и делись счастьем с другими."},
    {"name": "Суд", "img": "20-Judgement.png", "description": "Пришло время подвести итоги. Старое уходит, ты готов к новому этапу. Услышь свой внутренний призыв."},
    {"name": "Мир", "img": "21-TheWorld.png", "description": "Цикл завершён. Ты достигнешь цели, обретёшь целостность и гармонию. Это время наград и завершений."},
    # Жезлы
    {"name": "Туз Жезлов", "img": "Wands-01-Ace.png", "description": "Новая энергия врывается в твою жизнь. Страсть, вдохновение, начало проекта. Действуй!"},
    {"name": "Двойка Жезлов", "img": "Wands-02-Two.png", "description": "Планирование и выбор. Ты стоишь перед решением, которое определит твой путь. Взвесь варианты."},
    {"name": "Тройка Жезлов", "img": "Wands-03-Three.png", "description": "Прогресс и расширение. Твои усилия приносят первые плоды. Смотри вперёд с уверенностью."},
    {"name": "Четвёрка Жезлов", "img": "Wands-04-Four.png", "description": "Праздник и стабильность. Дом, семья, радость. Отпразднуй то, чего достиг."},
    {"name": "Пятёрка Жезлов", "img": "Wands-05-Five.png", "description": "Конфликт или конкуренция. Не избегай борьбы, но не позволяй ей разрушить важное."},
    {"name": "Шестёрка Жезлов", "img": "Wands-06-Six.png", "description": "Победа и признание. Твои заслуги будут замечены. Гордись собой."},
    {"name": "Семёрка Жезлов", "img": "Wands-07-Seven.png", "description": "Защита своих позиций. Придётся отстаивать своё мнение. Будь стоек."},
    {"name": "Восьмёрка Жезлов", "img": "Wands-08-Eight.png", "description": "Скорость и движение. События будут развиваться быстро. Будь готов к новостям."},
    {"name": "Девятка Жезлов", "img": "Wands-09-Nine.png", "description": "Ты почти у цели. Последнее усилие — и ты справишься. Не сдавайся."},
    {"name": "Десятка Жезлов", "img": "Wands-10-Ten.png", "description": "Ты взвалил на себя слишком много. Пора разделить ответственность или отпустить лишнее."},
    {"name": "Паж Жезлов", "img": "Wands-11-Page.png", "description": "Новые идеи и энтузиазм. Пора действовать, даже если план ещё не идеален."},
    {"name": "Рыцарь Жезлов", "img": "Wands-12-Knight.png", "description": "Страсть и импульс. Ты готов к приключениям, но не забывай о последствиях."},
    {"name": "Королева Жезлов", "img": "Wands-13-Queen.png", "description": "Уверенность и независимость. Ты привлекаешь людей своей энергией. Будь лидером."},
    {"name": "Король Жезлов", "img": "Wands-14-King.png", "description": "Видение и лидерство. Ты способен вдохновить других. Действуй масштабно."},
    # Кубки
    {"name": "Туз Кубков", "img": "Cups-01-Ace.png", "description": "Новое чувство или любовь. Открой сердце — оно приведёт к радости."},
    {"name": "Двойка Кубков", "img": "Cups-02-Two.png", "description": "Союз и партнёрство. Отношения будут гармоничными. Встречай близкого человека."},
    {"name": "Тройка Кубков", "img": "Cups-03-Three.png", "description": "Дружба и праздник. Время радости и встреч. Раздели счастье с близкими."},
    {"name": "Четвёрка Кубков", "img": "Cups-04-Four.png", "description": "Апатия и размышления. Возможно, ты упускаешь что-то важное. Оглянись."},
    {"name": "Пятёрка Кубков", "img": "Cups-05-Five.png", "description": "Потеря и печаль. Но не всё потеряно — сосредоточься на том, что осталось."},
    {"name": "Шестёрка Кубков", "img": "Cups-06-Six.png", "description": "Ностальгия и прошлое. Старые связи могут принести радость или уроки."},
    {"name": "Семёрка Кубков", "img": "Cups-07-Seven.png", "description": "Иллюзии и мечты. Отдели фантазии от реальности. Выбери один путь."},
    {"name": "Восьмёрка Кубков", "img": "Cups-08-Eight.png", "description": "Уход от того, что не приносит счастья. Пора двигаться дальше, даже если страшно."},
    {"name": "Девятка Кубков", "img": "Cups-09-Nine.png", "description": "Исполнение желаний. Ты получишь то, о чём мечтал. Наслаждайся."},
    {"name": "Десятка Кубков", "img": "Cups-10-Ten.png", "description": "Семейное счастье и гармония. Впереди мир и радость."},
    {"name": "Паж Кубков", "img": "Cups-11-Page.png", "description": "Предложение или новое чувство. Будь открыт к приятным сюрпризам."},
    {"name": "Рыцарь Кубков", "img": "Cups-12-Knight.png", "description": "Романтический порыв. Тебя ждёт приглашение или красивое признание."},
    {"name": "Королева Кубков", "img": "Cups-13-Queen.png", "description": "Сострадание и мудрость. Слушай своё сердце и заботься о других."},
    {"name": "Король Кубков", "img": "Cups-14-King.png", "description": "Эмоциональная зрелость. Ты способен управлять чувствами и помогать другим."},
    # Мечи
    {"name": "Туз Мечей", "img": "Swords-01-Ace.png", "description": "Ясность и прорыв. Правда выйдет наружу, и ты увидишь ситуацию чётко."},
    {"name": "Двойка Мечей", "img": "Swords-02-Two.png", "description": "Тупик и нежелание выбирать. Пора принять решение, даже если оно сложное."},
    {"name": "Тройка Мечей", "img": "Swords-03-Three.png", "description": "Боль и разочарование. Дай себе время исцелиться."},
    {"name": "Четвёрка Мечей", "img": "Swords-04-Four.png", "description": "Отдых и восстановление. Тебе нужна пауза. Отдохни, чтобы вернуться сильнее."},
    {"name": "Пятёрка Мечей", "img": "Swords-05-Five.png", "description": "Конфликт, в котором нет победителей. Иногда лучше отступить."},
    {"name": "Шестёрка Мечей", "img": "Swords-06-Six.png", "description": "Переход и исцеление. Ты оставляешь позади трудности и двигаешься к спокойствию."},
    {"name": "Семёрка Мечей", "img": "Swords-07-Seven.png", "description": "Хитрость или обман. Будь бдителен и не доверяй всему без проверки."},
    {"name": "Восьмёрка Мечей", "img": "Swords-08-Eight.png", "description": "Ограничения, которые ты сам создал. Ты сильнее, чем думаешь."},
    {"name": "Девятка Мечей", "img": "Swords-09-Nine.png", "description": "Тревога и страхи. Не позволяй мыслям управлять тобой."},
    {"name": "Десятка Мечей", "img": "Swords-10-Ten.png", "description": "Крах, но это конец страданий. После падения будет новый подъём."},
    {"name": "Паж Мечей", "img": "Swords-11-Page.png", "description": "Любопытство и бдительность. Узнавай новое, но будь осторожен."},
    {"name": "Рыцарь Мечей", "img": "Swords-12-Knight.png", "description": "Скорость и решительность. Действуй быстро, но не навреди."},
    {"name": "Королева Мечей", "img": "Swords-13-Queen.png", "description": "Честность и независимость. Будь прямым и защищай свои границы."},
    {"name": "Король Мечей", "img": "Swords-14-King.png", "description": "Интеллект и авторитет. Принимай решения холодным умом."},
    # Пентакли
    {"name": "Туз Пентаклей", "img": "Pentacles-01-Ace.png", "description": "Новая возможность, ресурс. Деньги или работа придут к тебе."},
    {"name": "Двойка Пентаклей", "img": "Pentacles-02-Two.png", "description": "Баланс между делами. Учись распределять энергию."},
    {"name": "Тройка Пентаклей", "img": "Pentacles-03-Three.png", "description": "Команда и мастерство. Работа в сотрудничестве принесёт плоды."},
    {"name": "Четвёрка Пентаклей", "img": "Pentacles-04-Four.png", "description": "Контроль и стабильность. Храни нажитое, но не зацикливайся."},
    {"name": "Пятёрка Пентаклей", "img": "Pentacles-05-Five.png", "description": "Трудности и нехватка. Не бойся просить помощи."},
    {"name": "Шестёрка Пентаклей", "img": "Pentacles-06-Six.png", "description": "Щедрость и помощь. Будь открыт к дару или поделись с другими."},
    {"name": "Семёрка Пентаклей", "img": "Pentacles-07-Seven.png", "description": "Терпение и ожидание. Посеянное скоро прорастёт. Не торопись."},
    {"name": "Восьмёрка Пентаклей", "img": "Pentacles-08-Eight.png", "description": "Усердие и мастерство. Учись и совершенствуй навыки."},
    {"name": "Девятка Пентаклей", "img": "Pentacles-09-Nine.png", "description": "Уют и самодостаточность. Ты создал себе комфорт. Наслаждайся."},
    {"name": "Десятка Пентаклей", "img": "Pentacles-10-Ten.png", "description": "Наследие и богатство. Семейные ценности и стабильность."},
    {"name": "Паж Пентаклей", "img": "Pentacles-11-Page.png", "description": "Обучение, новая работа. Впереди полезный опыт."},
    {"name": "Рыцарь Пентаклей", "img": "Pentacles-12-Knight.png", "description": "Надёжность и упорство. Двигайся к цели без спешки."},
    {"name": "Королева Пентаклей", "img": "Pentacles-13-Queen.png", "description": "Забота и изобилие. Умей создавать уют и помогать другим."},
    {"name": "Король Пентаклей", "img": "Pentacles-14-King.png", "description": "Успех и процветание. Финансовая стабильность и мудрость."}
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
                    users[user_id] = {"attempts": 0, "month": now}
                
                u = users[user_id]
                
                # Сброс счётчика в начале месяца
                if u["month"] != now:
                    u["attempts"] = 0
                    u["month"] = now
                
                if text == "/start":
                    keyboard = [
                        [{"text": "🔮 Расклад на жизнь", "callback_data": "life"}],
                        [{"text": "❤️ Расклад на отношения", "callback_data": "love"}],
                        [{"text": "💼 Расклад на работу", "callback_data": "work"}],
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
                    users[user_id] = {"attempts": 0, "month": now}
                u = users[user_id]
                
                if u["month"] != now:
                    u["attempts"] = 0
                    u["month"] = now
                
                if data_cb == "status":
                    remaining = FREE_ATTEMPTS - u["attempts"]
                    text = f"📊 **Ваш статус**\n\nОсталось бесплатных раскладов в этом месяце: {remaining}"
                    edit_message(chat_id, message_id, text, [[{"text": "🔙 Назад", "callback_data": "back"}]])
                
                elif data_cb == "back":
                    keyboard = [
                        [{"text": "🔮 Расклад на жизнь", "callback_data": "life"}],
                        [{"text": "❤️ Расклад на отношения", "callback_data": "love"}],
                        [{"text": "💼 Расклад на работу", "callback_data": "work"}],
                        [{"text": "📊 Статус", "callback_data": "status"}]
                    ]
                    edit_message(chat_id, message_id, "✨ Выбери тему расклада:", keyboard)
                
                elif data_cb in ["life", "love", "work"]:
                    if u["attempts"] >= FREE_ATTEMPTS:
                        edit_message(chat_id, message_id, f"❌ Лимит {FREE_ATTEMPTS} раскладов в этом месяце исчерпан.")
                        save_users(users)
                        return
                    
                    card = get_card()
                    if data_cb == "life":
                        title = "Расклад на жизнь"
                    elif data_cb == "love":
                        title = "Расклад на отношения"
                    else:
                        title = "Расклад на работу"
                    
                    send_photo(chat_id, card["img"], title, card["description"])
                    u["attempts"] += 1
                    remaining = FREE_ATTEMPTS - u["attempts"]
                    send_message(chat_id, f"Осталось раскладов в этом месяце: {remaining}")
                
                save_users(users)
                answer_url = f"https://api.telegram.org/bot{BOT_TOKEN}/answerCallbackQuery"
                requests.post(answer_url, json={"callback_query_id": query["id"]})
        
        except Exception as e:
            print(f"Error: {e}")
        
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"ok") 
