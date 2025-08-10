"""Тесты для Telegram интерфейса"""

import unittest
from unittest.mock import MagicMock, patch
from frontend.telegram import TelegramInterface

class TestTelegramInterface(unittest.TestCase):
    @patch('frontend.telegram.ApplicationBuilder')
    def test_message_handling(self, mock_builder):
        """Тест обработки сообщений"""
        # Мокируем бэкенд
        mock_backend = MagicMock()
        mock_backend.process_message.return_value = "Test response"
        
        # Создаем экземпляр интерфейса
        interface = TelegramInterface("test_token", mock_backend)
        
        # Создаем мок-объекты Telegram
        mock_update = MagicMock()
        mock_context = MagicMock()
        mock_update.message.text = "Test message"
        
        # Вызываем обработчик
        interface.handle_message(mock_update, mock_context)
        
        # Проверяем вызовы
        mock_backend.process_message.assert_called_with("Test message")
        mock_update.message.reply_text.assert_called_with("Test response")

    @patch('frontend.telegram.ApplicationBuilder')
    def test_commands(self, mock_builder):
        """Тест обработки команд"""
        mock_backend = MagicMock()
        interface = TelegramInterface("test_token", mock_backend)
        
        # Тест команды /start
        mock_update = MagicMock()
        mock_update.effective_user.first_name = "TestUser"
        interface.start(mock_update, None)
        mock_update.message.reply_text.assert_called_with("Привет TestUser! Я умный бот. Чем могу помочь?")
        
        # Тест команды /help
        mock_update.reset_mock()
        interface.help(mock_update, None)
        mock_update.message.reply_text.assert_called()
        self.assertIn("/start", mock_update.message.reply_text.call_args[0][0])
        self.assertIn("/help", mock_update.message.reply_text.call_args[0][0])