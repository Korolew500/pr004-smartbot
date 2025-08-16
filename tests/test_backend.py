"""Обновленные тесты для backend модуля"""

import unittest
from unittest.mock import MagicMock
from backend.main import Backend

class TestBackend(unittest.TestCase):
    def setUp(self):
        self.backend = Backend()
        
        # Мокируем зависимости
        self.backend.keyword_processor.process = MagicMock(return_value=[
            {"responses": ["Тестовый ответ"], "type": "тест"}
        ])
        self.backend.spell_checker.correct_text = MagicMock(side_effect=lambda x: x)
        self.backend.synonym_mapper.map_to_base = MagicMock(side_effect=lambda x: x)
    
    def test_response_priority(self):
        """Тест приоритизации ответов"""
        mock_responses = [
            {"responses": ["Ответ 1"], "type": "продукт"},
            {"responses": ["Ответ 2"], "type": "вопрос"},
            {"responses": ["Ответ 3"], "type": "приветствие"}
        ]
        self.backend.keyword_processor.process.return_value = mock_responses
        
        result = self.backend.process_message("тест")
        self.assertEqual(result, "Ответ 3")  # Приветствие имеет высший приоритет
    
    def test_module_management(self):
        """Тест включения/выключения модулей"""
        self.assertTrue(self.backend.toggle_module("spell_check", False))
        self.assertFalse(self.backend.active_modules["spell_check"])
        
        self.assertTrue(self.backend.toggle_module("spell_check", True))
        self.assertTrue(self.backend.active_modules["spell_check"])
        
    def test_empty_response(self):
        """Тест обработки пустого ответа"""
        self.backend.keyword_processor.process.return_value = []
        result = self.backend.process_message("тест")
        self.assertEqual(result, "Не понимаю запрос")