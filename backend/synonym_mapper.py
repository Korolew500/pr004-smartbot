from .data_manager import DataManager

class SynonymMapper:
    def __init__(self, data_dir='data'):
        self.synonym_map = {}
        self.data_manager = DataManager(data_dir)
        self._load_synonyms()

    def _load_synonyms(self):
        synonyms_data = self.data_manager.load_data("synonyms")
        for base_word, synonyms in synonyms_data.items():
            for synonym in synonyms:
                self.synonym_map[synonym] = base_word
                
    def map_to_base(self, word):
        """Отображает слово на его базовую форму"""
        return self.synonym_map.get(word, word)
        
    def find_synonyms(self, query):
        """Поиск синонимов по запросу"""
        try:
            results = {}
            query = query.lower()
            synonyms_data = self.data_manager.load_data("synonyms")
            
            # Поиск по базовым словам
            for base_word, synonyms in synonyms_data.items():
                if query in base_word.lower():
                    results[base_word] = synonyms
                    
            # Поиск по синонимам
            for synonym, base_word in self.synonym_map.items():
                if query in synonym.lower() and base_word not in results:
                    results[base_word] = synonyms_data.get(base_word, [])
                    
            return results
        except Exception as e:
            print(f"Ошибка поиска синонимов: {str(e)}")
            return {}