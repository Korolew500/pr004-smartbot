"""Обновленные тесты коррекции орфографии"""

import unittest
from backend.spell_checker import check_spelling

class TestSpellChecker(unittest.TestCase):
    def test_basic_correction(self):
        self.assertEqual(check_spelling("привет"), "привет")
        self.assertEqual(check_spelling("приветсвую"), "приветствовать")
        self.assertEqual(check_spelling("машына"), "машина")

    def test_special_cases(self):
        self.assertEqual(check_spelling("приветсвуй"), "приветствовать")
        self.assertEqual(check_spelling("приветсвует"), "приветствовать")
        self.assertEqual(check_spelling("машына"), "машина")

    def test_short_words(self):
        self.assertEqual(check_spelling("а"), "а")
        self.assertEqual(check_spelling("я"), "я")
        self.assertEqual(check_spelling("с"), "с")

if __name__ == '__main__':
    unittest.main()