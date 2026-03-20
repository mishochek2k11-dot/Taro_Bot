from http.server import BaseHTTPRequestHandler
import json
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, PreCheckoutQueryHandler
from config import BOT_TOKEN
from handlers.start import start_command
from handlers.commands import card_command, three_command, question_command
from handlers.payments import buy_command, buy_callback, pre_checkout, successful_payment
from handlers.status import status_command, stats_command

logging.basicConfig(level=logging.INFO)

# Создаём приложение
application = ApplicationBuilder().token(BOT_TOKEN).build()

# Регистрируем обработчики
application.add_handler(CommandHandler("start", start_command))
application.add_handler(CommandHandler("card", card_command))
application.add_handler(CommandHandler("three", three_command))
application.add_handler(CommandHandler("question", question_command))
application.add_handler(CommandHandler("buy", buy_command))
application.add_handler(CommandHandler("status", status_command))
application.add_handler(CommandHandler("stats", stats_command))
application.add_handler(CallbackQueryHandler(buy_callback, pattern="^buy_premium$"))
application.add_handler(PreCheckoutQueryHandler(pre_checkout))
application.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment))

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"Bot is alive")
    
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        try:
            update_dict = json.loads(post_data.decode('utf-8'))
        except Exception as e:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(f"Invalid JSON: {e}".encode())
            return
        
        try:
            update = Update.de_json(update_dict, application.bot)
            application.update_queue.put_nowait(update)
        except Exception as e:
            logging.error(f"Update error: {e}")
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f"Update error: {e}".encode())
            return
        
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"ok")
