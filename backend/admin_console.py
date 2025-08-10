class AdminConsole:
    ...
    
    def search_synonyms(self, query):
        """Поиск синонимов по запросу"""
        return self.backend.synonym_mapper.find_synonyms(query)
    
    ...