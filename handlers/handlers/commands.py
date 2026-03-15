from telegram import Update, InputMediaPhoto
from telegram.ext import ContextTypes
from services.tarot import get_random_card, get_random_cards, format_card_message
from services.ai import get_ai_interpretation
from services.database import get_user, update_user, check_attempts
from config import PREMIUM_PRICE_STARS
import os

async def card_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик одной карты"""
    user_id = update.effective_user.id
    user = await get_user(user_id)

    # Проверяем лимиты
    can_proceed, remaining, limit_msg = await check_attempts(user)
    if not can_proceed:
        await update.message.reply_text(limit_msg, parse_mode='Markdown')
        return

    # Получаем карту
    card = get_random_card()
    text, image_file = format_card_message(card)

    # Отправляем картинку
    image_path = f"images/{image_file}"
    if os.path.exists(image_path):
        with open(image_path, "rb") as photo:
            await update.message.reply_photo(photo=photo, caption=text, parse_mode='Markdown')
    else:
        await update.message.reply_text(text, parse_mode='Markdown')

    # Обновляем счётчики
    if not user.subscription_active:
        user.attempts_used += 1
    user.total_readings += 1
    await update_user(user)

    # Показываем остаток
    if not user.subscription_active:
        await update.message.reply_text(f"Осталось бесплатных попыток: {remaining-1}")

async def three_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик трёх карт"""
    user_id = update.effective_user.id
    user = await get_user(user_id)

    can_proceed, remaining, limit_msg = await check_attempts(user)
    if not can_proceed:
        await update.message.reply_text(limit_msg, parse_mode='Markdown')
        return

    # Получаем 3 карты
    cards = get_random_cards(3)
    positions = ["Прошлое", "Настоящее", "Будущее"]

    # Создаём медиа-группу
    media_group = []
    for i, card in enumerate(cards):
        text = f"**{positions[i]}**\n{card['name']}\n\n_{card['meaning']}_"
        image_path = f"images/{card['image']}"
        if os.path.exists(image_path):
            with open(image_path, "rb") as photo:
                media_group.append(InputMediaPhoto(
                    media=photo,
                    caption=text if i == 0 else None,
                    parse_mode='Markdown'
                ))

    if media_group:
        await update.message.reply_media_group(media=media_group)
    else:
        # Если нет картинок, просто текстом
        response = "**Расклад на прошлое/настоящее/будущее:**\n\n"
        for i, card in enumerate(cards):
            response += f"**{positions[i]}**: {card['name']} — {card['meaning']}\n\n"
        await update.message.reply_text(response, parse_mode='Markdown')

    # Обновляем счётчики
    if not user.subscription_active:
        user.attempts_used += 1
    user.total_readings += 1
    await update_user(user)

async def question_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик вопроса с AI"""
    user_id = update.effective_user.id
    user = await get_user(user_id)

    # Получаем вопрос из аргументов
    question = " ".join(context.args) if context.args else None
    if not question:
        await update.message.reply_text(
            "❓ **Задайте вопрос**\n\n"
            "Например: `/question Что меня ждёт в любви?`",
            parse_mode='Markdown'
        )
        return

    can_proceed, remaining, limit_msg = await check_attempts(user)
    if not can_proceed:
        await update.message.reply_text(limit_msg, parse_mode='Markdown')
        return

    # Получаем карты
    cards = get_random_cards(3)
    positions = ["Прошлое", "Настоящее", "Будущее"]

    # Отправляем картинки
    media_group = []
    for i, card in enumerate(cards):
        image_path = f"images/{card['image']}"
        if os.path.exists(image_path):
            with open(image_path, "rb") as photo:
                media_group.append(InputMediaPhoto(
                    media=photo,
                    caption=f"**{positions[i]}**\n{card['name']}" if i == 0 else None,
                    parse_mode='Markdown'
                ))

    if media_group:
        await update.message.reply_media_group(media=media_group)

    # Отправляем статус "печатает"
    await update.message.chat.send_action(action="typing")

    # Получаем AI-толкование
    interpretation = await get_ai_interpretation(
        user_name=update.effective_user.first_name,
        question=question,
        cards_data=cards
    )

    if interpretation:
        await update.message.reply_text(f"🔮 **Толкование:**\n\n{interpretation}")
    else:
        # Если AI недоступен, используем стандартные значения
        response = f"🔮 **Расклад на вопрос:** '{question}'\n\n"
        for i, card in enumerate(cards):
            response += f"**{positions[i]}**: {card['name']} — {card['meaning']}\n\n"
        await update.message.reply_text(response)

    # Обновляем счётчики
    if not user.subscription_active:
        user.attempts_used += 1
    user.total_readings += 1
    await update_user(user)
