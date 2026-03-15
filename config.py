import os
from dotenv import load_dotenv

load_dotenv()

# Токены
BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

# Настройки лимитов
FREE_ATTEMPTS_PER_DAY = 3  # 3 бесплатные попытки в день
PREMIUM_PRICE_STARS = 50    # Стоимость подписки в Stars
PREMIUM_DURATION_DAYS = 30  # Длительность подписки
