import json
import os
import logging

class KeywordProcessor:
    def __init__(self):
        self.keywords = {}
        self.logger = logging.getLogger('keyword_processor')
        self._load_keywords()  # Автоматическая загрузка при инициализации
        
    def _load_keywords(self):
        """Загружает ключевые слова из JSON-файла с обработкой ошибок"""
        try:
            file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'keywords.json')
            with open(file_path, 'r', encoding='utf-8') as f:
                self.keywords = json.load(f)
            self.logger.info(f"Успешно загружено {len(self.keywords)} ключевых слов")
        except FileNotFoundError:
            self.logger.error("Файл keywords.json не найден")
        except json.JSONDecodeError as e:
            self.logger.error(f"Ошибка формата JSON: {str(e)}")
        except Exception as e:
            self.logger.error(f"Ошибка загрузки ключевых слов: {str(e)}")
            
    def extract_keywords(self, message):
        """Извлекает все ключевые слова из сообщения"""
        found_keywords = []
        for keyword in self.keywords:
            if keyword in message:
                found_keywords.append(keyword)
        return found_keywords