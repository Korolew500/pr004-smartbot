"""Модуль для улучшения естественности ответов"""
import random


def add_context(response, context):
    """Добавляет контекстные фразы к ответу"""
    connectors = {
        "question": ["Кстати, ", "К вашему сведению, "],
        "info": ["Заметил, что ", "Интересно, что "],
        "action": ["Между прочим, ", "Советую учесть, "]
    }
    return random.choice(connectors[context]) + response