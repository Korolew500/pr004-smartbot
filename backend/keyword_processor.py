import re
from collections import OrderedDict

class KeywordProcessor:
    def __init__(self):
        self.keywords = {}
        self._keyword_trie_dict = {}

    def add_keyword(self, keyword, response):
        self.keywords[keyword] = response
        current_dict = self._keyword_trie_dict
        for char in keyword:
            current_dict = current_dict.setdefault(char, {})
        current_dict['__kw__'] = keyword

    def extract_keywords(self, text):
        """Извлекает ключевые слова с приоритетом длинных фраз"""
        found_keywords = OrderedDict()
        text_lower = text.lower()
        
        # Поиск самых длинных совпадений
        for i in range(len(text_lower)):
            current_dict = self._keyword_trie_dict
            for j in range(i, len(text_lower)):
                char = text_lower[j]
                if char not in current_dict:
                    break
                
                current_dict = current_dict[char]
                if '__kw__' in current_dict:
                    keyword = current_dict['__kw__']
                    # Перезаписываем более короткие вхождения
                    found_keywords[keyword] = self.keywords[keyword]
                    
                    # Пропускаем символы найденного ключевого слова
                    i = j
                    break
        
        return list(found_keywords.keys())

    def get_response(self, keyword):
        """Возвращает ответ для ключевого слова"""
        return self.keywords.get(keyword, None)