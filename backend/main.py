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
        self.data_refresh_time = {}  # Трекер времени изменения данных

    def check_data_updates(self):
        """Проверяет обновления файлов данных"""
        data_files = {
            "keywords": "data/keywords.json",
            "synonyms": "data/synonyms.json"
        }
        
        for data_type, file_path in data_files.items():
            mod_time = os.path.getmtime(file_path)
            
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
            return self._select_best_response(responses)
        
        return "Пожалуйста, уточните ваш вопрос"
    
    # ... остальной код без изменений ...