"""Обновлённые тесты для backend модуля"""

import unittest
from unittest.mock import MagicMock
from backend.main import Backend

class TestBackend(unittest.TestCase):
    def setUp(self):
        self.backend = Backend()
        
        # Мокируем зависимости
        self.backend.keyword_processor.extract_keywords = MagicMock()
        self.backend.keyword_processor.get_response = MagicMock()
        self.backend.spell_checker.correct_text = MagicMock(side_effect=lambda x: x)
        self.backend.synonym_mapper.map_to_base = MagicMock(side_effect=lambda x: x)
    
    def test_composite_response(self):
        """Тест составного ответа из нескольких ключевых слов"""
        # Настройка моков
        self.backend.keyword_processor.extract_keywords.return_value = [
            "липовый мед",
            "стоимость",
            "заказ"
        ]
        
        self.backend.keyword_processor.get_response.side_effect = [
            "Липовый мед: 500 руб/банка",
            "Цены уточняйте по телефону",
            "Для заказа нажмите кнопку 'Оформить заказ'"
        ]
        
        # Тестовый запрос
        response = self.backend.process_message("Хочу липовый мед, какая стоимость и как заказать?")
        
        # Проверяем составной ответ
        expected = "Липовый мед: 500 руб/банка Цены уточняйте по телефону Для заказа нажмите кнопку 'Оформить заказ'"
        self.assertEqual(response, expected)
    
    def test_single_keyword_response(self):
        """Тест обработки одного ключевого слова"""
        self.backend.keyword_processor.extract_keywords.return_value = ["привет"]
        self.backend.keyword_processor.get_response.return_value = "Здравствуйте! Чем могу помочь?"
        
        response = self.backend.process_message("привет")
        self.assertEqual(response, "Здравствуйте! Чем могу помочь?")
    
    def test_no_keywords(self):
        """Тест отсутствия ключевых слов"""
        self.backend.keyword_processor.extract_keywords.return_value = []
        
        response = self.backend.process_message("случайный текст")
        self.assertEqual(response, "Извините, я не понял вопрос. Можете переформулировать?")
    
    def test_phrase_priority(self):
        """Тест приоритета длинных фраз"""
        # Настройка моков
        self.backend.keyword_processor.extract_keywords.side_effect = lambda text: ["липовый мед"]
        self.backend.keyword_processor.get_response.return_value = "Ответ по длинной фразе"
        
        response = self.backend.process_message("интересует липовый мед")
        self.assertEqual(response, "Ответ по длинной фразе")