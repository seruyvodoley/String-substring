"""модуль реализующий алгоритм КМП"""


def compute_prefix(substring):
    """
    вычисляет префикс-функцию для заданной подстроки

    :param substring: подстрока, для которой нужно вычислить префикс-функцию
    :return: список, содержащий значения префикс-функции для каждой позиции в подстроке
    """
    prefix = [0] * len(substring)
    j = 0
    for i in range(1, len(substring)):
        while j > 0 and substring[i] != substring[j]:
            j = prefix[j - 1]
        if substring[i] == substring[j]:
            j += 1
        prefix[i] = j
    return prefix


class KMPSearch:
    """
    класс для реализации алгоритма Кнута-Морриса-Пратта
    """
    def __init__(self, string):
        """
        конструктор класса KMPSearch
        :param string: строка в которой будет производиться поиск
        """
        self.string = string

    def kmp(self, substring, method):
        """
        Поиск всех вхождений подстроки в строку с использованием алгоритма Кнута-Морриса-Пратта
        :param substring: Подстрока для поиска
        :param method: Направление поиска
        :return: Список индексов начала каждого вхождения подстроки в строку
        """
        prefix = compute_prefix(substring)
        matches = []
        j = 0
        i = 0

        if method == 'last':
            i = len(self.string) - 1
            substring = substring[::-1]

        while 0 <= i < len(self.string):
            while j > 0 and self.string[i] != substring[j]:
                j = prefix[j - 1]
            if self.string[i] == substring[j]:
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

    def kmp_search(self, substring, method, count):
        """
        функция реализующая поиск алгоритмом КМП
        :param substring: подстрока для поиска
        :param method: метод поиска с начала или конца
        :param count: счетчик сколько вхождений найти
        :return: кортеж из индексов подстрок
        """
        result_list = self.kmp(substring, method)

        if count > 0:
            result_list = result_list[:count]

        return tuple(result_list) if result_list else None
