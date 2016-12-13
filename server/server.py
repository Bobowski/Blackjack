from random import shuffle

import json


class Card:
    def __init__(self, color, rank):
        # color - 'D' Diamonds, 'C' Clubs, 'H' Hearts, 'S' Spades
        # rank - number from 1 to 13
        self.color = color
        self.rank = rank

    def get_rank(self):
        return self.rank

    # TODO JSON to Table parser if needed


class Deck:
    def __init__(self):
        self.cards = []
        colors = ['D', 'C', 'H', 'S']
        for c in colors:
            for r in range(1, 14):
                self.cards.append(Card(c, r))

    def shuffle(self):
        shuffle(self.cards)

    def get_card(self):
        return self.cards.pop()

    # TODO JSON to Table parser if needed


class PublicTable:
    def __init__(self, deck, bid):
        self.insurance = 0
        self.state = 0
        self.client_cards_1 = []
        self.client_cards_2 = []
        self.bid = bid
        self.croupier_cards = [deck.get_card(), ]

    # JSON To PublicTable parser similarly other parsers
    # TODO parser optimization maybe?
    def JSONtoPublicTable(self, js):
        if 'bid' in js:
            self.bid = js['bid']
        if 'insurance' in js:
            self.insurance = js['insurance']
        if 'state' in js:
            self.state = js['state']
        if 'client_cards_1' in js:
            i = 0
            for card in self.client_cards_1:
                if i < len(js['client_cards_1']):
                    card.color = js['client_cards_1'][i]['color']
                    card.rank = js['client_cards_1'][i]['rank']
                    i += 1
        if 'client_cards_2' in js:
            i = 0
            for card in self.client_cards_2:
                if i < len(js['client_cards_2']):
                    card.color = js['client_cards_2'][i]['color']
                    card.rank = js['client_cards_2'][i]['rank']
                    i += 1
        if 'croupier_cards' in js:
            i = 0
            for card in self.croupier_cards:
                if i < len(js['croupier_cards']):
                    card.color = js['croupier_cards'][i]['color']
                    card.rank = js['croupier_cards'][i]['rank']
                    i += 1


class Table:
    def __init__(self, bid):
        self.deck = Deck()
        self.croupier_card = self.deck.get_card()
        self.public_table = PublicTable(self.deck, bid)
        self.add_card()
        self.add_card()
        self.game_state = 0

    def add_card(self):
        if len(self.public_table.client_cards_2) != 0:
            self.public_table.client_cards_2.append(self.deck.get_card())
        self.public_table.client_cards_1.append(self.deck.get_card())
        self.game_state = 1

    def double(self):
        if self.game_state == 0:
            self.public_table.bid *= 2
        self.add_card()
        self.game_state = 1

    def split(self):
        if self.game_state == 0:
            if len(self.public_table.client_cards_1) == 2 and self.public_table.client_cards_1[0].get_rank() == \
                    self.public_table.client_cards_1[1].get_rank():
                self.public_table.client_cards_2.append(self.public_table.client_cards_1.pop())

    def insure(self):
        if self.game_state == 0:
            if len(self.public_table.croupier_cards) == 1 and (
                            self.public_table.croupier_cards[0].get_rank() == 10 or
                            self.public_table.croupier_cards[0].get_rank() == 11):
                self.public_table.insurance = True

    def pas(self):
        return 0;

    # TODO JSON to Table parser if needed


# I don't know if this belong to server or client ;p object -> JSON
def toJSON(obj):
    return json.dumps(obj, default=lambda o: o.__dict__, sort_keys=True)
