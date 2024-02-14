# Импорт необходимых библиотек
import csv
from datetime import datetime

# Путь к исходному файлу данных
input_file_path = 'C:/Users/user/PycharmProjects/Nastya/1/scientist.txt'
output_file_path = 'C:/Users/user/PycharmProjects/Nastya/1/scientist_origin.txt'


def read_data_with_header_check(file_path):
    """
    Читает данные из файла, исключая заголовок, и возвращает список словарей с информацией о препаратах.

    Аргументы:
    file_path: строка, путь к файлу с данными.

    Возвращает:
    data: список словарей, каждый из которых содержит информацию об ученом, препарате, дате и компонентах.
    """
    data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split('#')
            if len(parts) == 4 and parts[2] != 'date':
                data.append({
                    'ScientistName': parts[0],
                    'Preparation': parts[1],
                    'Date': parts[2],
                    'Components': parts[3]
                })
    return data


def find_original_preparations_fixed(data):
    """
    Определяет оригинальные препараты, исключая дубликаты с позднейшими датами, с корректным сравнением дат.

    Аргументы:
    data: список словарей с информацией о препаратах.

    Возвращает:
    Список словарей, содержащий информацию только об оригинальных препаратах.
    """
    preparations = {}
    for entry in data:
        prep_name = entry['Preparation']
        prep_date = datetime.strptime(entry['Date'], '%Y-%m-%d')  # Преобразование строки в datetime
        if prep_name not in preparations or prep_date < datetime.strptime(preparations[prep_name]['Date'], '%Y-%m-%d'):
            preparations[prep_name] = entry
    return list(preparations.values())


def write_data(file_path, data):
    """
    Записывает данные в файл.

    Аргументы:
    file_path: строка, путь к файлу для записи.
    data: список словарей с информацией для записи.
    """
    with open(file_path, 'w', encoding='utf-8') as file:
        for entry in data:
            file.write(
                '#'.join([entry['ScientistName'], entry['Preparation'], entry['Date'], entry['Components']]) + '\n')


def find_allopurinol_accomplices(data):
    """
    Находит всех разработчиков Аллопуринола, кроме оригинального, и сортирует по дате.

    Аргументы:
    data: список словарей с информацией о препаратах.

    Возвращает:
    accomplices: список словарей с информацией о подельниках.
    original: словарь с информацией об оригинальном разработчике.
    """
    allopurinol_entries = [entry for entry in data if entry['Preparation'] == 'Аллопуринол']
    allopurinol_entries.sort(key=lambda x: datetime.strptime(x['Date'], '%Y-%m-%d'))
    original = allopurinol_entries[0]
    accomplices = allopurinol_entries[1:]
    return accomplices, original


# Основной блок выполнения
data = read_data_with_header_check(input_file_path)
original_preparations_fixed = find_original_preparations_fixed(data)
write_data(output_file_path, original_preparations_fixed)

accomplices, original = find_allopurinol_accomplices(data)

# Формирование итогового отчета по Аллопуринолу
allopurinol_report_fixed = f"Разработчиками Аллопуринола были такие люди (результаты выведены в порядке возрастания даты):\n"
for accomplice in accomplices:
    allopurinol_report_fixed += f"{accomplice['ScientistName']} - {accomplice['Date']}\n"
allopurinol_report_fixed += f"Оригинальный рецепт принадлежит: {original['ScientistName']}"
