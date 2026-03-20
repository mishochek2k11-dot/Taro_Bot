from http.server import BaseHTTPRequestHandler
import json
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from config import BOT_TOKEN

logging.basicConfig(level=logging.INFO)

# Самый простой обработчик
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Бот работает!")
    logging.info("start command received")

# Создаём приложение
app = Application.builder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))

# Vercel handler
class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is alive")
    
    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        data = self.rfile.read(length)
        try:
            update = Update.de_json(json.loads(data), app.bot)
            app.update_queue.put_nowait(update)
            logging.info("POST received and queued")
        except Exception as e:
            logging.error(f"POST error: {e}")
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"ok")
