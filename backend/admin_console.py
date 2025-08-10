class AdminConsole:
    def __init__(self, backend):
        self.backend = backend
        
    def add_keyword(self, keyword, response):
        ...
            
    def add_synonym(self, base_word, synonym):
        ...
    
    def remove_synonym(self, base_word, synonym):
        """Удаляет синоним из списка для базового слова"""
        if not base_word or not synonym:
            print("Ошибка: Базовое слово и синоним обязательны")
            return False
            
        try:
            synonyms = self.backend.synonym_mapper.synonym_map.get(base_word, [])
            
            if synonym in synonyms:
                synonyms.remove(synonym)
                self.backend.synonym_mapper.synonym_map[base_word] = synonyms
                
                self.backend.synonym_mapper.data_manager.save_data("synonyms", 
                    {k: v for k, v in self.backend.synonym_mapper.synonym_map.items()})
                
                print(f"Удален синоним: {synonym} → {base_word}")
                return True
            else:
                print(f"Синоним {synonym} не найден для {base_word}")
                return False
        except Exception as e:
            print(f"Ошибка при удалении синонима: {str(e)}")
            return False
    
    def get_synonyms(self):
        ...
    
    def run(self):
        ...