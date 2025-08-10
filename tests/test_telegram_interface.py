"""Тесты для Telegram интерфейса"""

import unittest
from unittest.mock import MagicMock, patch
import asyncio
from frontend.telegram import TelegramInterface

class TestTelegramInterface(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        
    async def async_test(self, test_func):
        await test_func()
        
    def run_async(self, test_func):
        self.loop.run_until_complete(self.async_test(test_func))
        
    def test_message_handling(self):
        """Тест обработки сообщений"""
        async def test():
            mock_backend = MagicMock()
            mock_backend.process_message.return_value = "Test response"
            
            interface = TelegramInterface("test_token", mock_backend)
            
            mock_update = MagicMock()
            mock_context = MagicMock()
            mock_update.message.text = "Test message"
            
            await interface.handle_message(mock_update, mock_context)
            
            mock_backend.process_message.assert_called_with("Test message")
            mock_update.message.reply_text.assert_called_with("Test response")
        
        self.run_async(test)

    def test_commands(self):
        """Тест обработки команд"""
        async def test():
            mock_backend = MagicMock()
            interface = TelegramInterface("test_token", mock_backend)
            
            mock_update = MagicMock()
            mock_update.effective_user.first_name = "TestUser"
            await interface.start(mock_update, None)
            mock_update.message.reply_text.assert_called_with("Привет TestUser! Я умный бот. Чем могу помочь?")
            
            mock_update.reset_mock()
            await interface.help(mock_update, None)
            args, kwargs = mock_update.message.reply_text.call_args
            self.assertIn("/start", args[0])
            self.assertIn("/help", args[0])
        
        self.run_async(test)