"""Основной модуль backend"""

from .keyword_processor import KeywordProcessor

class Backend:
    def __init__(self):
        self.keyword_processor = KeywordProcessor()
        self.active_modules = {
            'spell_check': True,  # Включаем проверку орфографии
            'keyword_processing': True
        }
        print("Backend инициализирован")

    def process_message(self, message):
        """Обработка входящего сообщения"""
        # Проверка орфографии
        if self.active_modules['spell_check']:
            from .spell_checker import check_spelling
            corrected_message = check_spelling(message)
            print(f"Исправлено: {message} -> {corrected_message}")
            message = corrected_message
        
        # Обработка ключевых слов
        if self.active_modules['keyword_processing']:
            response = self.keyword_processor.process(message)
            return response
        
        return "Команда обработана"