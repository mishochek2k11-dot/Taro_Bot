from telegram import Update
from telegram.ext import ContextTypes
from services.database import get_user, check_attempts
from config import FREE_ATTEMPTS_PER_DAY

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /status - статус подписки и попыток"""
    user_id = update.effective_user.id
    user = await get_user(user_id)

    # Проверяем подписку
    if user.subscription_active:
        until = user.subscription_until.split('T')[0]
        status_text = f"🌟 **Статус:** Премиум (до {until})"
        attempts_text = "♾️ Безлимитные расклады"
    else:
        # Сколько осталось попыток
        _, remaining, _ = await check_attempts(user)
        status_text = "🆓 **Статус:** Бесплатный"
        attempts_text = f"Осталось попыток: {remaining} из {FREE_ATTEMPTS_PER_DAY}"

    await update.message.reply_text(
        f"📊 **Ваш профиль**\n\n"
        f"{status_text}\n"
        f"{attempts_text}\n"
        f"📈 Всего раскладов: {user.total_readings}",
        parse_mode='Markdown'
    )

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /stats - статистика пользователя"""
    user_id = update.effective_user.id
    user = await get_user(user_id)

    reg_date = user.registered_at.split('T')[0]

    await update.message.reply_text(
        f"📈 **Ваша статистика**\n\n"
        f"📅 Зарегистрировались: {reg_date}\n"
        f"🔮 Всего раскладов: {user.total_readings}\n"
        f"💰 Всего потрачено Stars: {sum(p.get('amount', 0) for p in user.payments) if user.payments else 0}",
        parse_mode='Markdown'
    )
