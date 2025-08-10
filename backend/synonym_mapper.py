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