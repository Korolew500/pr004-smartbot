"""Обновленные тесты для backend модуля"""

import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.keyword_processor import KeywordProcessor

class TestBackend(unittest.TestCase):
    def setUp(self):
        self.processor = KeywordProcessor()

    def test_keyword_processing(self):
        self.assertEqual(
            self.processor.process("привет"),
            "Здравствуйте! Чем могу помочь?"
        )
        self.assertEqual(
            self.processor.process("пока"),
            "До свидания! Обращайтесь ещё!"
        )

    def test_unknown_input(self):
        self.assertEqual(
            self.processor.process("случайный текст"),
            "Не понимаю ваш запрос. Попробуйте переформулировать."
        )

    def test_synonym_processing(self):
        # Проверка однословных синонимов
        for synonym in ["здравствуй", "прив"]:
            self.assertEqual(
                self.processor.process(synonym),
                "Здравствуйте! Чем могу помочь?"
            )
        
        # Проверка многословных синонимов
        self.assertEqual(
            self.processor.process("добрый день"),
            "Здравствуйте! Чем могу помочь?"
        )
        
        # Проверка синонимов прощания
        for synonym in ["до свидания", "прощайте"]:
            self.assertEqual(
                self.processor.process(synonym),
                "До свидания! Обращайтесь ещё!"
            )

if __name__ == "__main__":
    unittest.main()