import re

class UrlFilter:

    def __init__(self):
        pass

    #TODO: Implementar reglas para filtrar macro_ids y usar expresiones regulares para asignar una url sin filtrar
    #      al macro estado correspondiente.

if __name__ == '__main__':
    macrostate1 = '(http://)?nosfuimos.cl/search-ride'
    p = re.compile(macrostate1)
    m = p.match('http://nosfuimos.cl/search-ride?field_starting_from_value=Santiago%2C+Chile&field_going_to_value=Universidad+de+la+Serena%2C+Santiago%2C+Chile undefin')
    if m:
        print("Match found: "+ m.group())
    else:
        print("No Match")

    m = p.match('nosfuimos.cl/search-ride?field_starting_from_value=Sanasdasago%2C+Chile&field_going_to_value=Universidad+de+la+Serena%2C+Santiago%2C+Chile undefin')
    if m:
        print("Match found: " + m.group())
    else:
        print("No Match")
