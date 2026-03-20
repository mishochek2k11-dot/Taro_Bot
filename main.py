from http.server import BaseHTTPRequestHandler
import json
import logging
import random
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, PreCheckoutQueryHandler, MessageHandler, filters
from config import BOT_TOKEN, PREMIUM_PRICE_STARS

logging.basicConfig(level=logging.INFO)

FREE_ATTEMPTS = 3  # 3 попытки в месяц

users = {}

async def start(update, context):
    uid = update.effective_user.id
    if uid not in users:
        users[uid] = {"attempts": 0, "premium": False, "month": datetime.now().strftime("%Y-%m")}
    
    keyboard = [[InlineKeyboardButton("🔮 Карта", callback_data="card")],
                [InlineKeyboardButton("🃏 3 карты", callback_data="three")],
                [InlineKeyboardButton("🌟 Подписка", callback_data="buy")]]
    await update.message.reply_text("✨ Привет! 3 бесплатных расклада в месяц.", reply_markup=InlineKeyboardMarkup(keyboard))

async def card(update, context):
    q = update.callback_query
    await q.answer()
    uid = q.from_user.id
    now = datetime.now().strftime("%Y-%m")
    
    if uid not in users:
        users[uid] = {"attempts": 0, "premium": False, "month": now}
    u = users[uid]
    
    if u["month"] != now:
        u["attempts"] = 0
        u["month"] = now
    
    if not u["premium"] and u["attempts"] >= FREE_ATTEMPTS:
        await q.edit_message_text(f"❌ Лимит {FREE_ATTEMPTS} раскладов в месяц. Купи подписку за {PREMIUM_PRICE_STARS} Stars.")
        return
    
    cards = ["Шут", "Маг", "Жрица", "Императрица", "Император", "Влюблённые"]
    val = {"Шут": "Новое начало", "Маг": "Сила", "Жрица": "Интуиция", "Императрица": "Изобилие", "Император": "Власть", "Влюблённые": "Выбор"}
    c = random.choice(cards)
    text = f"🔮 {c}\n{val[c]}"
    
    if not u["premium"]:
        u["attempts"] += 1
        text += f"\n\nОсталось: {FREE_ATTEMPTS - u['attempts']} из {FREE_ATTEMPTS}"
    else:
        text += "\n♾️ Премиум"
    
    await q.edit_message_text(text)

async def three(update, context):
    q = update.callback_query
    await q.answer()
    uid = q.from_user.id
    now = datetime.now().strftime("%Y-%m")
    
    if uid not in users:
        users[uid] = {"attempts": 0, "premium": False, "month": now}
    u = users[uid]
    
    if u["month"] != now:
        u["attempts"] = 0
        u["month"] = now
    
    if not u["premium"] and u["attempts"] >= FREE_ATTEMPTS:
        await q.edit_message_text(f"❌ Лимит {FREE_ATTEMPTS} раскладов в месяц. Купи подписку за {PREMIUM_PRICE_STARS} Stars.")
        return
    
    cards = ["Шут", "Маг", "Жрица", "Императрица", "Император", "Влюблённые"]
    pos = ["Прошлое", "Настоящее", "Будущее"]
    text = "🃏 Расклад\n"
    for i in range(3):
        text += f"{pos[i]}: {random.choice(cards)}\n"
    
    if not u["premium"]:
        u["attempts"] += 1
        text += f"\nОсталось: {FREE_ATTEMPTS - u['attempts']} из {FREE_ATTEMPTS}"
    else:
        text += "\n♾️ Премиум"
    
    await q.edit_message_text(text)

async def buy(update, context):
    q = update.callback_query
    await q.answer()
    await q.message.reply_invoice(title="Премиум", description="Безлимит на месяц", payload="premium", currency="XTR", prices=[{"label": "Подписка", "amount": PREMIUM_PRICE_STARS}])

async def pre_checkout(update, context):
    await update.pre_checkout_query.answer(ok=True)

async def pay_ok(update, context):
    uid = update.effective_user.id
    users[uid] = {"attempts": 0, "premium": True, "month": datetime.now().strftime("%Y-%m")}
    await update.message.reply_text("✅ Подписка активна!")

app = Application.builder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(card, pattern="^card$"))
app.add_handler(CallbackQueryHandler(three, pattern="^three$"))
app.add_handler(CallbackQueryHandler(buy, pattern="^buy$"))
app.add_handler(PreCheckoutQueryHandler(pre_checkout))
app.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, pay_ok))

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is alive")
    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        data = self.rfile.read(length)
        try:
            app.update_queue.put_nowait(Update.de_json(json.loads(data), app.bot))
        except Exception as e:
            logging.error(f"POST error: {e}")
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"ok")
