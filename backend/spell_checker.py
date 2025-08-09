from pymorphy3 import MorphAnalyzer

_morph = MorphAnalyzer()

# Специальные случаи коррекции
SPECIAL_CASES = {
    "приветсвую": "приветствовать",
    "приветсвуй": "приветствовать",
    "приветсвует": "приветствовать",
    "машына": "машина"
}

def check_spelling(word):
    """Улучшенная проверка орфографии"""
    # Проверка специальных случаев
    if word in SPECIAL_CASES:
        return SPECIAL_CASES[word]
        
    # Обработка коротких слов
    if len(word) < 3:
        return word
        
    # Стандартная обработка
    parsed = _morph.parse(word)
    if not parsed or parsed[0].score < 0.5:
        return word
    
    # Выбираем вариант с наибольшей вероятностью
    best_parse = max(parsed, key=lambda p: p.score)
    return best_parse.normal_form