import os
import logging
import re  # Добавлен импорт модуля re
from .keyword_processor import KeywordProcessor
from .spell_checker import SpellChecker
from .synonym_mapper import SynonymMapper

class Backend:
    def __init__(self):
        self.keyword_processor = KeywordProcessor()
        self.spell_checker = SpellChecker()
        self.synonym_mapper = SynonymMapper()
        self.logger = logging.getLogger('backend')
        self.stop_words = self.load_stop_words()  # Загрузка стоп-слов

    def load_stop_words(self):
        # Загрузка стоп-слов из файла
        stop_words_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'stop_words.txt')
        stop_words = set()
        try:
            with open(stop_words_path, 'r', encoding='utf-8') as f:
                for line in f:
                    word = line.strip()
                    if word:
                        stop_words.add(word)
        except FileNotFoundError:
            self.logger.error("Файл стоп-слов не найден")
        return stop_words

    def process_message(self, message):
        try:
            # Логирование исходного сообщения
            self.logger.info(f"Обработка сообщения: {message}")
            
            # Удаление пунктуации и приведение к нижнему регистру
            clean_msg = re.sub(r'[^\w\s]', '', message).lower()
            
            # Удаление стоп-слов
            clean_msg = ' '.join([word for word in clean_msg.split() if word not in self.stop_words])
            
            # Исправление орфографии
            corrected = self.spell_checker.correct_text(clean_msg)
            if corrected != clean_msg:
                self.logger.info(f"Исправлено: '{clean_msg}' -> '{corrected}'")
            
            # Нормализация текста (приведение к базовой форме)
            normalized = self.synonym_mapper.map_to_base(corrected)
            
            # Извлечение ВСЕХ ключевых слов
            keywords = self.keyword_processor.extract_keywords(normalized)
            
            # Сбор ВСЕХ ответов
            responses = []
            for keyword in keywords:
                if keyword in self.keyword_processor.keywords:
                    data = self.keyword_processor.keywords[keyword]
                    # Поддержка старого (response) и нового формата (responses)
                    if 'responses' in data:
                        responses.extend(data['responses'])
                    elif 'response' in data:
                        responses.append(data['response'])
            
            # Формирование составного ответа
            if responses:
                # Удаление дубликатов и склейка
                return " ".join(dict.fromkeys(responses))
            else:
                return "Извините, я не понял вопрос. Можете переформулировать?"
                
        except Exception as e:
            self.logger.error(f"Ошибка обработки: {str(e)}", exc_info=True)
            return "Произошла внутренняя ошибка. Пожалуйста, повторите позже."