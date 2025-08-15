"""Основной модуль backend"""

from .keyword_processor import KeywordProcessor
from .synonym_mapper import SynonymMapper
from .spell_checker import SpellChecker

class Backend:
    def __init__(self):
        self.keyword_processor = KeywordProcessor()
        self.synonym_mapper = SynonymMapper()
        self.spell_checker = SpellChecker()
        self.active_modules = {
            'spell_check': True,
            'synonym_mapping': True,
            'keyword_processing': True
        }
        self.response_priority = {
            "приветствие": 10,
            "прощание": 10,
            "вопрос": 7,
            "продукт": 5,
            "техподдержка": 8
        }

    def process_message(self, message):
        """Обработка входящего сообщения"""
        if self.active_modules['spell_check']:
            message = self.spell_checker.correct_text(message)
            
        if self.active_modules['synonym_mapping']:
            words = message.split()
            mapped_words = [self.synonym_mapper.map_to_base(word) for word in words]
            message = " ".join(mapped_words)
        
        if self.active_modules['keyword_processing']:
            responses = self.keyword_processor.process(message)
            return self._select_best_response(responses)
        
        return "Пожалуйста, уточните ваш вопрос"
    
    def _select_best_response(self, responses):
        """Выбирает лучший ответ на основе приоритетов"""
        if not responses:
            return "Не понимаю запрос"
            
        # Сортируем ответы по приоритету
        sorted_responses = sorted(
            responses,
            key=lambda r: self.response_priority.get(
                r.get("type", "общий"), 
                3
            ),
            reverse=True
        )
        return sorted_responses[0]["response"]

    def toggle_module(self, module_name, state):
        """Включает/выключает модули обработки"""
        if module_name in self.active_modules:
            self.active_modules[module_name] = state
            return True
        return False
        
    def add_keyword(self, keyword, response, ktype="общий"):
        """Добавляет ключевое слово"""
        return self.keyword_processor.add_keyword(keyword, response, ktype)
        
    def remove_keyword(self, keyword):
        """Удаляет ключевое слово"""
        return self.keyword_processor.remove_keyword(keyword)
        
    def add_synonym(self, base_word, synonym):
        """Добавляет синоним"""
        return self.synonym_mapper.add_synonym(base_word, synonym)
        
    def remove_synonym(self, base_word, synonym):
        """Удаляет синоним"""
        return self.synonym_mapper.remove_synonym(base_word, synonym)