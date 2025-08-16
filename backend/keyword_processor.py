import re
from .data_manager import DataManager

class KeywordProcessor:
    def __init__(self, data_dir='data'):
        self.keyword_data = {}
        self.data_manager = DataManager(data_dir)
        self._load_keywords()

    def _load_keywords(self):
        """Загружает ключевые слова из файла"""
        self.keyword_data = self.data_manager.load_data("keywords") or {}

    def extract_keywords(self, text):
        """Извлекает ключевые слова из текста с учётом словоформ"""
        text_lower = text.lower()
        tokens = set(re.findall(r'\w+', text_lower))
        return [k for k in self.keyword_data if any(word in k.lower() for word in tokens)]

    def process(self, text, max_responses=None):
        """Возвращает все подходящие ответы с метаданными"""
        keywords = self.extract_keywords(text)
        return [self.keyword_data[k] for k in keywords]
    
    def add_keyword(self, keyword, response, ktype="общий"):
        """Добавляет новое ключевое слово"""
        self.keyword_data[keyword] = {
            "type": ktype,
            "response": response,
            "context": "общий"
        }
        self.data_manager.save_data("keywords", self.keyword_data)
        
    def remove_keyword(self, keyword):
        """Удаляет ключевое слово"""
        if keyword in self.keyword_data:
            del self.keyword_data[keyword]
            self.data_manager.save_data("keywords", self.keyword_data)