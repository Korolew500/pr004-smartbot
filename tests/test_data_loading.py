"""Обновленные тесты загрузки данных"""

import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.keyword_processor import KeywordProcessor

class TestDataLoading(unittest.TestCase):
    def test_keywords_loading(self):
        """Тест загрузки ключевых слов"""
        processor = KeywordProcessor()
        self.assertIn("привет", processor.keywords)
        self.assertEqual(processor.keywords["привет"]["response"], "Здравствуйте! Чем могу помочь?")

    def test_synonyms_loading(self):
        """Тест загрузки синонимов"""
        processor = KeywordProcessor()
        
        # Проверяем отображение синоним->базовое
        self.assertIn("здравствуй", processor.synonym_map)
        self.assertEqual(processor.synonym_map["здравствуй"], "привет")
        
        # Проверяем отображение базовое->синонимы
        self.assertIn("привет", processor.base_to_synonyms)
        self.assertIn("добрый день", processor.base_to_synonyms["привет"])

if __name__ == "__main__":
    unittest.main()