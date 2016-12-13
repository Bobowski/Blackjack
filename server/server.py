from random import shuffle


class Card:
    def __init__(self, color, rank):
        # color - 'D' Diamonds, 'C' Clubs, 'H' Hearts, 'S' Spades
        # rank - number from 1 to 13
        self.color = color
        self.rank = rank

    def get_rank(self):
        return self.rank


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


class PublicTable:
    def __init__(self, deck, bid):
        self.insurance = 0
        self.state = 0
        self.client_cards_1 = []
        self.client_cards_2 = []
        self.bid = bid
        self.croupier_cards = [deck.get_card(), ]


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
