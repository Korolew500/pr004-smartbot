"""Основной модуль backend"""

from .keyword_processor import KeywordProcessor
from .synonym_mapper import SynonymMapper
from .spell_checker import SpellChecker  # Добавлен импорт

class Backend:
    def __init__(self):
        self.keyword_processor = KeywordProcessor()
        self.synonym_mapper = SynonymMapper()
        self.spell_checker = SpellChecker()  # Инициализация
        self.active_modules = {
            'spell_check': True,
            'synonym_mapping': True,
            'keyword_processing': True
        }

    def process_message(self, message):
        """Обработка входящего сообщения"""
        # Коррекция орфографии
        if self.active_modules['spell_check']:
            message = self.spell_checker.correct_text(message)
            
        # Обработка синонимов
        if self.active_modules['synonym_mapping']:
            words = message.split()
            mapped_words = [self.synonym_mapper.map_to_base(word) for word in words]
            message = " ".join(mapped_words)
        
        # Обработка ключевых слов
        if self.active_modules['keyword_processing']:
            responses = self.keyword_processor.process(message)
            return self._select_best_response(responses)
        
        return "Команда обработана"
    
    def _select_best_response(self, responses):
        """Выбирает лучший ответ (пока просто первый)"""
        return responses[0] if responses else "Не понимаю запрос"