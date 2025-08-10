class AdminConsole:
    def __init__(self, backend):
        self.backend = backend
        
    def search_synonyms(self, query):
        """Поиск синонимов по запросу"""
        return self.backend.synonym_mapper.find_synonyms(query)
        
    def add_synonym(self, base_word, synonym):
        """Добавляет синоним к базовому слову"""
        if not base_word or not synonym:
            print("Ошибка: Базовое слово и синоним обязательны")
            return False
            
        try:
            synonyms = self.backend.synonym_mapper.synonym_map.get(base_word, [])
            
            if synonym not in synonyms:
                synonyms.append(synonym)
                self.backend.synonym_mapper.synonym_map[base_word] = synonyms
                
                self.backend.synonym_mapper.data_manager.save_data(
                    "synonyms",
                    {k: v for k, v in self.backend.synonym_mapper.synonym_map.items()}
                )
                
            print(f"Добавлен синоним: {synonym} → {base_word}")
            return True
        except Exception as e:
            print(f"Ошибка при добавлении синонима: {str(e)}")
            return False
            
    def remove_synonym(self, base_word, synonym):
        """Удаляет синоним из базового слова"""
        if not base_word or not synonym:
            print("Ошибка: Базовое слово и синоним обязательны")
            return False
            
        try:
            if base_word in self.backend.synonym_mapper.synonym_map:
                synonyms = self.backend.synonym_mapper.synonym_map[base_word]
                if synonym in synonyms:
                    synonyms.remove(synonym)
                    self.backend.synonym_mapper.data_manager.save_data(
                        "synonyms",
                        {k: v for k, v in self.backend.synonym_mapper.synonym_map.items()}
                    )
                    print(f"Удален синоним: {synonym} → {base_word}")
                    return True
                else:
                    print(f"Синоним {synonym} не найден для {base_word}")
                    return False
            else:
                print(f"Базовое слово {base_word} не найдено")
                return False
        except Exception as e:
            print(f"Ошибка при удалении синонима: {str(e)}")
            return False
            
    def get_synonyms(self):
        """Возвращает словарь всех синонимов"""
        return self.backend.synonym_mapper.synonym_map
        
    def run(self):
        """Интерактивная консоль с обработкой ошибок"""
        print("Административная консоль. Введите 'help' для списка команд.")
        while True:
            try:
                command = input("> ").strip()
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