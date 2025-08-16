"""Frontend модуль для взаимодействия с пользователем"""

# Импорт основных компонентов
from .main import Frontend
from .console import ConsoleInterface
from .tele import TelegramInterface

__all__ = ['Frontend', 'ConsoleInterface', 'TelegramInterface']