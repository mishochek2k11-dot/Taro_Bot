from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, PreCheckoutQueryHandler, MessageHandler, filters
from datetime import datetime, timedelta
from config import PREMIUM_PRICE_STARS, PREMIUM_DURATION_DAYS
from services.database import get_user, update_user

async def buy_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /buy - покупка подписки"""
    keyboard = [[InlineKeyboardButton("Купить подписку на месяц", callback_data="buy_premium")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🌟 **Премиум-доступ**\n\n"
        f"Стоимость: {PREMIUM_PRICE_STARS} Stars в месяц\n\n"
        "Преимущества:\n"
        "• ♾️ Безлимитные расклады\n"
        "• 🔮 Подробные AI-толкования\n"
        "• 📊 Полная статистика\n"
        "• ⭐️ Приоритетная поддержка",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def buy_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка нажатия на кнопку покупки"""
    query = update.callback_query
    await query.answer()

    if query.data == "buy_premium":
        # Создаём инвойс для оплаты Stars
        await query.message.reply_invoice(
            title="Премиум-подписка на месяц",
            description="Неограниченные расклады и AI-толкования на 30 дней",
            payload="premium_month",
            currency="XTR",  # XTR = Telegram Stars
            prices=[{"label": "Подписка", "amount": PREMIUM_PRICE_STARS}]
        )

async def pre_checkout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Проверка перед оплатой"""
    query = update.pre_checkout_query
    await query.answer(ok=True)  # Всегда разрешаем

async def successful_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка успешного платежа"""
    user_id = update.effective_user.id
    user = await get_user(user_id)

    # Активируем подписку
    user.subscription_active = True
    user.subscription_until = (datetime.now() + timedelta(days=PREMIUM_DURATION_DAYS)).isoformat()

    # Сохраняем информацию о платеже
    if user.payments is None:
        user.payments = []

    user.payments.append({
        "date": datetime.now().isoformat(),
        "amount": PREMIUM_PRICE_STARS,
        "currency": "XTR"
    })

    await update_user(user)

    await update.message.reply_text(
        "✅ **Оплата прошла успешно!**\n\n"
        f"Подписка активна до {user.subscription_until.split('T')[0]}.\n"
        "Спасибо за поддержку! ✨",
        parse_mode='Markdown'
    )
