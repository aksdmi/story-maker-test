import argparse

from typing import Optional

from positions import list_of_strings_positions
from strings import list_of_strings, stop_words


class TextFormatter:
    def __init__(self, strings: list, positions: list, stop_words: Optional[list] = None):
        self.strings = strings
        self.positions = positions
        self.stop_words = stop_words if stop_words else []


               

    def get_as_list(self, username: str) -> list:
        """
        Метод возвращает правильно сформированный список слов итогового текста.
        Среди возвращаемых элементов не должно содержаться слов из списка стоп-слов.
        Элементы списка, содержащие шаблон {username}, должны быть заменены на значение переменной username.
        :param username: Имя пользователя
        :return: Список слов в правильном порядке
        """
        resdict = {}
        for i in range(len(self.positions)):
            val = self.positions[i]
            val2 = self.strings[i]
            
            if val2 in self.stop_words:
                continue

            if val2 == "{username}":
                val2 = username


            if isinstance(val, list):
                for j in range(len(val)):
                    resdict[val[j]] = val2    
            else:
                # reslist.insert(val, self.strings[i])
                resdict[val] = val2
        
        # for x in sorted(resdict.keys()):
        #     print(resdict[x])


        return [resdict[x] for x in sorted(resdict.keys())]



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

        was_sign = False
        was_dot = False

        stop_signs = ('.', '!', '?', ',')

        strlist2 = []

        if not strlist:
            return ''

        first = True

        for mstr in strlist:
            if mstr in stop_signs:
                was_sign = True
                if mstr == '.':
                    was_dot = True
                strlist2.append(mstr)
            elif was_sign:
                if was_dot:
                    strlist2.append(f' {mstr.title()}')
                    was_dot = False
                else:
                    strlist2.append(mstr)
                    was_sign = False
            else:
                if first:
                    strlist2.append(mstr.title())
                    first = False
                else:
                    strlist2.append(mstr)
        
        return ' '.join(strlist2)


formatter = TextFormatter(list_of_strings, list_of_strings_positions, stop_words)

# print(formatter.get_as_list('Dima'))
print(formatter.get_as_text('Dima'))


arguments_parser = argparse.ArgumentParser(prog="python3 main.py", description="Консольный рассказчик.")
arguments_parser.add_argument('-u',
                              '--username',
                              action='store',
                              help='Имя пользователя в истории')

arguments = arguments_parser.parse_args()

if arguments.username:
    print(formatter.get_as_text(arguments.username))
    
