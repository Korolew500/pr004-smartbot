import os
import logging
from collections import defaultdict

class KeywordProcessor:
    def __init__(self):
        self.keywords = self.load_keywords()
        self.synonym_map, self.base_to_synonyms = self.load_synonyms()
        self.prioritizer = ResponsePrioritizer()

    def load_keywords(self):
        return {
            "привет": {"type": "greeting", "response": "Здравствуйте! Чем могу помочь?"},
            "пока": {"type": "farewell", "response": "До свидания! Обращайтесь ещё!"},
            "цена": {"type": "product", "response": "Цены начинаются от 1000 рублей."},
            "оплата": {"type": "payment", "response": "Мы принимаем карты и электронные кошельки."},
            "доставка": {"type": "delivery", "response": "Доставка занимает 1-3 рабочих дня."}
        }

    def load_synonyms(self):
        synonym_map = {
            "прив": "привет",
            "здравствуй": "привет",
            "добрый день": "привет",
            "прощайте": "пока",
            "до свидания": "пока",
            "стоимость": "цена",
            "оплатить": "оплата",
            "доставить": "доставка"
        }
        
        # Создаем обратное отображение
        base_to_synonyms = defaultdict(list)
        for synonym, base in synonym_map.items():
            base_to_synonyms[base].append(synonym)
            
        return synonym_map, dict(base_to_synonyms)

    def process(self, message: str) -> str:
        responses = self.find_responses(message)
        sorted_responses = self.prioritizer.sort_responses(responses)
        return sorted_responses[0]["response"] if sorted_responses else "Не понимаю ваш запрос. Попробуйте переформулировать."

    def find_responses(self, message: str) -> list:
        """Находит все подходящие ответы в сообщении"""
        responses = []
        words = message.lower().split()
        
        # Проверка словосочетаний (2-3 слова)
        for i in range(len(words)-1):
            phrase = " ".join(words[i:i+2])
            if phrase in self.synonym_map:
                base = self.synonym_map[phrase]
                responses.append(self.keywords[base])
        
        # Проверка отдельных слов
        for word in words:
            if word in self.synonym_map:
                base = self.synonym_map[word]
                responses.append(self.keywords[base])
            elif word in self.keywords:
                responses.append(self.keywords[word])
        
        return responses

class ResponsePrioritizer:
    PRIORITY_ORDER = ["greeting", "product", "payment", "delivery", "farewell"]
    
    def sort_responses(self, responses):
        if not responses: return []
        
        type_groups = defaultdict(list)
        for response in responses:
            response_type = response.get("type", "other")
            type_groups[response_type].append(response)
        
        sorted_responses = []
        for p_type in self.PRIORITY_ORDER:
            if p_type in type_groups:
                sorted_responses.extend(type_groups[p_type])
        
        for r_type, group in type_groups.items():
            if r_type not in self.PRIORITY_ORDER:
                sorted_responses.extend(group)
                
        return sorted_responses