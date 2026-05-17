from http.server import BaseHTTPRequestHandler
import json
import requests
import os

BOT_TOKEN = "8279893361:AAF5MW-v6m-JIMI0-pWSXf1yZLY963j50yw"
KV_REST_API_URL = os.environ.get("KV_REST_API_URL")
KV_REST_API_TOKEN = os.environ.get("KV_REST_API_TOKEN")

def kv_set(key, value):
    try:
        url = f"{KV_REST_API_URL}/set/{key}"
        requests.post(url, headers={"Authorization": f"Bearer {KV_REST_API_TOKEN}"}, json={"value": value})
    except Exception as e:
        print(f"KV set error: {e}")

def kv_get(key):
    try:
        url = f"{KV_REST_API_URL}/get/{key}"
        r = requests.get(url, headers={"Authorization": f"Bearer {KV_REST_API_TOKEN}"})
        if r.status_code == 200:
            return r.json().get("result")
    except Exception as e:
        print(f"KV get error: {e}")
    return None

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": text, "parse_mode": "Markdown"})

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
                user_id = str(update["message"]["from"]["id"])
                text = update["message"].get("text", "")

                if text == "/start":
                    # Проверяем KV
                    kv_set(f"test:{user_id}", "hello")
                    value = kv_get(f"test:{user_id}")
                    if value:
                        send_message(chat_id, f"✅ Бот работает!\nKV подключена. Запись: {value}")
                    else:
                        send_message(chat_id, "⚠️ Бот работает, но KV не отвечает")
                else:
                    send_message(chat_id, "❌ Неизвестная команда. /start")
        except Exception as e:
            print(f"Error: {e}")

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"ok")
