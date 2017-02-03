from blackjack.game.decks import Card
from blackjack.game.exceptions import InvalidMove


class Hand:
    def __init__(self):
        self.playing = False
        self.cards = []

    def add(self, card: Card, face_up: bool=True):
        self.playing = True
        card.face_up = face_up
        self.cards.append(card)

    @property
    def is_empty(self):
        return len(self.cards) == 0

    def clear(self):
        self.cards.clear()

    @property
    def value(self) -> int:
        cards = [x for x in self.cards if x.face_up]
        aces = len([x for x in cards if x.rank == 1])
        value = sum([10 if x.rank > 10 else x.rank for x in cards]) + aces * 10

        if value <= 21 or aces == 0:
            return value

        while aces > 0 and value > 21:
            value -= 10
            aces -= 1
        return value

    @property
    def has_blackjack(self) -> bool:
        return self.value == 21 and len(self.cards) == 2


class Player:
    def __init__(self, account_balance: int):
        self._balance = account_balance
        self.hands = (Hand(), Hand())

    @property
    def account_balance(self) -> int:
        return self._balance

    @account_balance.setter
    def account_balance(self, value: int):
        if value < 0:
            raise InvalidMove("Negative account balance is not allowed")
        self._balance = value

    def switch_hand(self):
        if self.hands[1].playing:
            self.hands = (self.hands[1], self.hands[0])

    @property
    def hand(self) -> Hand:
        return self.hands[0]

    @property
    def other_hand(self):
        return self.hands[1]

    def clear(self):
        for hand in self.hands:
            hand.clear()


class Croupier:
    def __init__(self):
        self.hand = Hand()

    def clear(self):
        self.hand.clear()