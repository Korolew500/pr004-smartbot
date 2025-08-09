import unittest
import os
from backend.logger import setup_logger

class TestLogger(unittest.TestCase):
    def test_log_creation(self):
        """Тест создания лог-файла"""
        logger = setup_logger('test_logger', log_file='test.log')
        logger.info('Test log entry')
        
        self.assertTrue(os.path.exists('logs/test.log'))
        with open('logs/test.log', 'r') as f:
            content = f.read()
            self.assertIn('Test log entry', content)

if __name__ == '__main__':
    unittest.main()