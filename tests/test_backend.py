import unittest
from backend.main import Backend
from unittest.mock import MagicMock

class TestBackend(unittest.TestCase):
    def setUp(self):
        self.backend = Backend()
        self.backend.spell_checker = MagicMock()
        self.backend.spell_checker.correct_text = lambda x: x
        self.backend.synonym_mapper = MagicMock()
        self.backend.synonym_mapper.map_to_base = lambda x: x
        self.backend.keyword_processor.keywords = {
            "привет": {"responses": ["Здравствуйте!"]},
            "мед": {"responses": ["У нас есть разные виды меда."]},
            "стоит": {"responses": ["Цена зависит от объема."]}
        }

    def test_composite_response(self):
        """Тест составного ответа из нескольких ключевых слов"""
        result = self.backend.process_message("привет сколько стоит мед")
        self.assertIn("Здравствуйте!", result)
        self.assertIn("Цена зависит от объема.", result)
        self.assertIn("У нас есть разные виды меда.", result)

    def test_stop_words_removal(self):
        """Тест удаления стоп-слов"""
        self.backend.stop_words = {"и", "в", "на"}
        result = self.backend.process_message("Привет и пока")
        self.assertIn("Здравствуйте!", result)

    def test_spell_correction(self):
        """Тест коррекции орфографии"""
        self.backend.spell_checker.correct_text = lambda x: "привет" if x == "првиет" else x
        result = self.backend.process_message("првиет")
        self.assertIn("Здравствуйте!", result)

if __name__ == "__main__":
    unittest.main()