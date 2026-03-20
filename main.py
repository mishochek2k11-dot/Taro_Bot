from http.server import BaseHTTPRequestHandler
import json
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler
from config import BOT_TOKEN
from handlers.start import start_command

# Создаём приложение
application = ApplicationBuilder().token(BOT_TOKEN).build()
application.add_handler(CommandHandler("start", start_command))

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"Bot is alive")
    
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        # Превращаем строку в словарь (dict)
        try:
            update_dict = json.loads(post_data.decode('utf-8'))
        except Exception as e:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(f"Invalid JSON: {e}".encode())
            return
        
        # Передаём словарь в Update.de_json
        try:
            update = Update.de_json(update_dict, application.bot)
            application.update_queue.put_nowait(update)
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f"Update error: {e}".encode())
            return
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"ok": True}).encode())
