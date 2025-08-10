"""Тесты для административной консоли"""

import unittest
from unittest.mock import MagicMock, patch
from backend.admin_console import AdminConsole

class TestAdminConsole(unittest.TestCase):
    def setUp(self):
        self.mock_backend = MagicMock()
        self.console = AdminConsole(self.mock_backend)
    
    def test_add_keyword(self):
        """Тест добавления ключевого слова"""
        with patch('builtins.print') as mock_print:
            self.console.add_keyword("доставка", "Сроки доставки 1-3 дня")
            self.mock_backend.keyword_processor.add_keyword.assert_called_with(
                "доставка", "Сроки доставки 1-3 дня"
            )
            mock_print.assert_called_with("Added keyword: доставка -> Сроки доставки 1-3 дня")
    
    def test_invalid_add_keyword(self):
        """Тест добавления невалидного ключевого слова"""
        with patch('builtins.print') as mock_print:
            self.console.add_keyword("", "Пустое ключевое слово")
            mock_print.assert_called_with("Ошибка: Ключевое слово и ответ обязательны")
    
    @patch('builtins.input', side_effect=["add test_key test_response", "exit"])
    def test_run_add_command(self, mock_input):
        """Тест выполнения команды добавления"""
        with patch.object(self.console, 'add_keyword') as mock_add:
            self.console.run()
            mock_add.assert_called_with("test_key", "test_response")