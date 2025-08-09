import unittest
from backend.spell_checker import SpellChecker

class TestSpellChecker(unittest.TestCase):
    def setUp(self):
        self.checker = SpellChecker()
    
    def test_short_words(self):
        """Тестирование обработки коротких слов"""
        self.assertEqual(self.checker.correct_spelling("я"), "я")
        self.assertEqual(self.checker.correct_spelling("и"), "и")
        self.assertEqual(self.checker.correct_spelling("к"), "к")
        self.assertEqual(self.checker.correct_spelling("a"), "a")
    
    def test_numbers(self):
        """Цифры не должны корректироваться"""
        self.assertEqual(self.checker.correct_spelling("123"), "123")
        self.assertEqual(self.checker.correct_spelling("42"), "42")
    
    def test_correction(self):
        """Тест базовой коррекции"""
        self.assertEqual(self.checker.correct_spelling("првет"), "привет")
        self.assertEqual(self.checker.correct_spelling("мине"), "мне")
    
    def test_full_text(self):
        """Тест коррекции полного текста"""
        text = "првет как дила"
        corrected = "привет как дела"
        self.assertEqual(self.checker.correct_text(text), corrected)

if __name__ == "__main__":
    unittest.main()