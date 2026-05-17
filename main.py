from http.server import BaseHTTPRequestHandler
from vercel_kv import KV

kv = KV()

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is alive")
