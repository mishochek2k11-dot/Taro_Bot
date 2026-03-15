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
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("card", card_command))
    application.add_handler(CommandHandler("three", three_command))
    application.add_handler(CommandHandler("question", question_command))
    application.add_handler(CommandHandler("buy", buy_command))
    application.add_handler(CommandHandler("status", status_command))
    application.add_handler(CommandHandler("stats", stats_command))

    # Обработчики платежей
    application.add_handler(CallbackQueryHandler(buy_callback, pattern="^buy_premium$"))
    application.add_handler(PreCheckoutQueryHandler(pre_checkout))
    application.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment))

    # Запускаем бота
    application.run_polling()

if __name__ == '__main__':
    main()
