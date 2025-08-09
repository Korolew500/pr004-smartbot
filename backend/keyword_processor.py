import os
import logging
from collections import defaultdict
from typing import List, Dict

# Инициализация логгера
logger = logging.getLogger(__name__)

class KeywordProcessor:
    def __init__(self):
        self.keywords = self.load_keywords()
        self.synonyms = self.load_synonyms()
        self.prioritizer = ResponsePrioritizer()

    def load_keywords(self) -> Dict[str, Dict]:
        # ... существующая реализация ...

    def load_synonyms(self) -> Dict[str, str]:
        # ... существующая реализация ...

    def process_message(self, message: str) -> List[Dict]:
        """Обрабатывает сообщение и возвращает ответы с приоритетом"""
        responses = []
        
        # Обработка ключевых слов и синонимов
        # ... существующая логика ...
        
        # Сортировка по приоритету
        return self.prioritizer.sort_responses(responses)


class ResponsePrioritizer:
    PRIORITY_ORDER = ["greeting", "product", "payment", "delivery"]
    
    def sort_responses(self, responses: List[Dict]) -> List[Dict]:
        """Сортирует ответы по заданному приоритету"""
        if not responses:
            return []
            
        # Группировка по типам
        type_groups = defaultdict(list)
        for response in responses:
            response_type = response.get("type", "other")
            type_groups[response_type].append(response)
        
        # Сортировка по приоритету
        sorted_responses = []
        for p_type in self.PRIORITY_ORDER:
            if p_type in type_groups:
                sorted_responses.extend(type_groups[p_type])
        
        # Добавление неподдерживаемых типов в конец
        for r_type, group in type_groups.items():
            if r_type not in self.PRIORITY_ORDER:
                sorted_responses.extend(group)
                
        return sorted_responses