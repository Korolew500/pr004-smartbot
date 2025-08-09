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
        """Временная заглушка для загрузки ключевых слов"""
        return {
            "привет": {"type": "greeting", "response": "Здравствуйте! Чем могу помочь?"},
            "цена": {"type": "product", "response": "Цены начинаются от 1000 рублей."},
            "оплата": {"type": "payment", "response": "Мы принимаем карты и электронные кошельки."},
            "доставка": {"type": "delivery", "response": "Доставка занимает 1-3 рабочих дня."}
        }

    def load_synonyms(self) -> Dict[str, str]:
        """Временная заглушка для загрузки синонимов"""
        return {
            "прив": "привет",
            "здравствуй": "привет",
            "стоимость": "цена",
            "оплатить": "оплата",
            "доставить": "доставка"
        }

    def process_message(self, message: str) -> List[Dict]:
        """Обрабатывает сообщение и возвращает ответы с приоритетом"""
        responses = []
        words = message.split()
        
        for word in words:
            # Проверяем синонимы
            base_word = self.synonyms.get(word.lower(), word.lower())
            
            # Ищем ключевое слово
            if base_word in self.keywords:
                responses.append(self.keywords[base_word])
        
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