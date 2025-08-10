class AdminConsole:
    def __init__(self, backend):
        self.backend = backend
        
    def add_keyword(self, keyword, response):
        """Добавляет ключевое слово с валидацией"""
        if not keyword or not response:
            print("Ошибка: Ключевое слово и ответ обязательны")
            return
            
        try:
            self.backend.keyword_processor.add_keyword(keyword, response)
            print(f"Added keyword: {keyword} -> {response}")
            return True
        except Exception as e:
            print(f"Ошибка при добавлении ключевого слова: {str(e)}")
            return False
    
    def run(self):
        """Интерактивная консоль с обработкой ошибок"""
        print("Административная консоль запущена. Введите 'help' для справки")
        while True:
            try:
                command = input("Admin> ").strip()
                if command == "exit":
                    print("Завершение работы...")
                    break
                elif command == "help":
                    print("Доступные команды: add <ключ> <ответ>, exit")
                elif command.startswith("add "):
                    parts = command.split(maxsplit=2)
                    if len(parts) < 3:
                        print("Ошибка: Неверный формат. Используйте: add <ключ> <ответ>")
                    else:
                        self.add_keyword(parts[1], parts[2])
                else:
                    print(f"Неизвестная команда: {command}")
            except KeyboardInterrupt:
                print("\nЗавершение работы...")
                break
            except Exception as e:
                print(f"Ошибка: {str(e)}")