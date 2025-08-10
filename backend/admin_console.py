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
        except Exception as e:
            print(f"Ошибка при добавлении ключевого слова: {str(e)}")
    
    # ... остальные методы ...
    
    def run(self):
        """Интерактивная консоль с обработкой ошибок"""
        print("Административная консоль запущена. Введите 'help' для справки")
        while True:
            try:
                command = input("Admin> ").strip()
                if not command:
                    continue
                
                # ... обработка команд ...
                
            except KeyboardInterrupt:
                print("\nЗавершение работы...")
                break
            except Exception as e:
                print(f"Ошибка: {str(e)}")
                break