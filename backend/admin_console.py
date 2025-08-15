class AdminConsole:
    def __init__(self, backend):
        self.backend = backend
        
    def search_synonyms(self, query):
        return self.backend.synonym_mapper.find_synonyms(query)
        
    def add_synonym(self, base_word, synonym):
        if not base_word or not synonym:
            print("Ошибка: Базовое слово и синоним обязательны")
            return False
            
        try:
            self.backend.add_synonym(base_word, synonym)
            print(f"Добавлен синоним: {synonym} → {base_word}")
            return True
        except Exception as e:
            print(f"Ошибка: {str(e)}")
            return False
            
    def remove_synonym(self, base_word, synonym):
        if not base_word or not synonym:
            print("Ошибка: Базовое слово и синоним обязательны")
            return False
            
        try:
            self.backend.remove_synonym(base_word, synonym)
            print(f"Удален синоним: {synonym} → {base_word}")
            return True
        except KeyError:
            print(f"Синоним не найден: {synonym}")
            return False
        except Exception as e:
            print(f"Ошибка: {str(e)}")
            return False
    
    def add_keyword(self, keyword, response, ktype="общий"):
        """Добавляет новое ключевое слово"""
        if not keyword or not response:
            print("Ошибка: Ключевое слово и ответ обязательны")
            return False
            
        try:
            self.backend.add_keyword(keyword, response, ktype)
            print(f"Добавлено ключевое слово: {keyword}")
            return True
        except Exception as e:
            print(f"Ошибка: {str(e)}")
            return False
    
    def remove_keyword(self, keyword):
        """Удаляет ключевое слово"""
        if not keyword:
            print("Ошибка: Укажите ключевое слово")
            return False
            
        try:
            self.backend.remove_keyword(keyword)
            print(f"Удалено ключевое слово: {keyword}")
            return True
        except KeyError:
            print(f"Ключевое слово не найдено: {keyword}")
            return False
        except Exception as e:
            print(f"Ошибка: {str(e)}")
            return False
    
    def toggle_module(self, module_name, state):
        """Включает/выключает модули обработки"""
        state_bool = state.lower() in ["on", "true", "1"]
        if self.backend.toggle_module(module_name, state_bool):
            print(f"Модуль {module_name} {'включен' if state_bool else 'выключен'}")
            return True
        print(f"Неизвестный модуль: {module_name}")
        return False
        
    def run(self):
        """Интерактивная консоль"""
        print("Административная консоль. Введите 'help' для списка команд.")
        while True:
            try:
                command = input("> ").strip()
                if command == "exit":
                    break
                elif command == "help":
                    print("Доступные команды:\n"
                          "  addsyn <база> <синоним>\n"
                          "  rmsyn <база> <синоним>\n"
                          "  addkey <ключ> <ответ> [тип]\n"
                          "  rmkey <ключ>\n"
                          "  module <имя> <on/off>\n"
                          "  exit")
                
                elif command.startswith("addsyn "):
                    parts = command.split(maxsplit=2)
                    if len(parts) == 3:
                        self.add_synonym(parts[1], parts[2])
                
                elif command.startswith("rmsyn "):
                    parts = command.split(maxsplit=2)
                    if len(parts) == 3:
                        self.remove_synonym(parts[1], parts[2])
                
                elif command.startswith("addkey "):
                    parts = command.split(maxsplit=3)
                    if len(parts) >= 3:
                        self.add_keyword(parts[1], parts[2], parts[3] if len(parts) > 3 else "общий")
                
                elif command.startswith("rmkey "):
                    parts = command.split(maxsplit=1)
                    if len(parts) == 2:
                        self.remove_keyword(parts[1])
                
                elif command.startswith("module "):
                    parts = command.split(maxsplit=2)
                    if len(parts) == 3:
                        self.toggle_module(parts[1], parts[2])
                
                else:
                    print("Неизвестная команда. Введите 'help' для справки.")
            
            except KeyboardInterrupt:
                print("\nЗавершение работы...")
                break
            except Exception as e:
                print(f"Ошибка: {str(e)}")