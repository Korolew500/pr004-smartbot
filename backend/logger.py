import logging
import os
from pathlib import Path

def setup_logger(name, log_file='bot.log', level=logging.INFO):
    """Настройка логгера"""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Создаем папку для логов
    Path('logs').mkdir(exist_ok=True)
    
    # Форматирование
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
    
    # Файловый обработчик
    file_handler = logging.FileHandler(os.path.join('logs', log_file))
    file_handler.setFormatter(formatter)
    
    # Консольный обработчик
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger