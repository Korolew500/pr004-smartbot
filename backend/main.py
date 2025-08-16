import random
import json
import re
from .keyword_processor import KeywordProcessor
from .spell_checker import SpellChecker

class Backend:
    def __init__(self):
        self.keyword_processor = KeywordProcessor()
        self.spell_checker = SpellChecker()
        self.default_response = "Извините, я не понял вопрос. Можете переформулировать?"
        self.load_keywords()

    def load_keywords(self):
        with open('data/keywords.json', 'r', encoding='utf-8') as f:
            keywords_data = json.load(f)
            
        for keyword, data in keywords_data.items():
            # Обработка синонимов
            synonyms = data.get('synonyms', [])
            all_keys = [keyword] + synonyms
            
            for key in all_keys:
                self.keyword_processor.add_keyword(
                    key.lower(), 
                    data.get('responses', data.get('response', ''))
                )

    def process_message(self, message):
        # Очистка и нормализация
        clean_msg = re.sub(r'[^\w\s]', '', message).strip()
        
        # Проверка орфографии
        corrected = self.spell_checker.correct_text(clean_msg)
        
        # Извлечение ключевых слов
        keywords = self.keyword_processor.extract_keywords(corrected.lower())
        
        # Формирование ответа
        responses = []
        seen_responses = set()
        
        for keyword in keywords:
            response = self.keyword_processor.get_response(keyword)
            
            if isinstance(response, list):
                response = random.choice(response)
            
            # Убираем дубликаты
            if response not in seen_responses:
                responses.append(response)
                seen_responses.add(response)
        
        if responses:
            return ". ".join(responses)
        
        return self.default_response