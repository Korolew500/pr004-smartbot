#!/usr/bin/env python3
"""Главный запускаемый файл проекта"""

import os
import sys
from backend.main import Backend
from frontend.main import Frontend
from backend.admin_console import AdminConsole  # <-- NEW

class SmartBot:
    def __init__(self):
        self.backend = Backend()
        self.frontend = Frontend(self.backend)
        self.admin_console = AdminConsole(self.backend)  # <-- NEW

    def run(self):
        """Основной цикл работы бота"""
        print("SmartBot запущен!")
        
        # Запуск админской консоли в отдельном потоке
        if os.getenv('ADMIN_MODE') == 'console':
            import threading
            threading.Thread(target=self.admin_console.run, daemon=True).start()
        
        # ... остальной код без изменений ...