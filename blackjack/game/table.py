from functools import wraps
from typing import List

from namedlist import namedlist

from blackjack.game.decks import Decks, Card


State = namedlist("State", ["phase", "bid", "winner"])


class InvalidMove(Exception):
    def __init__(self, message):
        Exception.__init__(self)
        self.message = message


class Hand:
    def __init__(self):
        self.playing = False
        self.cards = []

    def add(self, card: Card, face_up: bool=True):
        self.playing = True
        card.face_up = face_up
        self.cards.append(card)

    def clear(self):
        self.cards.clear()

    @property
    def value(self) -> int:
        aces = len([x for x in self.cards if x.rank == 1])
        value = sum([10 if x.rank > 10 else x.rank for x in self.cards]) + aces * 10

        if value <= 21 or aces == 0:
            return value

        while aces > 0 and value > 21:
            value -= 10
            aces -= 1
        return value


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
        self.hand = Hand()  # TODO

    def clear(self):
        self.hand.clear()


class Table:
    def __init__(self, account_balance: int):
        self.state = State(phase="awaiting", bid=0, winner=None)
        self.player = Player(account_balance)
        self.croupier = Croupier()
        self.decks = Decks()

        self.did_split = False
        self.did_double = False
        self.did_insure = False

    def game_action(*phases):
        def decorator(f):
            @wraps(f)
            def wrapper(self, *args, **kw):
                if self.state.phase not in phases:
                    raise InvalidMove("Not in proper phase")

                f(self, *args, **kw)

                if self.player.hand.value > 21:
                    self.player.hand.playing = False
                    return

                if self.player.other_hand.playing:
                    self.player.switch_hand()
                    return

                if not self.player.hand.playing:
                    self.state.phase = "end_game"

                    self.croupier.hand.cards[0].face_up = True
                    self.croupier.hand.cards[1].face_up = True
                    while self.croupier.hand.value <= 16:
                        self.croupier.hand.add(self.decks.get())

            return wrapper
        return decorator

    def clear(self):  # TODO
        self.state = State(phase="awaiting", bid=0, winner=None)
        self.croupier.clear()
        self.player.clear()

    @game_action("awaiting")
    def begin_game(self, bid: int):
        self.player.account_balance -= bid
        self.state.bid = bid

        self.croupier.hand.add(self.decks.get(), face_up=False)
        self.croupier.hand.add(self.decks.get(), face_up=True)
        self.player.hand.add(self.decks.get(), face_up=True)
        self.player.hand.add(self.decks.get(), face_up=True)

        self.state.phase = "begin_game"

    @game_action("begin_game", "in_game")
    def get_card(self):
        self.player.hand.add(self.decks.get(), face_up=True)

        self.state.phase = "in_game"

    @game_action("begin_game", "in_game")
    def pas(self):
        self.player.hand.playing = False

        self.state.phase = "in_game"

    @game_action("begin_game")
    def double_down(self):
        self.player.account_balance -= self.state.bid
        self.state.bid *= 2

        self.player.hand.add(self.decks.get(), face_up=True)

        self.state.phase = "in_game"

    @game_action("begin_game")
    def split(self):
        # TODO double bid and split into two hands only if rank matches
        if self.did_split:
            raise InvalidMove("Already did split")

        first_hand, second_hand = self.player.hands
        if first_hand.cards[0].rank == first_hand.cards[1].rank:
            second_hand.add(first_hand.cards.pop())
            self.did_split = True
        else:
            raise InvalidMove("Cannot split cards")

    @game_action("begin_game")
    def insure(self):
        # TODO put additional 0.5 bid if croupier has ace (blackjack possibility)
        raise InvalidMove("Not yet implemented")

        if self.did_insure:
            raise InvalidMove("Already insured")
        if self.croupier.hand.cards[1].rank != 1:
            raise InvalidMove("Croupier does not have ace")

        # TODO finish

    def surrender(self):
        # TODO abandon bid and start new game (open croupier's card ?)
        pass