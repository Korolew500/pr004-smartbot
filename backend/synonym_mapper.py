class SynonymMapper:
    def __init__(self, synonyms_path='data/synonyms.txt'):
        self.synonym_map = {}
        self.synonyms_path = synonyms_path
        self._load_synonyms()

    def _load_synonyms(self):
        try:
            with open(self.synonyms_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    
                    parts = [p.strip() for p in line.split('|')]
                    if len(parts) < 2:
                        continue
                        
                    base_word = parts[0]
                    synonyms = [s.strip() for s in parts[1].split(',')]
                    
                    for synonym in synonyms:
                        self.synonym_map[synonym] = base_word
        except FileNotFoundError:
            print(f"Warning: {self.synonyms_path} not found")

    def map_to_base(self, word):
        """Преобразует синоним в базовое слово"""
        return self.synonym_map.get(word, word)