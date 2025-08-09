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
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Запустите бота в консольном режиме:
```bash
python main.py
```

4. Для выхода введите "exit"

## Запуск тестов
```bash
python run_tests.py
```