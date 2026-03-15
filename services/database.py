import json
import aiofiles
from datetime import datetime
from models.user import User

DB_PATH = "data/users.json"

async def get_user(user_id: int) -> User:
    """Получить пользователя из БД или создать нового"""
    try:
        async with aiofiles.open(DB_PATH, "r") as f:
            data = json.loads(await f.read())
    except FileNotFoundError:
        data = {}

    if str(user_id) not in data:
        # Новый пользователь
        now = datetime.now().isoformat()
        user = User(
            user_id=user_id,
            registered_at=now,
            last_attempt_reset=now.split("T")[0]  # Только дата
        )
        data[str(user_id)] = user.to_dict()
        await save_db(data)
        return user

    user_data = data[str(user_id)]
    return User(**user_data)

async def save_db(data):
    """Сохранить БД в файл"""
    async with aiofiles.open(DB_PATH, "w") as f:
        await f.write(json.dumps(data, indent=2, ensure_ascii=False))

async def update_user(user: User):
    """Обновить данные пользователя"""
    data = await load_db()
    data[str(user.user_id)] = user.to_dict()
    await save_db(data)

async def check_attempts(user: User) -> tuple[bool, int]:
    """Проверить, может ли пользователь сделать расклад
    Возвращает (можно_ли_делать, осталось_попыток)
    """
    # Проверка подписки
    if user.subscription_active:
        # Проверить, не истекла ли подписка
        if user.subscription_until:
            until = datetime.fromisoformat(user.subscription_until)
            if datetime.now() < until:
                return True, -1  # -1 означает безлимит
            else:
                # Подписка истекла
                user.subscription_active = False
                await update_user(user)

    # Проверка даты последнего сброса
    today = datetime.now().strftime("%Y-%m-%d")
    if user.last_attempt_reset != today:
        user.attempts_used = 0
        user.last_attempt_reset = today
        await update_user(user)

    remaining = FREE_ATTEMPTS_PER_DAY - user.attempts_used
    return remaining > 0, remaining
