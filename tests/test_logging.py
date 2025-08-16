import unittest
import logging
from unittest.mock import patch
from backend.main import Backend

class TestLogging(unittest.TestCase):
    @patch('logging.Logger.info')
    def test_processing_logging(self, mock_log):
        """Тестирование логирования процесса обработки"""
        backend = Backend()
        backend.process_message("тестовое сообщение")
        
        # Проверяем что было минимум 2 логирования: начало обработки и результат
        self.assertGreaterEqual(mock_log.call_count, 2)
        
        # Проверяем что первое сообщение содержит текст сообщения
        first_call_args = mock_log.call_args_list[0][0][0]
        self.assertIn("тестовое сообщение", first_call_args)

if __name__ == "__main__":
    unittest.main()