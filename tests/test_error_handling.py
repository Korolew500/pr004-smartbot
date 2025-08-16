import unittest
from unittest.mock import MagicMock, patch
from backend.main import Backend

class TestErrorHandling(unittest.TestCase):
    def setUp(self):
        self.backend = Backend()
        
    def test_module_failure_handling(self):
        """Тестирование обработки сбоев в модулях"""
        with patch('backend.spell_checker.SpellChecker.correct_text', side_effect=Exception("Test error")):
            response = self.backend.process_message("тест")
            self.assertIn("ошибка", response.lower())
            
    def test_keyword_processor_failure(self):
        """Тестирование обработки сбоев в обработчике ключевых слов"""
        with patch('backend.keyword_processor.KeywordProcessor.process', side_effect=Exception("Test error")):
            response = self.backend.process_message("тест")
            self.assertIn("ошибка", response.lower())

if __name__ == "__main__":
    unittest.main()