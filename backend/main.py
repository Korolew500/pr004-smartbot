import os
import logging
from .keyword_processor import KeywordProcessor
from .spell_checker import SpellChecker
from .synonym_mapper import SynonymMapper

class Backend:
    def __init__(self):
        self.keyword_processor = KeywordProcessor()
        self.spell_checker = SpellChecker()
        self.synonym_mapper = SynonymMapper()
        self.logger = logging.getLogger('backend')

    def process_message(self, message):
        try:
            # Логирование исходного сообщения
            self.logger.info(f"Обработка сообщения: {message}")
            
            # Коррекция орфографии
            corrected = self.spell_checker.correct_text(message)
            if corrected != message:
                self.logger.info(f"Исправлено: '{message}' -> '{corrected}'")
            
            # Поиск синонимов (ИСПРАВЛЕНО: map_to_base вместо map_synonyms)
            normalized = self.synonym_mapper.map_to_base(corrected)
            
            # Обработка ключевых слов
            responses = self.keyword_processor.process(normalized)
            
            # Формирование ответа
            if responses:
                return self._select_response(responses)
            else:
                return "Извините, я не понял вопрос. Можете переформулировать?"
                
        except Exception as e:
            self.logger.error(f"Ошибка обработки: {str(e)}", exc_info=True)
            return "Произошла внутренняя ошибка. Пожалуйста, повторите позже."

    def _select_response(self, responses):
        # Логика выбора лучшего ответа
        return responses[0]['responses'][0]