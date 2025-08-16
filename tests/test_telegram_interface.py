"""Тесты для Telegram интерфейса"""

import unittest
from unittest.mock import AsyncMock, MagicMock, patch
import asyncio
from frontend.tele import TelegramInterface

class TestTelegramInterface(unittest.IsolatedAsyncioTestCase):
    async def test_message_handling(self):
        """Тест обработки сообщений"""
        mock_backend = MagicMock()
        mock_backend.process_message.return_value = "Test response"
        
        interface = TelegramInterface("test_token", mock_backend)
        
        mock_update = AsyncMock()
        mock_context = MagicMock()
        mock_update.message.text = "Test message"
        mock_update.message.reply_text = AsyncMock()
        
        await interface.handle_message(mock_update, mock_context)
        
        mock_backend.process_message.assert_called_with("Test message")
        mock_update.message.reply_text.assert_awaited_with("Test response")

    async def test_commands(self):
        """Тест обработки команд"""
        mock_backend = MagicMock()
        interface = TelegramInterface("test_token", mock_backend)
        
        mock_update = AsyncMock()
        mock_update.effective_user.first_name = "TestUser"
        mock_update.message.reply_text = AsyncMock()
        
        await interface.start(mock_update, None)
        mock_update.message.reply_text.assert_awaited_with("Привет TestUser! Я умный бот. Чем могу помочь?")
        
        await interface.help(mock_update, None)
        args, _ = mock_update.message.reply_text.call_args
        self.assertIn("/start", args[0])
        self.assertIn("/help", args[0])