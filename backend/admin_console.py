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
            
    def add_synonym(self, base_word, synonym):
        """Добавляет синоним к базовому слову"""
        if not base_word or not synonym:
            print("Ошибка: Базовое слово и синоним обязательны")
            return False
            
        try:
            # Получаем текущие синонимы
            synonyms = self.backend.synonym_mapper.synonym_map.get(base_word, [])
            
            # Добавляем новый синоним если его еще нет
            if synonym not in synonyms:
                synonyms.append(synonym)
                self.backend.synonym_mapper.synonym_map[base_word] = synonyms
                
                # Обновляем данные в менеджере
                self.backend.synonym_mapper.data_manager.save_data("synonyms", 
                    {k: v for k, v in self.backend.synonym_mapper.synonym_map.items()})
                
            print(f"Добавлен синоним: {synonym} → {base_word}")
            return True
        except Exception as e:
            print(f"Ошибка при добавлении синонима: {str(e)}")
            return False
    
    def get_synonyms(self):
        """Возвращает словарь всех синонимов"""
        return self.backend.synonym_mapper.synonym_map
    
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
                    print("Доступные команды: add <ключ> <ответ>, addsyn <базовое> <синоним>, exit")
                elif command.startswith("add "):
                    parts = command.split(maxsplit=2)
                    if len(parts) < 3:
                        print("Ошибка: Неверный формат. Используйте: add <ключ> <ответ>")
                    else:
                        self.add_keyword(parts[1], parts[2])
                elif command.startswith("addsyn "):
                    parts = command.split(maxsplit=2)
                    if len(parts) < 3:
                        print("Ошибка: Неверный формат. Используйте: addsyn <базовое> <синоним>")
                    else:
                        self.add_synonym(parts[1], parts[2])
                else:
                    print(f"Неизвестная команда: {command}")
            except KeyboardInterrupt:
                print("\nЗавершение работы...")
                break
            except Exception as e:
                print(f"Ошибка: {str(e)}")