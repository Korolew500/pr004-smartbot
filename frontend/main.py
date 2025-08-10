"""Основной модуль frontend"""

class Frontend:
    def __init__(self, backend):  # <-- ADDED BACKEND ARGUMENT
        self.backend = backend  # <-- NEW
        self.active_interface = None
        self.interfaces = {
            'console': None,
            'web': None,
            'api': None,
            'telegram': None
        }
        print("Frontend инициализирован")

    def activate_interface(self, interface_name):
        """Активация выбранного интерфейса"""
        if interface_name == 'console':
            from .console import ConsoleInterface
            self.active_interface = ConsoleInterface()
        elif interface_name == 'telegram':
            from .telegram import TelegramInterface
            token = os.getenv('TELEGRAM_TOKEN')
            if not token:
                raise ValueError("TELEGRAM_TOKEN not set in environment")
            self.active_interface = TelegramInterface(token, self.backend)
        # TODO: Реализовать другие интерфейсы
        print(f"Активирован интерфейс: {interface_name}")
        
        # Start Telegram bot in background if activated
        if interface_name == 'telegram':
            import threading
            threading.Thread(target=self.active_interface.run, daemon=True).start()

    # ... остальной код без изменений ...