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
        # Проверка орфографии
        if self.active_modules['spell_check']:
            from .spell_checker import SpellChecker
            checker = SpellChecker()
            message = checker.correct_text(message)
            
        # Преобразование синонимов
        if self.active_modules['synonym_mapping']:
            words = message.split()
            mapped_words = [self.synonym_mapper.map_to_base(word) for word in words]
            message = ' '.join(mapped_words)
            
        # Обработка ключевых слов
        if self.active_modules['keyword_processing']:
            return self.keyword_processor.process(message)
        
        return "Команда обработана"