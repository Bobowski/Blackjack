from functools import wraps

from namedlist import namedlist

from blackjack.game.decks import Decks, Card


State = namedlist("State", ["phase", "bid", "winner"])


class InvalidMove(Exception):
    def __init__(self, message):
        Exception.__init__(self)
        self.message = message


class Hand:
    def __init__(self):
        self.playing = True
        self.cards = []

    def add(self, card: Card, face_up: bool=True):
        card.face_up = face_up
        self.cards.append(card)

    def clear(self):
        self.cards.clear()


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

    @property
    def hand(self) -> Hand or None:
        for hand in self.hands:
            if hand.playing:
                return hand
        return None

    def clear(self):
        for hand in self.hands:
            hand.clear()


class Croupier:
    def __init__(self):
        self.hand = Hand()  # TODO

    def clear(self):
        self.hand.clear()


def game_action(*phases):
    def decorator(f):
        @wraps(f)
        def wrapper(self: Table, *args, **kw):
            if self.state.phase in phases:
                return f(*args, **kw)  # TODO if_end?
            raise InvalidMove("Not in proper phase")
        return wrapper
    return decorator


class Table:
    def __init__(self, account_balance: int):
        self.state = State(phase="awaiting", bid=0, winner=None)
        self.player = Player(account_balance)
        self.croupier = Croupier()
        self.decks = Decks()

        self.did_split = False
        self.did_double = False
        self.did_insure = False

    def clear(self):
        self.state = State(phase="awaiting", bid=0, winner=None)
        self.croupier.clear()
        self.player.clear()

    @game_action("awaiting")
    def begin_game(self, bid: int):
        self.player.account_balance -= bid
        self.state.bid = bid
        self.state.phase = "begin_game"

        self.croupier.hand.add(self.decks.get(), face_up=False)
        self.croupier.hand.add(self.decks.get(), face_up=True)
        self.player.hand.add(self.decks.get(), face_up=True)
        self.player.hand.add(self.decks.get(), face_up=True)

    @game_action("begin_game", "in_game")
    def get_card(self):
        self.player.hand.add(self.decks.get(), face_up=True)

    @game_action("begin_game", "in_game")
    def pas(self):
        self.player.hand.playing = False

    @game_action("begin_game")
    def double_down(self):
        # TODO
        pass

    @game_action("begin_game")
    def split(self):  # TODO check this
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
        if self.did_insure:
            raise InvalidMove("Already insured")
        if self.croupier.hand.cards[1].rank != 1:
            raise InvalidMove("Croupier does not have ace")

        # TODO finish

    def surrender(self):
        # TODO does it exist in rules?
        pass