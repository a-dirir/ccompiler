from lexical.automata import Automata
from lexical.specs import specs


specifications = [[specs[i], specs[i+1]] for i in range(0, len(specs), 2)]
aut = Automata(specifications)


def run(code: str):
    while len(code) != 0:
        match = aut.match(code)
        if match is None:
            print('Error')
            break
        else:
            if match['type'] == 'IDENTIFIER' or match['type'] == 'NUMBER':
                code = code[match['index']-1:]
            else:
                code = code[match['index']:]

            print(match)

