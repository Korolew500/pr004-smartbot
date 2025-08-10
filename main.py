#!/usr/bin/env python3
"""Главный запускаемый файл проекта"""

import os
import sys
from backend.main import Backend
from frontend.main import Frontend
from backend.admin_console import AdminConsole
from frontend.web_admin import init_web_admin  # <-- NEW IMPORT

class SmartBot:
    def __init__(self):
        self.backend = Backend()
        self.frontend = Frontend(self.backend)
        self.admin_console = AdminConsole(self.backend)
        
        # Инициализация веб-интерфейса администратора
        init_web_admin(self.admin_console)  # <-- NEW INIT

    def run(self):
        """Основной цикл работы бота"""
        print("SmartBot запущен!")
        
        # Запуск админской консоли в отдельном потоке
        if os.getenv('ADMIN_MODE') == 'console':
            import threading
            threading.Thread(target=self.admin_console.run, daemon=True).start()
        
        # Запуск веб-интерфейса администратора
        if os.getenv('ADMIN_MODE') == 'web':
            import threading
            from frontend.web_admin import app
            threading.Thread(
                target=lambda: app.run(host='0.0.0.0', port=5000),
                daemon=True
            ).start()
            print("Веб-интерфейс администратора доступен по адресу: http://localhost:5000")
        
        # ... остальной код без изменений ...