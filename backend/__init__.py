"""Backend модуль для обработки сообщений"""

# Импорт основных компонентов
from .main import Backend
from .spell_checker import SpellChecker
from .keyword_processor import KeywordProcessor
from .synonym_mapper import SynonymMapper

__all__ = ['Backend', 'SpellChecker', 'KeywordProcessor', 'SynonymMapper']