class AdminConsole:
    def __init__(self, backend):
        self.backend = backend
        
    def add_keyword(self, keyword, response):
        """Добавляет ключевое слово"""
        # Логика добавления в DataManager
        print(f"Added keyword: {keyword} -> {response}")
        
    def export_data(self, format='json'):
        """Экспорт данных"""
        print(f"Exporting data in {format} format")
        
    def run(self):
        """Интерактивная консоль"""
        while True:
            command = input("Admin> ").split()
            if not command:
                continue
                
            if command[0] == "add":
                self.add_keyword(command[1], " ".join(command[2:]))
            elif command[0] == "export":
                self.export_data(command[1] if len(command)>1 else 'json')
            elif command[0] == "exit":
                break