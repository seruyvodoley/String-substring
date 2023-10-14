"""Модуль поиска подстроки в строке"""
import argparse
import hashlib
import time
from colorama import Fore

def time_counter(function):
    def do_time_count(*args, **kwargs):
        start = time.perf_counter()
        result_time = function(*args, **kwargs)
        stop = time.perf_counter()
        print(f'Time result - {stop - start:0.9f}')
        return result_time

    return do_time_count


def hashh(input_string):
    """
    переопределение метода hash()
    :param input_string: входная строка
    :return: хэш строки
    """
    sha256 = hashlib.sha256()
    sha256.update(input_string.encode('utf-8'))
    hash_value = sha256.hexdigest()
    return hash_value


def rabin_karp(string, substring, method, count):
    """
    Функция Рабина-Карпа
    :param string: Строка в которой буддет производиться поиск
    :param substring: Подстрока, которая будет искаться в строке
    :param method: Направление поиска подстроки в строке
    :param count: Количество вхождений подктроки в строку
    :return: Количество индексов с вхождениями подстроки в строке
    """
    string_len, substring_len = len(string), len(substring)
    result_list = []
    start, stop, step = 0, string_len - substring_len + 1, 1
    hash_substring = hashh(substring)
    if method == 'last':
        start, stop, step = len(string) - 1, 0 + len(substring) - 2, -1
        # len(string) - 1 устанавливает начальную позицию в конце строки
        # означает, что итерация будет продолжаться до позиции len(substring) - 1.
        # 0 + len(substring) - 2То есть, мы итерируемся по подстроке, и однако, чтобы включить последний символ,
        # мы вычитаем 1
        substring = ''.join(reversed(substring))
        hash_substring = hashh(substring)
    if string_len >= substring_len:
        for i in range(start, stop, step):
            if method == 'first':
                slice_stop = i + substring_len  # для извлечения подстроки
            else:
                slice_stop = i - substring_len
                if slice_stop < 0:
                    slice_stop = None
            hs = hashh(string[i:slice_stop:step])  # вычислим хэш сегмента строки
            if hs == hash_substring:
                if string[i:slice_stop:step] == substring:
                    if method == 'first':
                        result_list.append(i)
                    else:
                        result_list.append(i - substring_len + 1)
                    if len(result_list) == count:
                        return tuple(result_list)
        if not result_list:
            return None
        else:
            return tuple(result_list)
    else:
        return None


@time_counter
def search(string=None, substring=None, case_sensitivity=True,
           method='first', count=1, file_path=None):
    """
    Функция для поиска подстроки в строке при помощи функции Рабина-Карпа
    :param string: Строка в которой будет производиться поиск
    :param substring: Последовательность из подстрок или одна подстрока для поиска в строке
    :param case_sensitivity: Флаг чувствительности к регистру
    :param method: Направление поиска подстроки в строке
    :param count: Количество вхождений подстроки в строку
    :param file_path: Файл, в котором будет производиться поиск
    :return: Количество индексов с вхождениями подстроки в строке или словарь
    """
    if file_path:
        with open(file_path, 'r') as string_file:
            string = string_file.read()

    if not case_sensitivity:
        string = string.lower()
        if isinstance(substring, str):
            substring = substring.lower()
        if isinstance(substring, tuple):
            substring = tuple(string.lower() for string in substring)

    if isinstance(substring, str):
        return rabin_karp(string, substring, method, count)
    if isinstance(substring, tuple):
        substring_dict = {}
        for i in substring:
            substring_dict[i] = rabin_karp(string, i, method, count)
        return substring_dict


def main():
    parser = argparse.ArgumentParser(description='Алгоритм Рабина-Карпа')
    parser.add_argument('-string', type=str, help='Строка для поиска')
    parser.add_argument('-substr', type=str, help='Подстрока или кортеж подстрок для поиска', nargs='*')
    parser.add_argument('-case_sensitivity', type=bool, help='Чувствительность к регистру', default=False)
    parser.add_argument('-method', type=str, help='Направление поиска подстроки в строке', default='first')
    parser.add_argument('-count', type=int, help='Количество вхождений подстроки в строку', default=1)
    parser.add_argument('-file_path', type=str, help='Файл, в котором будет производиться поиск строки', default=None)
    args = parser.parse_args()

    if isinstance(args.substr, list):
        if len(args.substr) < 2:
            args.substr = args.substr[0]
        else:
            args.substr = tuple(args.substr)

    if args.file_path:
        with open(args.file_path, 'r') as file:
            lines = file.readlines()[:10]
            string = "".join(lines)
    else:
        string = args.string

    results = search(string=string, substring=args.substr, case_sensitivity=args.case_sensitivity,
                     method=args.method, count=args.count, file_path=args.file_path)
    if isinstance(results, dict):
        print(f'Строка: {string}')
        print(f'Подстроки: {str(args.substr)}')
        print('Результат:')

        for key, value in results.items():
            if value:
                print(f"'{key}': {value}")
                if len(value) > 10:
                    print(f'Первые 10 индексов: {value[:10]}')
            else:
                print(f"'{key}': Not Found")
    else:
        print(f'Строка: {string}')
        print(f'Подстрока(и): {str(args.substr)}')
        print(f'Результат: {results}')
        if results and len(results) > 10:
            print(f'Первые 10 индексов: {results[:10]}')


if __name__ == '__main__':
    # colorama.init()
    main()
