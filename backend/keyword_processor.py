import re
import pymorphy3
from collections import defaultdict
from .data_manager import DataManager

class KeywordProcessor:
    def __init__(self, data_dir='data'):
        self.keyword_tree = defaultdict(dict)
        self.keyword_responses = {}
        self.data_manager = DataManager(data_dir)
        self.morph = pymorphy3.MorphAnalyzer()
        self._load_keywords()

    def _load_keywords(self):
        """Загружает ключевые слова из файла через DataManager"""
        keywords_data = self.data_manager.load_data("keywords")
        for keyword, data in keywords_data.items():
            self.keyword_responses[keyword] = data.get("response", "")

    # ... существующий код ...

    def process(self, text, max_responses=3):
        """Возвращает несколько подходящих ответов"""
        keywords = self.extract_keywords(text)
        responses = []
        
        for keyword in keywords[:max_responses]:
            if keyword in self.keyword_responses:
                responses.append(self.keyword_responses[keyword])
        
        return responses if responses else ["Не понимаю ваш запрос"]