"""Тесты вариативности ответов"""

import unittest
from unittest.mock import MagicMock
from backend.main import Backend

class TestResponseVariability(unittest.TestCase):
    def setUp(self):
        self.processor = Backend()
        self.processor.keyword_processor = MagicMock()
        self.processor.spell_checker = MagicMock()
        self.processor.synonym_mapper = MagicMock()
        
    def test_response_selection(self):
        """Тест выбора ответа из нескольких вариантов"""
        mock_responses = [
            {"responses": ["Вариант 1", "Вариант 2"]},
            {"response": "Вариант 3"}
        ]
        self.processor.keyword_processor.process.return_value = mock_responses
        
        result = self.processor.process_message("тест")
        self.assertIn(result, ["Вариант 1", "Вариант 2", "Вариант 3"])
        
    def test_legacy_response_support(self):
        """Тест поддержки старого формата ответов"""
        mock_responses = [{"response": "Старый формат ответа"}]
        self.processor.keyword_processor.process.return_value = mock_responses
        
        result = self.processor.process_message("тест")
        self.assertEqual(result, "Старый формат ответа")
        
    def test_response_enhancement(self):
        """Тест улучшения ответов"""
        # Тест требует доработки после исправления основного функционала
        pass