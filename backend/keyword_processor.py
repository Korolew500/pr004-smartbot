import json
import os
import logging

class KeywordProcessor:
    def __init__(self):
        self.keywords = {}
        self.logger = logging.getLogger('keyword_processor')
        self._load_keywords()
        
    def _load_keywords(self):
        try:
            file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'keywords.json')
            with open(file_path, 'r', encoding='utf-8') as f:
                self.keywords = json.load(f)
            self.logger.info(f"Загружено {len(self.keywords)} ключевых слов")
        
            # Сортировка по длине фразы (длинные - в первую очередь)
            self.sorted_keywords = sorted(
                self.keywords.keys(), 
                key=len, 
                reverse=True
            )
        except Exception as e:
            self.logger.error(f"Ошибка загрузки ключевых слов: {str(e)}")
            
    def extract_keywords(self, message):
        found_keywords = []
        
        # Поиск сначала длинных фраз, потом коротких
        for keyword in self.sorted_keywords:
            if keyword in message:
                found_keywords.append(keyword)
                # Удаляем найденную фразу из сообщения
                message = message.replace(keyword, "", 1)
                
        return found_keywords