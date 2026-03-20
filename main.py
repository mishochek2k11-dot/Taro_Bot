from http.server import BaseHTTPRequestHandler
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler
from config import BOT_TOKEN
from handlers.start import start_command

# Создаём приложение
application = ApplicationBuilder().token(BOT_TOKEN).build()
application.add_handler(CommandHandler("start", start_command))

# Обработчик для Vercel
class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        # Отправляем обновление в приложение
        application.update_queue.put_nowait(Update.de_json(post_data.decode('utf-8'), application.bot))
        
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"ok")
    
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is alive")
