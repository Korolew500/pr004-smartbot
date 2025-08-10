"""Обновленные тесты для backend модуля"""

import unittest
import os
import sys
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.keyword_processor import KeywordProcessor
from backend.main import Backend
from backend.synonym_mapper import SynonymMapper

class TestBackend(unittest.TestCase):
    def setUp(self):
        self.backend = Backend()
    
    def test_keyword_processing(self):
        """Тест обработки ключевых слов"""
        processor = KeywordProcessor()
        
        # Используем реальные данные вместо моков
        response = processor.process("привет")
        self.assertIn("Здравствуйте", response[0])
        
        response = processor.process("пока")
        self.assertIn("До свидания", response[0])
        
        # Проверка неизвестных запросов
        response = processor.process("случайный текст")
        self.assertEqual(response[0], "Не понимаю ваш запрос")

    @patch('backend.main.KeywordProcessor')
    @patch('backend.main.SynonymMapper')
    @patch('backend.spell_checker.SpellChecker')
    def test_full_workflow(self, mock_spell, mock_synonym, mock_kw):
        """Тест полного workflow бэкенда"""
        # Настраиваем моки
        mock_processor = mock_kw.return_value
        mock_processor.process.return_value = ["Тестовый ответ"]
        
        mock_synonym.return_value.map_to_base.side_effect = lambda x: "привет" if x == "здравствуйте" else x
        
        mock_spell.return_value.correct_text.side_effect = lambda x: x.replace("здарвствуйте", "здравствуйте")
        
        # Тестируем бэкенд
        backend = Backend()
        
        # Проверяем обработку сообщения
        response = backend.process_message("здарвствуйте")
        self.assertEqual(response, "Тестовый ответ")
        
        # Проверяем вызовы
        mock_spell.return_value.correct_text.assert_called_once()
        mock_synonym.return_value.map_to_base.assert_called()
        mock_processor.process.assert_called_once()

    def test_synonym_mapping(self):
        """Тест преобразования синонимов"""
        mapper = SynonymMapper()
        # Тест на реальных данных
        self.assertEqual(mapper.map_to_base("здравствуйте"), "привет")
        self.assertEqual(mapper.map_to_base("добрый день"), "привет")
        self.assertEqual(mapper.map_to_base("несуществующее"), "несуществующее")