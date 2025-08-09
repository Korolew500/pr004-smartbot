"""Основной модуль frontend"""

class Frontend:
    def __init__(self):
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
        # TODO: Реализовать другие интерфейсы
        print(f"Активирован интерфейс: {interface_name}")

    def get_input(self):
        """Получение ввода от пользователя"""
        return self.active_interface.get_input()

    def send_response(self, response):
        """Отправка ответа пользователю"""
        self.active_interface.send_response(response)