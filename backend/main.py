"""Основimport random
ной модуль backend"""

import os
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
        self.data_refresh_time = {}  # Трекер времени изменения данных

    def check_data_updates(self):
        """Проверяет обновления файлов данных"""
        data_files = {
            "keywords": "data/keywords.json",
            "synonyms": "data/synonyms.json"
        }
        
        for data_type, file_path in data_files.items():
            full_path = os.path.join(os.path.dirname(__file__), '..', file_path)
            abs_path = os.path.abspath(full_path)
            
            if not os.path.exists(abs_path):
                continue
                
            mod_time = os.path.getmtime(abs_path)
            
            if data_type not in self.data_refresh_time or mod_time > self.data_refresh_time[data_type]:
                self.data_refresh_time[data_type] = mod_time
                
                if data_type == "keywords":
                    self.keyword_processor._load_keywords()
                elif data_type == "synonyms":
                    self.synonym_mapper._load_synonyms()
                print(f"Обновлены данные: {data_type}")

    def process_message(self, message):
        """Обработка входящего сообщения"""
        self.check_data_updates()  # Проверка обновлений перед обработкой
        
        if self.active_modules['spell_check']:
            message = self.spell_checker.correct_text(message)
            
        if self.active_modules['synonym_mapping']:
            words = message.split()
            mapped_words = [self.synonym_mapper.map_to_base(word) for word in words]
            message = " ".join(mapped_words)
        
        if self.active_modules['keyword_processing']:
            responses = self.keyword_processor.process(message)
            response = self._select_best_response(responses)
return self._enhance_response(response)
        
        return "Пожалуйста, уточните ваш вопрос"
    
    def _select_best_response(self, responses):
        """Выбирает ответ с наивысшим приоритетом"""
        if not responses:
            return "Не понимаю запрос"
            
        # Находим ответ с максимальным приоритетом
        best_response = max(
            responses, 
            key=lambda r: self.response_priority.get(r.get("type", "общий"), 0)
        )
        # Добавляем вариативность ответов
responses = best_response.get("responses", [best_response["response"]])
return random.choice(responses) if responses else "Не понимаю запрос"

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
    def _enhance_response(self, response):
        """Добавляет естественность в ответы"""
        enhancers = {
            "приветствие": ["Как ваши дела?", "Чем могу помочь?"],
            "прощание": ["Хорошего дня!", "До новых встреч!"],
            "вопрос": ["Могу уточнить детали.", "Это важный вопрос."]
        }
        
        if random.random() > 0.7:  # 30% chance
            return f"{response} {random.choice(enhancers.get('general', ['']))}"
        return response