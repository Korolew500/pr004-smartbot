class KeywordProcessor:
    def __init__(self):
        self.keywords = {}

    def load_keywords(self, keywords_data):
        """Загрузка ключевых слов из JSON"""
        self.keywords = keywords_data

    def extract_keywords(self, text: str) -> list:
        """Извлечение ключевых слов с учётом приоритета длинных фраз"""
        found = []
        words = text.split()
        
        # Поиск от самых длинных фраз к коротким
        for length in range(4, 0, -1):
            for i in range(len(words) - length + 1):
                phrase = ' '.join(words[i:i+length])
                if phrase in self.keywords:
                    found.append(phrase)
                    # Пропускаем слова, вошедшие в фразу
                    words[i:i+length] = [''] * length
        
        return found

    def get_response(self, keyword):
        """Получение ответа для ключевого слова"""
        if keyword not in self.keywords:
            return None
            
        data = self.keywords[keyword]
        
        if 'responses' in data:
            return random.choice(data['responses'])
        elif 'response' in data:
            return data['response']
        
        return None