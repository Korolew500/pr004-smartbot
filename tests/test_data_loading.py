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
        
        # Создаем тестовые файлы
        cls.keyword_file = os.path.join(cls.test_dir, "keywords.json")
        with open(cls.keyword_file, 'w', encoding='utf-8') as f:
            f.write('{"test": {"responses": ["Test response"], "type": "test"}}')
        
    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.test_dir)
    
    def test_keywords_loading(self):
        """Тест загрузки ключевых слов"""
        processor = KeywordProcessor()
        
        # Временная подмена пути к файлу
        processor.keyword_file = self.keyword_file
        processor._load_keywords()
        
        self.assertIn("test", processor.keywords)
        self.assertEqual(processor.keywords["test"]["responses"][0], "Test response")