from .data_manager import DataManager

class SynonymMapper:
    def __init__(self, data_dir='data'):
        self.synonym_map = {}
        self.base_map = {}
        self.data_manager = DataManager(data_dir)
        self._load_synonyms()

    def _load_synonyms(self):
        """Загружает синонимы и создает индекс"""
        self.base_map = self.data_manager.load_data("synonyms") or {}
        for base_word, synonyms in self.base_map.items():
            for synonym in synonyms:
                self.synonym_map[synonym] = base_word
                
    def map_to_base(self, word):
        """Отображает слово на его базовую форму"""
        return self.synonym_map.get(word, word)
        
    def find_synonyms(self, query):
        """Поиск синонимов по запросу"""
        results = {}
        query = query.lower()
        
        # Поиск по базовым словам
        for base_word, synonyms in self.base_map.items():
            if query in base_word.lower():
                results[base_word] = synonyms
                
        # Поиск по синонимам
        for synonym, base_word in self.synonym_map.items():
            if query in synonym.lower() and base_word not in results:
                results[base_word] = self.base_map.get(base_word, [])
                
        return results
        
    def add_synonym(self, base_word, synonym):
        """Добавляет новый синоним"""
        synonyms = self.base_map.get(base_word, [])
        if synonym not in synonyms:
            synonyms.append(synonym)
            self.base_map[base_word] = synonyms
            self.synonym_map[synonym] = base_word
            self.data_manager.save_data("synonyms", self.base_map)
            
    def remove_synonym(self, base_word, synonym):
        """Удаляет синоним"""
        if base_word in self.base_map:
            synonyms = self.base_map[base_word]
            if synonym in synonyms:
                synonyms.remove(synonym)
                self.base_map[base_word] = synonyms
                del self.synonym_map[synonym]
                self.data_manager.save_data("synonyms", self.base_map)