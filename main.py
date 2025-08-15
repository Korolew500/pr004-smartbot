#!/usr/bin/env python3
"""Главный запускаемый файл проекта"""

import os
import sys
import time
from backend.main import Backend
from frontend.main import Frontend
from backend.admin_console import AdminConsole

class SmartBot:
    def __init__(self):
        self.backend = Backend()
        self.frontend = Frontend(self.backend)
        self.admin_console = AdminConsole(self.backend)

    def run(self):
        """Основной цикл работы бота"""
        print("SmartBot запущен!")
        
        # Запуск админской консоли в отдельном потоке
        if os.getenv('ADMIN_MODE') == 'console':
            import threading
            threading.Thread(target=self.admin_console.run, daemon=True).start()
        
        # Активация основного интерфейса
        interface_mode = os.getenv('FRONTEND_INTERFACE', 'console')
        self.frontend.activate_interface(interface_mode)
        
        # Поддержка работы для Telegram интерфейса
        if interface_mode == 'telegram':
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("Завершение работы...")

if __name__ == "__main__":
    bot = SmartBot()
    bot.run()