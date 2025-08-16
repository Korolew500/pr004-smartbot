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
        # Исправление орфографии
        corrected = self.spell_checker.correct_text(message)
        
        # Нормализация текста (приведение к базовой форме)
        normalized = self.normalize_text(corrected)
        
        # Извлечение ВСЕХ ключевых слов
        keywords = self.keyword_processor.extract_keywords(normalized)
        
        # Сбор ВСЕХ ответов
        responses = []
        for keyword in keywords:
            if keyword in self.keyword_processor.keywords:
                data = self.keyword_processor.keywords[keyword]
                # Поддержка старого (response) и нового формата (responses)
                if 'responses' in data:
                    responses.extend(data['responses'])
                elif 'response' in data:
                    responses.append(data['response'])
        
        # Формирование составного ответа
        if responses:
            return " ".join(responses)
        else:
            return "Извините, я не понял вопрос. Можете переформулировать?"
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
        priority_order = ['приветствие', 'прощание', 'продукт', 'информация']
        for p in priority_order:
            for r in responses:
                if r.get('type') == p:
                    if 'responses' in r:
                        return r['responses'][0]
                    return r['response']
        # Fallback to first response
        if 'responses' in responses[0]:
            return responses[0]['responses'][0]
        return responses[0]['response']