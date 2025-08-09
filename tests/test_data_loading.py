"""Тесты загрузки данных"""

import unittest
import os
import sys

# Добавляем путь к модулям проекта
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.keyword_processor import KeywordProcessor

class TestDataLoading(unittest.TestCase):
    def test_keywords_loading(self):
        """Тест загрузки ключевых слов"""
        processor = KeywordProcessor()
        self.assertIn("привет", processor.keywords)
        self.assertIn("оплата", processor.keywords)
        self.assertEqual(processor.keywords["привет"]["response"], "Здравствуйте! Чем могу помочь?")

    def test_synonyms_loading(self):
        """Тест загрузки синонимов"""
        processor = KeywordProcessor()
        self.assertIn("привет", processor.synonyms)
        self.assertIn("стоимость", processor.synonyms)
        self.assertIn("цена", processor.synonym_map)
        self.assertEqual(processor.synonym_map["цена"], "стоимость")

if __name__ == "__main__":
    unittest.main()