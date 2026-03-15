import random
from data.cards_data import cards

def get_random_card():
    """Получить случайную карту"""
    card_id = random.choice(list(cards.keys()))
    return cards[card_id]

def get_random_cards(count: int):
    """Получить несколько случайных карт"""
    card_ids = random.sample(list(cards.keys()), min(count, len(cards)))
    return [cards[card_id] for card_id in card_ids]

def format_card_message(card, position=None):
    """Форматировать сообщение с картой"""
    text = f"**{card['name']}**"
    if position:
        text = f"**{position}**\n{text}"

    text += f"\n\n_{card['meaning']}_"

    if 'description' in card:
        text += f"\n\n{card['description']}"

    return text, card['image']
