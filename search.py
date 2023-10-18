"""Модуль поиска подстроки в строке с помощью алгоритма КМП"""
import argparse
import time
from colorama import Fore, Style
from kmp_search import KMPSearch


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
        """
        Измеряет время выполнения функции и возвращает результат и время выполнения
        :param function: Функция, время выполнения которой нужно измерить
        :param args: Позиционные аргументы, передаваемые в функцию
        :param kwargs: Именованные аргументы, передаваемые в функцию
        :return: Результат выполнения функции и время выполнения в секундах (с точностью до 9 знаков)
        """
        start = time.perf_counter()
        result_time = function(*args, **kwargs)
        stop = time.perf_counter()
        print(f'Time result - {stop - start:0.9f}')
        return result_time

    return do_time_count


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
    searcher = KMPSearch(string)
    if isinstance(substring, str):
        return searcher.kmp_search(substring, method, count)
    if isinstance(substring, tuple):
        substring_dict = {}
        for i in substring:
            substring_dict[i] = searcher.kmp_search(i, method, count)
        return substring_dict


def highlight_substrings(string, indicies, color_map):
    """
    функция для подсветки подстрок в строке
    :param string: исходная строка
    :param indicies: словарь с индексами для подсветки
    :param color_map: набор цветов из которых выберется подсветка
    :return: None
    """
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
    """
    функция для создания информации о подсветке подстрок
    :param results: словарь с ключами - названия подстрок, а значения - списки индексов
    :return: кортеж из двух словарей
             positions: ключи - индексы символов в строке, значения - списки названий подстрок,
                        начинающихся в данной позиции.
            color_map: ключи - названия подстрок, значения - соответствующие ANSI-цвета для подсветки
    """
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
    """
    функция реализующая консольную обертку
    :return: None
    """
    parser = argparse.ArgumentParser(description='Алгоритм Рабина-Карпа')
    parser.add_argument('-string', type=str, help='Строка для поиска')
    parser.add_argument('-substr', type=str, help='Подстрока или кортеж подстрок для поиска', nargs='*')
    parser.add_argument('-case_sensitivity', type=bool, help='Чувствительность к регистру', default=False)
    parser.add_argument('-method', type=str, help='Направление поиска подстроки в строке', default='first')
    parser.add_argument('-count', type=int, help='Количество вхождений подстроки в строку', default=1)
    parser.add_argument('-file_path', type=str, help='Файл, в котором будет производиться поиск строки', default=None)
    args = parser.parse_args()

    # Преобразовать args.substr в кортеж, даже если это строка
    args.substr = tuple(args.substr) if args.substr else tuple()

    # Загрузить строку из файла, если указан файл
    if args.file_path:
        with open(args.file_path, 'r') as file:
            lines = file.readlines()
            string = "".join(lines)
    else:
        string = args.string

    result = search(
        string=string,
        substring=args.substr,
        case_sensitivity=args.case_sensitivity,
        method=args.method,
        count=args.count,
        file_path=args.file_path
    )

    # Ограничение на вывод первых 10 строк файла
    print_string = '\n'.join(string.split('\n')[:10])

    if isinstance(result, dict):
        positions, color_map = colored_string(result)
    else:
        positions, color_map = colored_string({args.substr: result})

    highlight_substrings(print_string, positions, color_map)
    print(f'Подстрока(и): {str(args.substr)}')
    print('Результат:')

    if isinstance(result, dict):
        for key, value in result.items():
            if value:
                print(f"'{key}': {value}")
            else:
                print(f"'{key}': Не нашель")
    else:
        print(f'Результат: {result}')


if __name__ == '__main__':
    main()
