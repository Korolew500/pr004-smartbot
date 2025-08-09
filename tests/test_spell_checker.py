"""Тесты для модуля проверки орфографии"""

import unittest
from backend.spell_checker import check_spelling

class TestSpellChecker(unittest.TestCase):
    def test_basic_correction(self):
        """Тест базовой коррекции"""
        # Проверка исправления падежей
        self.assertEqual(check_spelling("приветсвую"), "приветствовать")
        self.assertEqual(check_spelling("делайт"), "делать")
        
        # Проверка сохранения правильных слов
        self.assertEqual(check_spelling("здравствуйте как дела"), "здравствуйте как делать")
        
    def test_short_words(self):
        """Тест обработки коротких слов"""
        self.assertEqual(check_spelling("я и ты"), "я и ты")
        self.assertEqual(check_spelling("в на под"), "в на под")
        
    def test_special_cases(self):
        """Тест специальных случаев"""
        # Слова с дефисом
        self.assertEqual(check_spelling("интернет-магазин"), "интернет-магазин")
        
        # Английские слова
        self.assertEqual(check_spelling("hello world"), "hello world")

if __name__ == "__main__":
    unittest.main()