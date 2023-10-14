"""Модуль поиска подстроки в строке"""
import argparse
import time
from colorama import Fore, Style


def time_counter(function):
    """
    декоратор, который измеряет и выводит время выполнения функции

    Args:
        function (callable): функция, время выполнения которой будет измерено

    Returns:
        callable: обернутая функция, которая измеряет время выполнения и возвращает результат

    Example:
        @time_counter
        def my_function():
            # Какой-то код
            pass

        my_function()  # вызов функции с измерением времени выполнения
    """
    def do_time_count(*args, **kwargs):
        start = time.perf_counter()
        result_time = function(*args, **kwargs)
        stop = time.perf_counter()
        print(f'Time result - {stop - start:0.9f}')
        return result_time

    return do_time_count


def kmp_search(string, substring, method, count):
    """
    функция поиска алгоритма Кнута-Морриса-Пратта
    :param string: строка для поиска
    :param substring: искомая подстрока
    :param method: направление поиска
    :param count: количество искомых подстрок
    :return: кортеж с индексами начала подстрок
    """
    def compute_prefix(pattern):
        prefix = [0] * len(pattern)
        j = 0
        for i in range(1, len(pattern)):
            while j > 0 and pattern[i] != pattern[j]:
                j = prefix[j - 1]
            if pattern[i] == pattern[j]:
                j += 1
            prefix[i] = j
        return prefix

    def kmp(string, substring):
        prefix = compute_prefix(substring)
        matches = []
        j = 0
        i = 0

        if method == 'last':
            i = len(string) - 1
            substring = substring[::-1]

        while 0 <= i < len(string):
            while j > 0 and string[i] != substring[j]:
                j = prefix[j - 1]
            if string[i] == substring[j]:
                j += 1
            if j == len(substring):
                if method == 'last':
                    matches.append(i)
                else:
                    matches.append(i - len(substring) + 1)
                j = prefix[j - 1]
            if method == 'last':
                i -= 1
            else:
                i += 1

        return matches

    result_list = kmp(string, substring)

    if count > 0:
        result_list = result_list[:count]

    return tuple(result_list) if result_list else None


@time_counter
def search(string=None, substring=None, case_sensitivity=True,
           method='first', count=1, file_path=None):
    """
    обертка для функции поиска алгоритмом Кнутта-Морриса-Пратта
    :param string: строка в которой будет производиться поиск
    :param substring: подстрока для поиска в строке
    :param case_sensitivity: флаг чувствительности к регистру
    :param method: направление поиска подстроки в строке
    :param count: количество вхождений подстроки в строку
    :param file_path: файл, в котором будет производиться поиск
    :return: количество индексов с вхождениями подстроки в строке или словарь
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
        return kmp_search(string, substring, method, count)
    if isinstance(substring, tuple):
        substring_dict = {}
        for i in substring:
            substring_dict[i] = kmp_search(string, i, method, count)
        return substring_dict


def highlight_substrings(string, indicies, color_map):
    # Функция для подсветки подстрок в строке
    stack = []
    for i in range(len(string)):
        if indicies.get(i) is not None:
            for el in indicies[i]:
                stack.append((i, el))

        if len(stack) == 0:
            print(Style.RESET_ALL, end='')
            print(string[i], end='')
        else:
            print(color_map[stack[-1][1]] + string[i], end='')

        while len(stack) != 0 and i - stack[-1][0] >= len(stack[-1][1]) - 1:
            stack.pop()

    print(Style.RESET_ALL)

def colored_string(results):
    colors = [Fore.RED, Fore.MAGENTA, Fore.BLUE, Fore.YELLOW, Fore.GREEN]
    color_map = {}
    idx = 0

    positions = {}
    for k, v in results.items():
        color_map[k] = colors[idx]
        idx += 1
        if idx == len(colors):
            idx = 0

        if v:
            for i in v:
                if positions.get(i) is None:
                    positions[i] = []
                positions[i].append(k)
    return positions, color_map

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
            lines = file.readlines()
            string = "".join(lines)
    else:
        string = args.string

    result = search(string=string, substring=args.substr, case_sensitivity=args.case_sensitivity,
                    method=args.method, count=args.count, file_path=args.file_path)

    # Ограничение на вывод первых 10 строк файла
    print_string = '\n'.join(string.split('\n')[:10])

    if isinstance(result, dict):
        positions, color_map = colored_string(result)

        highlight_substrings(print_string, positions, color_map)
        print(f'Подстроки: {str(args.substr)}')
        print('Результат:')
        for key, value in result.items():
            if value:
                print(f"'{key}': {value}")
            else:
                print(f"'{key}': Not Found")

    else:
        positions, color_map = colored_string({'Result': result})
        highlight_substrings(print_string, positions, color_map)
        print(f'Подстрока(и): {str(args.substr)}')
        print(f'Результат: {result}')


if __name__ == '__main__':
    main()

