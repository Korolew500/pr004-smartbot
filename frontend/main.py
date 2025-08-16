"""Основной модуль frontend"""
import os


class Frontend:
    def __init__(self, backend):
        self.backend = backend
        self.active_interface = None
        self.interfaces = {
            'console': None,
            'telegram': None
        }
        print("Frontend инициализирован")

    def activate_interface(self, interface_name):
        """Активация выбранного интерфейса"""
        if interface_name == 'console':
            from .console import ConsoleInterface
            self.active_interface = ConsoleInterface()
            self._run_console_interface()
        elif interface_name == 'telegram':
            from .tele import TelegramInterface
            token = os.getenv('TELEGRAM_TOKEN')
            if not token:
                raise ValueError("TELEGRAM_TOKEN not set in environment")
            self.active_interface = TelegramInterface(token, self.backend)
            self._start_telegram_in_background()
        print(f"Активирован интерфейс: {interface_name}")

    def _run_console_interface(self):
        """Запуск консольного интерфейса"""
        print("Консольный интерфейс активирован. Введите сообщения (exit для выхода):")
        while True:
            try:
                user_input = self.active_interface.get_input()
                if user_input.lower() == 'exit':
                    print("Завершение работы...")
                    break
                response = self.backend.process_message(user_input)
                self.active_interface.send_response(response)
            except KeyboardInterrupt:
                print("\nЗавершение работы...")
                break

    def _start_telegram_in_background(self):
        """Запуск Telegram в фоновом режиме"""
        import threading
        threading.Thread(
            target=self.active_interface.run,
            daemon=True
        ).start()