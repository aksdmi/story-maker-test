import argparse

from typing import Optional

from positions import list_of_strings_positions
from strings import list_of_strings, stop_words


class TextFormatter:
    def __init__(self, strings: list, positions: list, stop_words: Optional[list] = None):
        self.strings = strings
        self.positions = positions
        self.stop_words = stop_words if stop_words else []

    def get_tuples(self, pos_list, par_index):
        for i, elm in enumerate(pos_list):
            if isinstance(elm, list):
                yield from self.get_tuples(elm, i)
            else:
                if par_index:
                    yield par_index, elm
                else:
                    yield i, elm


    def check_and_replace(self, cstr : str):
        if '{username}' in cstr:
            return self.username
        else:
            return cstr

    def get_as_list(self, username: str) -> list:
        """
        Метод возвращает правильно сформированный список слов итогового текста.
        Среди возвращаемых элементов не должно содержаться слов из списка стоп-слов.
        Элементы списка, содержащие шаблон {username}, должны быть заменены на значение переменной username.
        :param username: Имя пользователя
        :return: Список слов в правильном порядке
        """
        self.username = username
        pre_strings = [self.strings[i] for i, _ in sorted(self.get_tuples(self.positions, None), key=lambda x: x[1])
                                                                                    if self.strings[i] not in self.stop_words]
        return list(map(self.check_and_replace, pre_strings))



    def get_as_text(self, username: str) -> str:
        """
        Метод возвращает текст, сформированный из списка слов и позиций.
        В возвращаемом тексте не должно быть стоп-слов.
        Шаблон {username} должен быть заменён на значение переменной username.
        Каждое новое предложение должно начинаться с большой буквы.
        Между знаком препинания и впереди стоящим словом не должно быть пробелов.
        :param username: Имя пользователя
        :return: Текст, отформатированный согласно условиям задачи
        """
        
        strlist = self.get_as_list(username)

        if not strlist:
            return ''

        was_sign = False
        
        stop_signs = ('.', '!', '?')

        strlist[0] = strlist[0].title()

        for i in range(1, len(strlist)):
            mstr = strlist[i]
        
            if mstr in stop_signs:
                was_sign = True
            elif was_sign:
                strlist[i] = ' ' + mstr.title()
                was_sign = False
            elif mstr != ',':
                strlist[i] = ' ' + mstr
        
        return ''.join(strlist)


formatter = TextFormatter(list_of_strings, list_of_strings_positions, stop_words)

arguments_parser = argparse.ArgumentParser(prog="python3 main.py", description="Консольный рассказчик.")
arguments_parser.add_argument('-u',
                              '--username',
                              action='store',
                              help='Имя пользователя в истории')

arguments = arguments_parser.parse_args()

if arguments.username:
    print(formatter.get_as_text(arguments.username))
    
