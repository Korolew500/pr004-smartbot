"""Тесты для DataManager"""

import unittest
import os
import tempfile
from backend.data_manager import DataManager

class TestDataManager(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.manager = DataManager(self.temp_dir)

    def test_txt_to_json_conversion(self):
        """Тест конвертации TXT в JSON"""
        # Создаем тестовый TXT
        with open(os.path.join(self.temp_dir, "test.txt"), 'w', encoding='utf-8') as f:
            f.write("key1 | value1\nkey2 | value2,value3")

        # Загружаем данные
        data = self.manager.load_data("test")
        
        # Проверяем результат
        self.assertEqual(data, {"key1": "value1", "key2": ["value2", "value3"]})
        
        # Проверяем создание JSON
        json_path = os.path.join(self.temp_dir, "test.json")
        self.assertTrue(os.path.exists(json_path))

    def test_save_and_load_json(self):
        """Тест сохранения и загрузки JSON"""
        test_data = {"key": "value"}
        
        # Сохраняем данные
        self.assertTrue(self.manager.save_data("test", test_data))
        
        # Загружаем данные
        loaded_data = self.manager.load_data("test")
        
        # Проверяем результат
        self.assertEqual(loaded_data, test_data)

    def tearDown(self):
        # Удаляем временную директорию
        for file in os.listdir(self.temp_dir):
            os.remove(os.path.join(self.temp_dir, file))
        os.rmdir(self.temp_dir)