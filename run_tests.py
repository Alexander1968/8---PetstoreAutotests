#!/usr/bin/env python3
"""
Скрипт для запуска автотестов PetStore API
"""

import pytest
import sys
import os

from translate_to_ru_v3 import process_html_file


# Основная функция для запуска тестов
def main():

    print("Запуск автотестов для PetStore API...")

    # Добавляем путь к проекту в PYTHONPATH
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

    # Аргументы для pytest
    pytest_args = [
        "tests/",
        "-v",  # Подробный вывод
        "--tb=short",  # Короткий traceback
        "--html=test_report.html",  # Генерация HTML отчета
        "--self-contained-html",
        "-s"  # Вывод print statements
    ]

    # Запуск тестов
    exit_code = pytest.main(pytest_args)

    if exit_code == 0:
        print("\n🎉 Все тесты прошли успешно!")
    else:
        print(f"\n❌ Некоторые тесты не прошли. Код выхода: {exit_code}")

    print("\n📊 Отчет сохранен в файле: test_report.html")

    input_file = "test_report.html"

    if not os.path.exists(input_file):
        print(f"Файл {input_file} не найден")
        sys.exit(1)

    process_html_file(input_file)

    return exit_code


if __name__ == "__main__":
    main()