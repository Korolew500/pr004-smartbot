import unittest
from unittest.mock import MagicMock, patch
from backend.admin_console import AdminConsole

class TestAdminConsole(unittest.TestCase):
    def setUp(self):
        # Создаем мок бэкенда
        self.mock_backend = MagicMock()
        self.console = AdminConsole(self.mock_backend)

    def test_remove_synonym(self):
        """Тест удаления синонима"""
        self.mock_backend.synonym_mapper.synonym_map = {"test_base": ["test_syn"]}
        with patch('builtins.print') as mock_print:
            result = self.console.remove_synonym("test_base", "test_syn")
            self.assertTrue(result)
            self.assertNotIn("test_syn", self.mock_backend.synonym_mapper.synonym_map["test_base"])
            mock_print.assert_called_with("Удален синоним: test_syn → test_base")
    
    def test_remove_nonexistent_synonym(self):
        """Тест удаления несуществующего синонима"""
        self.mock_backend.synonym_mapper.synonym_map = {"test_base": []}
        with patch('builtins.print') as mock_print:
            result = self.console.remove_synonym("test_base", "missing")
            self.assertFalse(result)
            mock_print.assert_called_with("Синоним missing не найден для test_base")