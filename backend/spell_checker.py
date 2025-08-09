from pymorphy3 import MorphAnalyzer

# Загрузка словаря (остальной код без изменений)
_morph = MorphAnalyzer()

def check_spelling(word):
    """Проверка орфографии и возврат нормальной формы"""
    parsed = _morph.parse(word)
    if not parsed or parsed[0].score < 0.5:
        return None
    return parsed[0].normal_form