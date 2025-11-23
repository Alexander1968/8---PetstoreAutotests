import sys
import os
from datetime import datetime
from bs4 import BeautifulSoup
import json
import html


def translate_with_bs4(html_content):
    """
    Полный перевод с обработкой всех элементов
    """
    soup = BeautifulSoup(html_content, 'html.parser')

    translation_dict = {
        'test_report.html': 'Отчет по тестам',
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

    # 1. Обрабатываем основной текст
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

    # 2. Обрабатываем JSON данные в data-jsonblob
    data_container = soup.find('div', id='data-container')
    if data_container and 'data-jsonblob' in data_container.attrs:
        try:
            # Декодируем HTML entities и парсим JSON
            json_str = html.unescape(data_container['data-jsonblob'])
            data = json.loads(json_str)

            # Рекурсивно переводим статусы в JSON
            def translate_json(obj):
                if isinstance(obj, dict):
                    for key, value in obj.items():
                        if key == 'result' and isinstance(value, str):
                            # Перевод основных статусов
                            if value == 'Passed':
                                obj[key] = 'Пройдено'
                            elif value == 'Failed':
                                obj[key] = 'Не пройдено'
                            elif value == 'Skipped':
                                obj[key] = 'Пропущено'
                            elif value == 'Error':
                                obj[key] = 'Ошибка'
                        elif key == 'resultsTableRow' and isinstance(value, list):
                            # Обрабатываем HTML в resultsTableRow
                            for i, html_string in enumerate(value):
                                if 'Passed' in html_string:
                                    value[i] = html_string.replace('>Passed<', '>Пройдено<')
                                if 'Failed' in html_string:
                                    value[i] = html_string.replace('>Failed<', '>Не пройдено<')
                                if 'Skipped' in html_string:
                                    value[i] = html_string.replace('>Skipped<', '>Пропущено<')
                                if 'Error' in html_string:
                                    value[i] = html_string.replace('>Error<', '>Ошибка<')
                        elif key == 'renderCollapsed' and isinstance(value, list):
                            # Оставляем английским для JS логики
                            pass
                        elif key == 'title' and isinstance(value, str):
                            # Обновляем заголовок
                            if value == 'test_report.html':
                                obj[key] = 'отчет_тестов.html'
                        elif isinstance(value, (dict, list)):
                            translate_json(value)
                elif isinstance(obj, list):
                    for item in obj:
                        if isinstance(item, (dict, list)):
                            translate_json(item)

            translate_json(data)

            # Кодируем обратно и устанавливаем атрибут
            translated_json = json.dumps(data, ensure_ascii=False)
            data_container['data-jsonblob'] = html.escape(translated_json)

        except json.JSONDecodeError as e:
            print(f"Ошибка при обработке JSON: {e}")

    # 3. Обрабатываем шаблоны
    templates = soup.find_all('template')
    for template in templates:
        template_content = str(template)
        translated_content = template_content
        for eng, rus in translation_dict.items():
            translated_content = translated_content.replace(eng, rus)
        if translated_content != template_content:
            template.replace_with(BeautifulSoup(translated_content, 'html.parser').template)

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

    #input_file = sys.argv[1]
    input_file = "test_report.html"
    #output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    output_dir = os.getcwd()

    if not os.path.exists(input_file):
        print(f"Файл {input_file} не найден")
        sys.exit(1)

    process_html_file(input_file, output_dir)