import json


class PredictiveParser:
    def __init__(self):
        with open('grammer.json') as f:
            self.grammer = json.load(f)

            self.terminals = self.grammer['terminals']
            self.non_terminals = self.grammer['nonterminals']
            self.start_symbol = self.grammer['start_symbol']
            self.productions = self.grammer['productions']

        self.nullable = {}
        self.first = {}
        self.follow = {}
        self.table = {}

        self.initialize()

    def initialize(self):
        self.set_nullable()
        self.set_first()
        self.set_follow()
        self.build_predictive_table()

        print('nullable => ', self.nullable)
        print('first => ', self.first)
        print('follow => ', self.follow)

        # for non_terminal in self.non_terminals:
        #     print(non_terminal, '=> ', self.table[non_terminal])

    def set_nullable(self):
        for terminal in self.terminals:
            self.nullable[terminal] = False

        for non_terminal in self.non_terminals:
            self.nullable[non_terminal] = False

            for production in self.productions[non_terminal]:
                if len(production) == 0:
                    self.nullable[non_terminal] = True
                    break

    def set_first(self):
        loop = True

        for terminal in self.terminals:
            self.first[terminal] = [terminal]

        for non_terminal in self.non_terminals:
            self.first[non_terminal] = []


        while loop:
            loop = False
            for non_terminal in self.non_terminals:
                for production in self.productions[non_terminal]:
                    for element in production:
                        loop = self.add_first(self.first[element], non_terminal, loop)
                        if not self.nullable[element]:
                            break

    def set_follow(self):
        for terminal in self.terminals:
            self.follow[terminal] = []

        for non_terminal in self.non_terminals:
            self.follow[non_terminal] = []

        loop = True
        while loop:
            loop = False
            for x in self.non_terminals:
                for production in self.productions[x]:
                    for i in range(len(production)):
                        yi = production[i]

                        # check is all next symbols are nullable (Rule 4)
                        all_next_nullable = True
                        for j in range(i + 1, len(production)):
                            yj = production[j]
                            if not self.nullable[yj]:
                                all_next_nullable = False
                                break
                        if all_next_nullable:
                            loop = self.add_follow(self.follow[x], yi, loop)

                        for j in range(i + 1, len(production)):
                            yj = production[j]
                            loop = self.add_follow(self.first[yj], yi, loop)
                            if not self.nullable[yj]:
                                break

    def add_first(self, stack, symbol, loop):
        loop = loop
        for s in stack:
            if s not in self.first[symbol]:
                loop = True
                self.first[symbol].append(s)
        return loop

    def add_follow(self, stack, symbol, loop):
        loop = loop
        for s in stack:
            if s not in self.follow[symbol]:
                self.follow[symbol].append(s)
                loop = True

        return loop

    def build_predictive_table(self):
        self.table = {}

        for non_terminal in self.non_terminals:
            self.table[non_terminal] = {terminal: [] for terminal in self.terminals}
            for production in self.productions[non_terminal]:
                if len(production) == 0:
                    for symbol in self.follow[non_terminal]:
                        self.table[non_terminal][symbol].append(production)
                    continue

                for symbol in self.first[production[0]]:
                    self.table[non_terminal][symbol].append(production)

                if self.nullable[production[0]]:
                    for symbol in self.follow[non_terminal]:
                        self.table[non_terminal][symbol].append(production)





p = PredictiveParser()
