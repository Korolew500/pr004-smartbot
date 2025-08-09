"""Консольный интерфейс"""

class ConsoleInterface:
    def get_input(self):
        return input("Вы: ")
    
    def send_response(self, response):
        print(f"Бот: {response}")