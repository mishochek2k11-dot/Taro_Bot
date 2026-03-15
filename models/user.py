from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

@dataclass
class User:
    user_id: int
    username: str = ""
    first_name: str = ""
    registered_at: str = ""
    attempts_used: int = 0
    last_attempt_reset: str = ""
    subscription_active: bool = False
    subscription_until: str = ""
    total_readings: int = 0
    payments: List[dict] = None

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "first_name": self.first_name,
            "registered_at": self.registered_at,
            "attempts_used": self.attempts_used,
            "last_attempt_reset": self.last_attempt_reset,
            "subscription_active": self.subscription_active,
            "subscription_until": self.subscription_until,
            "total_readings": self.total_readings,
            "payments": self.payments or []
        }
