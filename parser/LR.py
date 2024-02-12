import json


class Item:
    def __init__(self, production, dot_position, lookahead=''):
        self.production = production
        self.dot_position = dot_position
        self.lookahead = lookahead

    def __str__(self):
        return self.production + ' ' + str(self.dot_position) + ' ' + self.lookahead



class ItemSet:
    def __init__(self, items):
        self.items = items




class LR0:
    def __init__(self):
        with open('grammer.json') as f:
            self.grammer = json.load(f)

            self.terminals = self.grammer['terminals']
            self.non_terminals = self.grammer['nonterminals']
            self.start_symbol = self.grammer['start_symbol']
            self.productions = self.grammer['productions']



        self.initialize()

    def initialize(self):
        pass





p = LR0()
