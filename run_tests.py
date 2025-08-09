#!/usr/bin/env python3
"""Обновленный скрипт запуска тестов"""

import argparse
import unittest

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run project tests')
    parser.add_argument('--report', help='Generate test report')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    loader = unittest.TestLoader()
    suite = loader.discover('tests')
    
    runner = unittest.TextTestRunner(verbosity=2 if args.verbose else 1)
    result = runner.run(suite)
    
    if args.report:
        with open(args.report, 'w') as f:
            f.write(f"Tests run: {result.testsRun}\n")
            f.write(f"Failures: {len(result.failures)}\n")
            f.write(f"Errors: {len(result.errors)}\n")