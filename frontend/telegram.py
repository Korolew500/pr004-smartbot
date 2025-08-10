"""Telegram bot interface"""

import logging
from telegram import Update, Bot
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    CallbackContext
)

class TelegramInterface:
    def __init__(self, token: str, backend):
        self.backend = backend
        self.logger = logging.getLogger('telegram')
        
        # Initialize bot
        self.application = ApplicationBuilder().token(token).build()
        
        # Register handlers
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CommandHandler("help", self.help))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        
        self.logger.info("Telegram interface initialized")

    async def start(self, update: Update, context: CallbackContext) -> None:
        """Send welcome message"""
        user = update.effective_user
        await update.message.reply_text(f"Привет {user.first_name}! Я умный бот. Чем могу помочь?")

    async def help(self, update: Update, context: CallbackContext) -> None:
        """Send help message"""
        help_text = (
            "Доступные команды:\n"
            "/start - Начать диалог\n"
            "/help - Показать справку\n\n"
            "Просто напишите ваш вопрос, и я постараюсь помочь!"
        )
        await update.message.reply_text(help_text)

    async def handle_message(self, update: Update, context: CallbackContext) -> None:
        """Process incoming messages"""
        user_input = update.message.text
        self.logger.info(f"Received message: {user_input}")
        
        # Process message through backend
        response = self.backend.process_message(user_input)
        
        # Send response
        await update.message.reply_text(response)

    def run(self):
        """Start the bot"""
        self.logger.info("Starting Telegram bot...")
        self.application.run_polling()