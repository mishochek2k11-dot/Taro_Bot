import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

async def get_ai_interpretation(user_name, question, cards_data):
    """Получить толкование от Gemini AI"""
    try:
        # Описываем расклад
        cards_description = ""
        positions = ["Прошлое", "Настоящее", "Будущее"]
        for i, card in enumerate(cards_data):
            position = positions[i] if len(cards_data) == 3 else f"Карта {i+1}"
            cards_description += f"\n{position}: {card['name']} — {card['meaning']}"

        prompt = f"""Ты — опытный таролог с 20-летним стажем. Твои толкования добрые, поддерживающие, но честные. Используй символизм карт Таро.

Имя пользователя: {user_name}
Вопрос: {question if question else 'Общий прогноз'}

Выпали карты:{cards_description}

Дай подробное, персонализированное толкование этого расклада. Отвечай на том же языке, на котором задан вопрос.
"""
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"AI Error: {e}")
        return None
