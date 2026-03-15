from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    user = update.effective_user

    # Создаём клавиатуру
    keyboard = [
        [InlineKeyboardButton("🔮 Одна карта", callback_data="card")],
        [InlineKeyboardButton("🃏 Три карты", callback_data="three")],
        [InlineKeyboardButton("❓ Задать вопрос", callback_data="question")],
        [InlineKeyboardButton("🌟 Купить подписку", callback_data="buy")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"✨ **Привет, {user.first_name}!** ✨\n\n"
        "Я — магический бот Таро. Задай вопрос, и карты покажут ответ.\n\n"
        "🔥 **3 бесплатных расклада в день**\n"
        "🌟 Премиум: безлимит + AI-толкования\n\n"
        "Выбери, что хочешь сделать:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )
