from functools import wraps

from namedlist import namedlist

from blackjack.game.decks import Decks, Card


State = namedlist("State", ["phase", "bid", "winnings"])


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
        cards = [x for x in self.cards if x.face_up]
        aces = len([x for x in cards if x.rank == 1])
        value = sum([10 if x.rank > 10 else x.rank for x in cards]) + aces * 10

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
        self.hand = Hand()

    def clear(self):
        self.hand.clear()


class Table:
    def __init__(self, account_balance: int):
        self.state = State(phase="awaiting", bid=0, winnings=0)
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

                if self.player.other_hand.playing:
                    self.player.switch_hand()
                    return

                if not self.player.hand.playing:
                    self.state.phase = "end_game"

                    self.croupier.hand.cards[0].face_up = True
                    self.croupier.hand.cards[1].face_up = True
                    while self.croupier.hand.value <= 16:
                        self.croupier.hand.add(self.decks.get())

                    for hand in self.player.hands:
                        if hand.value >= self.croupier.hand.value:
                            self.state.winnings += self.state.bid * 2
                    self.player.account_balance += self.state.winnings

                    self.state.phase = "end_game"
            return wrapper
        return decorator

    @game_action("awaiting", "end_game")
    def begin_game(self, bid: int):
        self.croupier.clear()
        self.player.clear()

        self.player.account_balance -= bid
        self.state.bid = bid
        self.state.winnings = 0

        self.croupier.hand.add(self.decks.get(), face_up=False)
        self.croupier.hand.add(self.decks.get(), face_up=True)
        self.player.hand.add(self.decks.get(), face_up=True)
        self.player.hand.add(self.decks.get(), face_up=True)

        self.state.phase = "begin_game"

    @game_action("begin_game", "in_game")
    def hit(self):
        self.player.hand.add(self.decks.get(), face_up=True)

        self.state.phase = "in_game"

    @game_action("begin_game", "in_game")
    def stand(self):
        self.player.hand.playing = False

        self.state.phase = "in_game"

    @game_action("begin_game")
    def double_down(self):
        self.player.account_balance -= self.state.bid
        self.state.bid *= 2
        self.player.hand.add(self.decks.get(), face_up=True)
        self.player.hand.playing = False

        self.state.phase = "in_game"

    @game_action("begin_game")
    def split(self):
        if self.did_split:
            raise InvalidMove("Already did split")

        self.player.account_balance -= self.state.bid

        first_hand, second_hand = self.player.hands
        if first_hand.cards[0].rank == first_hand.cards[1].rank:
            second_hand.add(first_hand.cards.pop())
            first_hand.add(self.decks.get(), face_up=True)
            second_hand.add(self.decks.get(), face_up=True)
            self.did_split = True
        else:
            raise InvalidMove("Cannot split cards")

    @game_action("begin_game")
    def insure(self):
        # TODO put additional 0.5 bid if croupier has ace (blackjack possibility)
        raise InvalidMove("Not yet implemented")

    @game_action("in_game", "begin_game")
    def surrender(self):
        # TODO abandon bid and start new game (open croupier's card ?)
        raise InvalidMove("Not yet implemented")
