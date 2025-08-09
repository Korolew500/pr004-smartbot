import unittest
from backend.keyword_processor import ResponsePrioritizer

class TestResponsePrioritizer(unittest.TestCase):
    def test_priority_ordering(self):
        """Тест правильного порядка приоритетов"""
        responses = [
            {"type": "product", "text": "Товар 1"},
            {"type": "greeting", "text": "Привет"},
            {"type": "delivery", "text": "Доставка"}
        ]
        
        prioritizer = ResponsePrioritizer()
        sorted_responses = prioritizer.sort_responses(responses)
        
        self.assertEqual(sorted_responses[0]["type"], "greeting")
        self.assertEqual(sorted_responses[1]["type"], "product")
        self.assertEqual(sorted_responses[2]["type"], "delivery")

    def test_mixed_types(self):
        """Тест смешанных типов ответов"""
        responses = [
            {"type": "other", "text": "Другое"},
            {"type": "payment", "text": "Оплата"},
            {"type": "greeting", "text": "Привет"}
        ]
        
        prioritizer = ResponsePrioritizer()
        sorted_responses = prioritizer.sort_responses(responses)
        
        self.assertEqual(sorted_responses[0]["type"], "greeting")
        self.assertEqual(sorted_responses[1]["type"], "payment")
        self.assertEqual(sorted_responses[2]["type"], "other")

if __name__ == '__main__':
    unittest.main()