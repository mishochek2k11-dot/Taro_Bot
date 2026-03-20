import logging
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, PreCheckoutQueryHandler
from config import BOT_TOKEN
from handlers.start import start_command
from handlers.commands import card_command, three_command, question_command
from handlers.payments import buy_command, buy_callback, pre_checkout, successful_payment
from handlers.status import status_command, stats_command

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def main():
    """Запуск бота"""
    # Создаём приложение
    application = Application.builder().token(BOT_TOKEN).build()

    # Регистрируем обработчики команд
    application.add_handler(CommandHandler("
