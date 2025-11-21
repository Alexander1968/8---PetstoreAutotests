import sys
import os
from datetime import datetime
from bs4 import BeautifulSoup


def translate_with_bs4(html_content):
    """
    Более точный перевод с использованием BeautifulSoup
    """
    soup = BeautifulSoup(html_content, 'html.parser')

    translation_dict = {
        'test_report.html': 'ОтчетПоТестам.html',
        'Report generated on': 'Отчет создан',
        'by': 'с помощью',
        'Environment': 'Окружение',
        'Summary': 'Сводка',
        'tests took': 'тестов заняло',
        '(Un)check the boxes to filter the results.': '(Снимите)установите флажки для фильтрации результатов.',
        'There are still tests running.': 'Некоторые тесты все еще выполняются.',
        'Reload this page to get the latest results!': 'Перезагрузите страницу для получения актуальных результатов!',
        'Result': 'Результат',
        'Test': 'Тест',
        'Duration': 'Длительность',
        'Links': 'Ссылки',
        'Show all details': 'Показать все детали',
        'Hide all details': 'Скрыть все детали',
        'No results found. Check the filters.': 'Результаты не найдены. Проверьте фильтры.',
        'No log output captured.': 'Логи не записаны.',
        'Passed': 'Пройдено',
        'Failed': 'Не пройдено',
        'Skipped': 'Пропущено',
        'Error': 'Ошибка',
        'Expected failures': 'Ожидаемые сбои',
        'Unexpected passes': 'Неожиданные прохождения',
        'Reruns': 'Перезапуски',
        'Failed,': 'Не пройдено,',
        'Passed,': 'Пройдено,',
        'Skipped,': 'Пропущено,',
        'Expected failures,': 'Ожидаемые сбои,',
        'Unexpected passes,': 'Неожиданные прохождения,',
        'Errors,': 'Ошибки,',
        'Reruns': 'Перезапуски',
        'expand [+]': 'развернуть [+]',
        'collapse [-]': 'свернуть [-]',
        'hide details': 'скрыть детали',
        'show details': 'показать детали'
    }

    def translate_text_nodes(element):
        if element.name in ['script', 'style']:
            return

        if hasattr(element, 'children'):
            for child in element.children:
                if child.name:
                    translate_text_nodes(child)
                else:
                    if child.string:
                        original_text = child.string
                        translated_text = original_text
                        for eng, rus in translation_dict.items():
                            translated_text = translated_text.replace(eng, rus)
                        if translated_text != original_text:
                            child.string.replace_with(translated_text)

    translate_text_nodes(soup)

    return str(soup)


def process_html_file(input_file_path, output_dir=None):
    """
    Обрабатывает HTML файл и создает переведенную версию
    """
    try:
        # Читаем исходный файл
        with open(input_file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()

        # Переводим содержимое
        translated_html = translate_with_bs4(html_content)

        # Генерируем имя для нового файла
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = os.path.splitext(os.path.basename(input_file_path))[0]
        new_filename = f"{base_name}_russian_{timestamp}.html"

        # Определяем путь для сохранения
        if output_dir:
            output_path = os.path.join(output_dir, new_filename)
        else:
            output_path = os.path.join(os.path.dirname(input_file_path), new_filename)

        # Сохраняем переведенный файл
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(translated_html)

        print(f"Переведенный отчет сохранен как: {output_path}")
        return output_path

    except Exception as e:
        print(f"Ошибка при обработке файла: {e}")
        return None


# Основная программа
if __name__ == "__main__":
    # if len(sys.argv) < 2:
    #     print("Использование: python script.py <input_file> [output_directory]")
    #     print("Пример: python script.py test_report.html")
    #     print("Пример: python script.py test_report.html ./output")
    #     sys.exit(1)

    #input_file = sys.argv[1]
    input_file = "test_report.html"
    #output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    output_dir = os.getcwd()

    if not os.path.exists(input_file):
        print(f"Файл {input_file} не найден")
        sys.exit(1)

    process_html_file(input_file, output_dir)

    # # Основная программа
    # if __name__ == "__main__":
    #     if len(sys.argv) < 2:
    #         print("Использование: python script.py <input_file> [output_directory]")
    #         print("Пример: python script.py test_report.html")
    #         print("Пример: python script.py test_report.html ./output")
    #         sys.exit(1)
    #
    #     # input_file = sys.argv[1]
    #     input_file = "test_report.html"
    #     output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    #
    #     if not os.path.exists(input_file):
    #         print(f"Файл {input_file} не найден")
    #         sys.exit(1)
    #
    #     process_html_file(input_file, output_dir)