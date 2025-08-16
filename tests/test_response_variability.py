import unittest
from unittest.mock import MagicMock, patch
from backend.main import Backend

class TestResponseVariability(unittest.TestCase):
    def setUp(self):
        self.backend = Backend()
        self.backend.keyword_processor.process = MagicMock()
        
    def test_response_selection(self):
        """Тестирование выбора случайного ответа"""
        mock_responses = [
            {"responses": ["Вариант 1", "Вариант 2", "Вариант 3"], "type": "тест"}
        ]
        self.backend.keyword_processor.process.return_value = mock_responses
        
        responses = set()
        for _ in range(10):
            response = self.backend.process_message("тест")
            responses.add(response)
            
        self.assertGreaterEqual(len(responses), 2)
        
    def test_legacy_response_support(self):
        """Тестирование поддержки старого формата ответов"""
        mock_responses = [
            {"response": "Старый формат", "type": "тест"}
        ]
        self.backend.keyword_processor.process.return_value = mock_responses
        
        response = self.backend.process_message("тест")
        self.assertEqual(response, "Старый формат")
        
    def test_response_enhancement(self):
        """Тестирование улучшения ответов"""
        mock_responses = [
            {"responses": ["Основной ответ"], "type": "тест"}
        ]
        self.backend.keyword_processor.process.return_value = mock_responses
        
        with patch('random.random', return_value=0.2):  # 20% < 30% - должно добавиться улучшение
            response = self.backend.process_message("тест")
            self.assertIn("Основной ответ", response)
            self.assertGreater(len(response), len("Основной ответ"))

if __name__ == "__main__":
    unittest.main()