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
        self.assertIn("привет", processor.keyword_responses)
        self.assertEqual(processor.keyword_responses["привет"], "Здравствуйте!")
    
    def test_synonyms_loading(self):
        """Тест загрузки синонимов"""
        file_path = os.path.join(self.test_dir, "synonyms.txt")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(
                "# Тестовые синонимы\n"
                "привет | здравствуйте, добрый день\n"
                "доставка | отправка, привоз\n"
            )
        
        mapper = SynonymMapper(self.test_dir)
        self.assertEqual(mapper.synonym_map["здравствуйте"], "привет")
        self.assertEqual(mapper.synonym_map["добрый день"], "привет")

if __name__ == "__main__":
    unittest.main()