"""Тесты загрузки данных из файлов"""

import unittest
import os
import tempfile
from backend.keyword_processor import KeywordProcessor
from backend.synonym_mapper import SynonymMapper

class TestDataLoading(unittest.TestCase):
    def test_keywords_loading(self):
        """Тест загрузки ключевых слов"""
        # Исправление: использование контекстного менеджера
        with tempfile.NamedTemporaryFile(mode='w+', encoding='utf-8', delete=False) as f:
            f.write(
                "# Тестовые ключевые слова\n"
                "привет | greeting | Здравствуйте!\n"
                "доставка | delivery | Доставка 1-3 дня\n"
            )
            f.flush()
            file_path = f.name
        
        try:
            processor = KeywordProcessor(file_path)
            self.assertIn("привет", processor.keyword_responses)
            self.assertEqual(processor.keyword_responses["привет"], "Здравствуйте!")
        finally:
            os.unlink(file_path)
    
    def test_synonyms_loading(self):
        """Тест загрузки синонимов"""
        # Исправление: гарантированное закрытие файла
        with tempfile.NamedTemporaryFile(mode='w+', encoding='utf-8', delete=False) as f:
            f.write(
                "# Тестовые синонимы\n"
                "привет | здравствуйте, добрый день\n"
                "доставка | отправка, привоз\n"
            )
            f.flush()
            file_path = f.name
        
        try:
            mapper = SynonymMapper(file_path)
            self.assertEqual(mapper.synonym_map["здравствуйте"], "привет")
            self.assertEqual(mapper.synonym_map["добрый день"], "привет")
        finally:
            os.unlink(file_path)

if __name__ == "__main__":
    unittest.main()