#!/usr/bin/env python3
"""Скрипт запуска тестов с автоматической активацией venv"""

import os
import sys
import argparse
import unittest
import json
import traceback
from datetime import datetime

# Проверка и активация venv
VENV_ACTIVATED = os.getenv('VIRTUAL_ENV') is not None

if not VENV_ACTIVATED:
    print("Активация виртуального окружения...")
    project_dir = os.path.dirname(os.path.abspath(__file__))
    venv_dir = os.path.join(project_dir, "venv")

    if os.path.exists(venv_dir):
        if sys.platform == "win32":
            activate_script = os.path.join(venv_dir, "Scripts", "activate.bat")
            os.system(f"{activate_script} && python {' '.join(sys.argv)}")
        else:
            activate_script = os.path.join(venv_dir, "bin", "activate")
            os.system(f"source {activate_script} && python {' '.join(sys.argv)}")
        sys.exit(0)
    else:
        print("Ошибка: venv не найден в проекте!")
        sys.exit(1)

# Обновление зависимостей
print("Обновление зависимостей...")
os.system("pip install -r requirements.txt")


# Функция для сохранения результатов тестов
def save_test_results(results, file_path="devos_report.json"):
    try:
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                report = json.load(f)
        else:
            report = {}

        report.setdefault("test_history", []).append({
            "timestamp": datetime.now().isoformat(),
            "results": results
        })

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Ошибка сохранения отчёта: {str(e)}")


# Запуск тестов
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run project tests')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    parser.add_argument('-p', '--parallel', type=int, default=1, help='Number of parallel processes')
    args = parser.parse_args()

    # Настройка параллельного запуска
    test_runner = unittest.TextTestRunner(verbosity=2 if args.verbose else 1)
    
    if args.parallel > 1:
        try:
            from concurrencytest import ConcurrentTestSuite, fork_for_tests
            loader = unittest.TestLoader()
            suite = loader.discover('tests')
            concurrent_suite = ConcurrentTestSuite(suite, fork_for_tests(args.parallel))
            result = test_runner.run(concurrent_suite)
        except ImportError:
            print("Для параллельного запуска установите concurrencytest: pip install concurrencytest")
            sys.exit(1)
    else:
        loader = unittest.TestLoader()
        suite = loader.discover('tests')
        result = test_runner.run(suite)
    
    test_results = {
        "tests_run": result.testsRun,
        "errors": [{"test": str(t[0]), "traceback": t[1]} for t in result.errors],
        "failures": [{"test": str(t[0]), "traceback": t[1]} for t in result.failures],
        "successful": result.testsRun - len(result.errors) - len(result.failures)
    }

    save_test_results(test_results)
    print(f"Тестов выполнено: {test_results['tests_run']}")
    print(f"Успешных: {test_results['successful']}")
    print(f"Ошибок: {len(test_results['errors'])}")
    print(f"Сбоев: {len(test_results['failures'])}")

    if test_results["errors"] or test_results["failures"]:
        sys.exit(1)