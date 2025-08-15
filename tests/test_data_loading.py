"""Тесты загрузки данных из файлов"""

import unittest
import os
import tempfile
import shutil
from backend.keyword_processor import KeywordProcessor
from backend.synonym_mapper import SynonymMapper

class TestDataLoading(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_dir = tempfile.mkdtemp()
        
    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.test_dir)
    
    def test_keywords_loading(self):
        """Тест загрузки ключевых слов"""
        file_path = os.path.join(self.test_dir, "keywords.txt")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(
                "# Тестовые ключевые слова\n"
                "привет | greeting | Здравствуйте!\n"
                "доставка | delivery | Доставка 1-3 дня\n"
            )
        
        processor = KeywordProcessor(self.test_dir)
        self.assertIn("привет", processor.keyword_data)
        self.assertEqual(processor.keyword_data["привет"]["response"], "Здравствуйте!")