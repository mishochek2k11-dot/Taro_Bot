from http.server import BaseHTTPRequestHandler
import json
import requests

BOT_TOKEN = "8279893361:AAF5MW-v6m-JIMI0-pWSXf1yZlY963j5Oyw"

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
            if "message" in update and "text" in update["message"]:
                chat_id = update["message"]["chat"]["id"]
                text = update["message"]["text"]
                
                if text == "/start":
                    reply = "✅ Бот работает!"
                else:
                    reply = f"Ты написал: {text}"
                
                url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
                requests.post(url, json={"chat_id": chat_id, "text": reply})
        except:
            pass
        
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"ok")
