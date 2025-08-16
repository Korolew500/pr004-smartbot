import re
import random
from .data_manager import DataManager
from .keyword_processor import KeywordProcessor
from .spell_checker import SpellChecker
from .synonym_mapper import SynonymMapper

class Backend:
    def __init__(self):
        self.data_manager = DataManager()
        self.keyword_processor = KeywordProcessor()
        self.spell_checker = SpellChecker()
        self.synonym_mapper = SynonymMapper()
        self.load_data()

    def load_data(self):
        """Загрузка всех необходимых данных"""
        self.keyword_processor.load_keywords(self.data_manager.load_keywords())
        self.spell_checker.load_dictionary('data/dictionary.txt')
        self.synonym_mapper.load_synonyms(self.data_manager.load_synonyms())
        
    def process_message(self, message: str) -> str:
        # Очистка от пунктуации
        clean_msg = re.sub(r'[^\w\s]', '', message)
        
        # Коррекция орфографии
        corrected = self.spell_checker.correct_text(clean_msg)
        
        # Приведение к базовой форме
        base_form = self.synonym_mapper.map_to_base(corrected)
        
        # Поиск ключевых слов
        keywords = self.keyword_processor.extract_keywords(base_form)
        
        if not keywords:
            return "Извините, я не понял вопрос. Можете переформулировать?"
        
        # Сбор ответов для всех найденных ключевых слов
        responses = []
        for keyword in keywords:
            response = self.keyword_processor.get_response(keyword)
            if response:
                responses.append(response)
        
        # Составной ответ из всех найденных ответов
        return ' '.join(responses)