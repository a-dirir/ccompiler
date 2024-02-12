

class State:
    def __init__(self, name: str, values: list, state_type: str = None, loop_back: list = None):
        self.name = name
        self.values = values
        self.state_type = state_type
        self.loop_back = loop_back
        self.transitions = []
        self.is_final = False

    def next(self, string, index):
        if self.state_type == "IDENTIFIER" or self.state_type == "NUMBER":
            lexeme = string[:index-1]
        else:
            lexeme = string[:index]

        if self.loop_back is not None:
            if string[index] in self.loop_back:
                return self.next(string, index+1)

        if self.is_final:
            if len(string[index:]) == 0:
                return {'name': self.name, 'index': index, 'type': self.state_type, 'lexeme': lexeme}

            if len(self.transitions) == 0:
                return {'name': self.name, 'index': index, 'type': self.state_type, 'lexeme': lexeme}

            else:
                lookahead = self.get_child(string[index])
                if lookahead is None:
                    return {'name': self.name, 'index': index, 'type': self.state_type, 'lexeme': lexeme}

                return lookahead.next(string, index+1)


        if len(string[index:]) == 0:
            return None

        next_state = self.get_child(string[index])
        if next_state is None:
            return None

        return next_state.next(string, index+1)

    def get_child(self, value):
        for transition in self.transitions:
            if value in transition.values:
                return transition

        return None

    def add_transition(self, transition):
        self.transitions.append(transition)

    def __repr__(self):
        output = f"State: {self.name}; "
        for value in self.values:
            output += f"{value}, "
        return output

    def print(self, visited):
        if self not in visited:
            print(self, end=' -> ')

            visited.add(self)
            for transition in self.transitions:
                transition.print(visited)


        if self.is_final:
            if len(self.transitions) == 0:
                print()
