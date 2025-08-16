import json
import os
import logging

class KeywordProcessor:
    def __init__(self):
        self.keywords = {}
        self.logger = logging.getLogger('keyword_processor')
        
    def _load_keywords(self):
        """Загружает ключевые слова из JSON-файла с обработкой ошибок"""
        try:
            file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'keywords.json')
            with open(file_path, 'r', encoding='utf-8') as f:
                self.keywords = json.load(f)
        except FileNotFoundError:
            self.logger.error("Файл keywords.json не найден")
        except json.JSONDecodeError as e:
            self.logger.error(f"Ошибка формата JSON: {str(e)}")
        except Exception as e:
            self.logger.error(f"Ошибка загрузки ключевых слов: {str(e)}")
            
    def process(self, message):
        """Обрабатывает сообщение и возвращает подходящие ответы"""
        found_responses = []
        
        for keyword, data in self.keywords.items():
            if keyword in message:
                # Поддержка старого и нового формата
                response_data = {
                    "type": data.get("type", "общий"),
                    "response": data.get("response", ""),
                    "responses": data.get("responses", [])
                }
                if not response_data["responses"] and response_data["response"]:
                    response_data["responses"] = [response_data["response"]]
                found_responses.append(response_data)
        
        return found_responses

    def add_keyword(self, keyword, response, ktype="общий"):
        """Добавляет новое ключевое слово"""
        self.keywords[keyword] = {
            "type": ktype,
            "response": response,
            "responses": [response]
        }
        self._save_keywords()
        return True
        
    def remove_keyword(self, keyword):
        """Удаляет ключевое слово"""
        if keyword in self.keywords:
            del self.keywords[keyword]
            self._save_keywords()
            return True
        return False
        
    def _save_keywords(self):
        """Сохраняет ключевые слова в JSON-файл"""
        try:
            file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'keywords.json')
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.keywords, f, ensure_ascii=False, indent=2)
        except Exception as e:
            self.logger.error(f"Ошибка сохранения ключевых слов: {str(e)}")