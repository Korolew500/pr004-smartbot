# pr004-smartbot

Проект интеллектуального бота

## Структура проекта

- `main.py` - Главный запускаемый файл
- `backend/` - Модули обработки сообщений
- `frontend/` - Интерфейсы взаимодействия
- `data/` - Файлы данных (синонимы, ключевые слова)
- `tests/` - Тесты

## Первый запуск

1. Создайте виртуальное окружение:
```bash
python -m venv venv
```

2. Активируйте окружение:
```bash
# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Запустите бота:
```bash
python main.py
```

## Запуск тестов
```bash
python run_tests.py
```

⚠️ Важно: Скрипт run_tests.py автоматически активирует venv