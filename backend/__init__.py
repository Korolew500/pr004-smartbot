"""Backend модуль для обработки сообщений"""

# Импорт основных компонентов
from .main import Backend
from .spell_checker import check_spelling
from .keyword_processor import KeywordProcessor

__all__ = ['Backend', 'check_spelling', 'KeywordProcessor']  # Явное указание экспортируемых объектов