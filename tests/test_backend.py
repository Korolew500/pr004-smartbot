"""Обновленные тесты для backend модуля"""

import unittest
from unittest.mock import MagicMock
from backend.main import Backend

class TestBackend(unittest.TestCase):
    def setUp(self):
        self.backend = Backend()
        
        # Мокируем зависимости (ИСПРАВЛЕНО: map_to_base вместо map_synonyms)
        self.backend.keyword_processor.process = MagicMock(return_value=[
            {"responses": ["Тестовый ответ"], "type": "тест"}
        ])
        self.backend.spell_checker.correct_text = MagicMock(side_effect=lambda x: x)
        self.backend.synonym_mapper.map_to_base = MagicMock(side_effect=lambda x: x)
    
    def test_composite_response(self):
        """Тест составного ответа из нескольких ключевых слов"""
        # Создаем тестовые ключевые слова
        self.bot.keyword_processor.keywords = {
            "мед": {"responses": ["У нас есть липовый мед!"]},
            "липовый": {"response": "Липовый мед: 500 руб/банка"},
            "стоимость": {"responses": ["Цены уточняйте по телефону"]}
        }
        
        # Тестовое сообщение содержит несколько ключевых слов
        response = self.bot.process_message("Хочу липовый мед, какая стоимость?")
        self.assertIn("липовый мед", response)
        self.assertIn("Цены уточняйте", response)
        """Тест приоритизации ответов"""
        mock_responses = [
            {"responses": ["Ответ 1"], "type": "продукт"},
            {"responses": ["Ответ 2"], "type": "вопрос"},
            {"responses": ["Ответ 3"], "type": "приветствие"}
        ]
        self.backend.keyword_processor.process.return_value = mock_responses
        
        result = self.backend.process_message("тест")
        self.assertEqual(result, "Ответ 3")  # Проверка приоритизации
    
    # УДАЛЕН: тест на несуществующий метод toggle_module
    
    def test_empty_response(self):
        """Тест обработки пустого ответа"""
        self.backend.keyword_processor.process.return_value = []
        result = self.backend.process_message("тест")
        self.assertEqual(result, "Извините, я не понял вопрос. Можете переформулировать?")