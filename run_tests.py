import unittest
import json
import os
import argparse
from io import StringIO


def load_tests(loader, standard_tests, pattern):
    package_tests = loader.discover(start_dir=os.path.dirname(__file__), pattern='test_*.py')
    standard_tests.addTests(package_tests)
    return standard_tests


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run tests and update DevOS report.')
    parser.add_argument('--report', type=str, default='devos_report.json',
                        help='Path to the DevOS report JSON file')
    args = parser.parse_args()

    # Формируем путь в родительской директории
    report_path = os.path.join('..', args.report)

    # Создаём директории, если их нет
    os.makedirs(os.path.dirname(os.path.abspath(report_path)), exist_ok=True)

    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests', pattern='test_*.py')

    stream = StringIO()
    runner = unittest.TextTestRunner(stream=stream, verbosity=2)
    result = runner.run(test_suite)

    print(stream.getvalue())

    test_results = {
        "total": result.testsRun,
        "failures": len(result.failures),
        "errors": len(result.errors),
        "skipped": len(result.skipped),
        "output": stream.getvalue()
    }

    # Загружаем или создаём отчёт
    if os.path.exists(report_path):
        with open(report_path, 'r', encoding='utf-8') as f:
            report = json.load(f)
    else:
        report = {}

    # Обновляем только результаты тестов
    report['test_results'] = test_results

    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print(f"Test results updated in {report_path}")