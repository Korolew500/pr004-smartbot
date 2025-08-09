import re
import pymorphy2
from collections import defaultdict

class KeywordProcessor:
    def __init__(self, keywords_path='data/keywords.txt'):
        self.keyword_tree = defaultdict(dict)
        self.keyword_responses = {}
        self.keywords_path = keywords_path
        self.morph = pymorphy2.MorphAnalyzer()
        self._load_keywords()

    def _load_keywords(self):
        try:
            with open(self.keywords_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    
                    parts = [p.strip() for p in line.split('|')]
                    if len(parts) < 3:
                        continue
                        
                    keyword = parts[0]
                    response = parts[2]
                    
                    # Нормализация ключевых слов
                    base_form = self._get_base_form(keyword)
                    self.keyword_responses[base_form] = response
                    self._add_keyword(base_form)
        except FileNotFoundError:
            print(f"Warning: {self.keywords_path} not found")

    def _add_keyword(self, keyword):
        current = self.keyword_tree
        for char in keyword:
            current = current.setdefault(char, {})
        current['__end__'] = True

    def _get_base_form(self, word):
        """Приводит слово к нормальной форме"""
        parsed = self.morph.parse(word)
        return parsed[0].normal_form if parsed else word

    def process(self, text):
        """Обрабатывает текст и возвращает ответ"""
        keywords = self.extract_keywords(text)
        
        if keywords:
            # Возвращаем ответ для первого найденного ключевого слова
            return self.keyword_responses.get(keywords[0], 
                   "Не понимаю ваш запрос. Попробуйте переформулировать.")
        
        return "Не понимаю ваш запрос. Попробуйте переформулировать."

    def extract_keywords(self, text):
        """Извлекает ключевые слова из текста с учётом морфологии"""
        results = []
        current = self.keyword_tree
        start_index = 0
        
        # Обработка текста по словам
        words = re.findall(r'\w+', text.lower())
        normalized_text = ' '.join([self._get_base_form(word) for word in words])
        
        for i, char in enumerate(normalized_text):
            if char in current:
                current = current[char]
                if '__end__' in current:
                    keyword = normalized_text[start_index:i+1]
                    if keyword in self.keyword_responses:
                        results.append(keyword)
                    current = self.keyword_tree
                    start_index = i+1
            else:
                current = self.keyword_tree
                start_index = i+1
        
        return results