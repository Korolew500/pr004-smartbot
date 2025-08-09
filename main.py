#!/usr/bin/env python3
"""Главный запускаемый файл проекта"""

from backend.main import Backend
from frontend.main import Frontend

class SmartBot:
    def __init__(self):
        self.backend = Backend()
        self.frontend = Frontend()

    def run(self):
        """Основной цикл работы бота"""
        print("SmartBot запущен!")
        self.frontend.activate_interface('console')
        
        while True:
            user_input = self.frontend.get_input()
            if user_input.lower() == 'exit':
                break
            
            # Обработка сообщения в backend
            response = self.backend.process_message(user_input)
            
            # Отправка ответа через frontend
            self.frontend.send_response(response)

if __name__ == "__main__":
    bot = SmartBot()
    bot.run()