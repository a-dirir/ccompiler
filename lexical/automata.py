from lexical.state import State


class Automata:
    def __init__(self, patterns: list):
        self.states = []
        self.start_state = State('q0', ['START'], 'START')
        self.identifier_start_state = State('q0', ['IDENTIFIER'], 'IDENTIFIER')
        self.states.append(self.start_state)
        self.states.append(self.identifier_start_state)

        self.create_machines(patterns)

    def create_machines(self, patterns):
        for pattern in patterns:
            self.create_machine(pattern)

        self.add_string_matching_state()
        self.add_char_matching_state()
        self.add_number_matching_state()
        self.add_identifier_matching_state()

    def create_machine(self, pattern_spec):
        current_state = self.start_state
        index = 0

        pattern = pattern_spec[0]
        pattern_type = pattern_spec[1]
        # skip existing states
        char = pattern[index]
        while current_state.get_child(char) is not None:
            current_state = current_state.get_child(char)

            index += 1

            if index == len(pattern):
                break

            char = pattern[index]


        if index == len(pattern):
            current_state.is_final = True
            return

        while index < len(pattern):
            char = pattern[index]
            new_state = State(f'q{len(self.states)+1}', [char], pattern_type)
            current_state.add_transition(new_state)
            current_state = new_state
            self.states.append(new_state)

            index += 1

        current_state.is_final = True


    def match(self, string):
        result = self.start_state.next(string, 0)
        if result is None:
            result = self.identifier_start_state.next(string, 0)

        return result

    def print(self):
        visited = set()
        self.start_state.print(visited)

    def add_string_matching_state(self):
        open_state = State(f'q{len(self.states) + 1}', ['"'], 'STRING')
        self.start_state.add_transition(open_state)
        self.states.append(open_state)

        # add any character to loop back except "
        open_state.loop_back = [chr(i) for i in range(0, 256) if chr(i) != '"']


        close_state = State(f'q{len(self.states) + 1}', ['"'], 'STRING')
        open_state.add_transition(close_state)
        self.states.append(close_state)
        close_state.is_final = True

    def add_char_matching_state(self):
        open_state = State(f'q{len(self.states) + 1}', ['\''], 'CHAR')
        self.start_state.add_transition(open_state)
        self.states.append(open_state)


        char_state = State(f'q{len(self.states) + 1}', [chr(i) for i in range(0, 256) if chr(i) != '\''], 'CHAR')
        open_state.add_transition(char_state)
        self.states.append(char_state)

        close_state = State(f'q{len(self.states) + 1}', ['\''], 'CHAR')
        self.states.append(close_state)
        close_state.is_final = True

        char_state.add_transition(close_state)


    def add_number_matching_state(self):
        number_state = State(f'q{len(self.states) + 1}', [f"{i}" for i in range(0, 10)], 'NUMBER')
        number_state.loop_back = [f"{j}" for j in range(0, 10)]
        self.start_state.add_transition(number_state)
        self.states.append(number_state)

        close_state = State(f'q{len(self.states) + 1}',  [' ', ';', '+', '-', '*', '/', '%', '>', '<', '=', '!',
                                                          '&', '|', '(', ')', '[', ']', '{', '}', ',', '.', ':',
                                                          '"', '\'', '\n', '\t', '\r', '\f', '\v', '\\', '?', ], 'NUMBER')
        self.states.append(close_state)
        close_state.is_final = True

        number_state.add_transition(close_state)

    def add_identifier_matching_state(self):
        # create identifier state getting letters capital and small only
        identifier_state = State(f'q{len(self.states) + 1}', [chr(i) for i in range(65, 91)] + [chr(i) for i in range(97, 123)] + ['_'], 'IDENTIFIER')
        identifier_state.loop_back = [chr(i) for i in range(65, 91)] + [chr(i) for i in range(97, 123)] + [chr(i) for i in range(48, 58)] + ['_']

        self.identifier_start_state.add_transition(identifier_state)
        self.states.append(identifier_state)

        identifier_end_state = State(f'q{len(self.states) + 1}', [' ', ';', '+', '-', '*', '/', '%', '>', '<', '=', '!',
                                                                  '&', '|', '(', ')', '[', ']', '{', '}', ',', '.', ':',
                                                                  '"', '\'', '\n', '\t', '\r', '\f', '\v', '\\', '?', ], 'IDENTIFIER')
        self.states.append(identifier_end_state)
        identifier_end_state.is_final = True
        identifier_state.add_transition(identifier_end_state)





