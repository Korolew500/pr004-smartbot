"""Основной модуль backend"""

from .keyword_processor import KeywordProcessor
from .synonym_mapper import SynonymMapper

class Backend:
    def __init__(self):
        self.keyword_processor = KeywordProcessor()
        self.synonym_mapper = SynonymMapper()
        self.active_modules = {
            'spell_check': True,
            'synonym_mapping': True,
            'keyword_processing': True
        }

    def process_message(self, message):
        """Обработка входящего сообщения"""
        # ... существующая предобработка ...
        
        if self.active_modules['keyword_processing']:
            responses = self.keyword_processor.process(message)
            return self._select_best_response(responses)  # <-- NEW
        
        return "Команда обработана"
    
    def _select_best_response(self, responses):
        """Выбирает лучший ответ (пока просто первый)"""
        return responses[0] if responses else "Не понимаю запрос"