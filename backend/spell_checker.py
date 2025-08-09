import re
from spellchecker import SpellChecker as ExternalSpellChecker

class SpellChecker:
    def __init__(self):
        self.spell = ExternalSpellChecker(language='ru')
        
    def correct_spelling(self, word: str) -> str:
        """Обработка коротких слов и специальных случаев"""
        if len(word) < 3:
            return word
            
        if re.match(r'^\d+$', word):
            return word
            
        return self.spell.correction(word) or word

    def correct_text(self, text: str) -> str:
        """Коррекция орфографии во всем тексте"""
        words = text.split()
        corrected = [self.correct_spelling(word) for word in words]
        return ' '.join(corrected)