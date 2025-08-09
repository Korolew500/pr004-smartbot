"""Тесты для backend модуля"""

import unittest
import os
import sys

# Добавляем путь к модулям проекта
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.keyword_processor import KeywordProcessor

class TestBackend(unittest.TestCase):
    def setUp(self):
        self.processor = KeywordProcessor()

    def test_keyword_processing(self):
        """Тест обработки ключевых слов"""
        response = self.processor.process("привет")
        self.assertEqual(response, "Здравствуйте! Чем могу помочь?")
        
        response = self.processor.process("пока")
        self.assertEqual(response, "До свидания! Обращайтесь ещё!")

    def test_unknown_input(self):
        """Тест обработки неизвестного ввода"""
        response = self.processor.process("случайный текст")
        self.assertEqual(response, "Не понимаю ваш запрос. Попробуйте переформулировать.")

    def test_synonym_processing(self):
        """Тест обработки синонимов"""
        # Проверяем все синонимы для "привет"
        for synonym in ["здравствуйте", "добрый день", "приветик"]:
            response = self.processor.process(synonym)
            self.assertEqual(response, "Здравствуйте! Чем могу помочь?")
        
        # Проверяем все синонимы для "пока"
        for synonym in ["до свидания", "прощайте", "всего доброго"]:
            response = self.processor.process(synonym)
            self.assertEqual(response, "До свидания! Обращайтесь ещё!")

if __name__ == "__main__":
    unittest.main()