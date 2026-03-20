from http.server import BaseHTTPRequestHandler
import json
import logging
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from config import BOT_TOKEN, PREMIUM_PRICE_STARS, FREE_ATTEMPTS_PER_DAY

logging.basicConfig(level=logging.INFO)

# === ВСЯ ЛОГИКА БОТА ПРЯМО ЗДЕСЬ ===

# Словарь пользователей (в памяти, без базы данных)
users = {}

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in users:
        users[user_id] = {"attempts": 0, "premium": False}
    
    keyboard = [
        [InlineKeyboardButton("🔮 Одна карта", callback_data="card")],
        [InlineKeyboardButton("🃏 Три карты", callback_data="three")],
        [InlineKeyboardButton("❓ Задать вопрос", callback_data="question")],
        [InlineKeyboardButton("🌟 Купить подписку", callback_data="buy")]
    ]
    await update.message.reply_text(
        f"✨ Привет! Я бот Таро.\n\n"
        f"🔥 {FREE_ATTEMPTS_PER_DAY} бесплатных раскладов в день\n"
        f"🌟 Премиум: безлимит + AI\n\n"
        f"Выбери:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def card_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    
    if user_id not in users:
        users[user_id] = {"attempts": 0, "premium": False}
    
    user = users[user_id]
    if not user["premium"] and user["attempts"] >= FREE_ATTEMPTS_PER_DAY:
        await query.edit_message_text(
            f"❌ Лимит {FREE_ATTEMPTS_PER_DAY} бесплатных раскладов исчерпан.\n"
            f"Купи подписку за {PREMIUM_PRICE_STARS} Stars в месяц."
        )
        return
    
    # Случайная карта
    cards = ["Шут", "Маг", "Верховная Жрица", "Императрица", "Император", "Влюблённые"]
    card = random.choice(cards)
    meanings = {
        "Шут": "Новые начинания, спонтанность",
        "Маг": "Сила воли, мастерство",
        "Верховная Жрица": "Интуиция, тайные знания",
        "Императрица": "Изобилие, плодородие",
        "Император": "Власть, структура",
        "Влюблённые": "Выбор, отношения"
    }
    meaning = meanings.get(card, "Глубокое значение")
    
    await query.edit_message_text(
        f"🔮 **{card}**\n\n{meaning}\n\n"
        f"Осталось попыток: {FREE_ATTEMPTS_PER_DAY - user['attempts'] - 1 if not user['premium'] else '♾️'}"
    )
    
    if not user["premium"]:
        user["attempts"] += 1

async def buy_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_invoice(
        title="Премиум-подписка на месяц",
        description="Неограниченные расклады на 30 дней",
        payload="premium_month",
        currency="XTR",
        prices=[{"label": "Подписка", "amount": PREMIUM_PRICE_STARS}]
    )

async def pre_checkout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.pre_checkout_query.answer(ok=True)

async def successful_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in users:
        users[user_id] = {"attempts": 0, "premium": False}
    users[user_id]["premium"] = True
    users[user_id]["attempts"] = 0
    await update.message.reply_text("✅ Подписка активирована! Теперь безлимитные расклады.")

# === НАСТРОЙКА ПРИЛОЖЕНИЯ ===

application = ApplicationBuilder().token(BOT_TOKEN).build()

application.add_handler(CommandHandler("start", start_command))
application.add_handler(CallbackQueryHandler(card_callback, pattern="^card$"))
application.add_handler(CallbackQueryHandler(buy_callback, pattern="^buy$"))
application.add_handler(PreCheckoutQueryHandler(pre_checkout))
application.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment))

# === ОБРАБОТЧИК ДЛЯ VERCEL ===

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is alive")
    
    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        data = self.rfile.read(length)
        
        try:
            update_dict = json.loads(data.decode('utf-8'))
            update = Update.de_json(update_dict, application.bot)
            application.update_queue.put_nowait(update)
        except Exception as e:
            logging.error(f"Error: {e}")
            self.send_response(500)
            self.end_headers()
            return
        
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"ok")
