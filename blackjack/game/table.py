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


def action(from_phases, to_phase):
    def decorator(foo):
        @wraps(foo)
        def wrapper(self, *args, **kw):
            # Do not allow execution of command if not in proper phase
            if self.state.phase not in from_phases:
                raise InvalidMove("Not in proper phase")

            # Execute action and switch to target phase
            foo(self, *args, **kw)
            self.state.phase = to_phase

            # Switch if other hand is still playing, resolve if none is
            if not self.player.hand.playing:
                if self.player.other_hand.playing:
                    self.player.switch_hand()
                else:
                    self.resolve_game()
        return wrapper
    return decorator


class Table:
    def __init__(self, account_balance: int, seed: int=42):
        self.state = State(phase="awaiting", bid=0, winnings=0)
        self.player = Player(account_balance)
        self.croupier = Croupier()
        self.decks = Decks(seed=seed)

        self.did_split = False
        self.did_double = False
        self.did_insure = False

    def resolve_game(self):
        self.state.phase = "end_game"

        croupier_hand = self.croupier.hand
        croupier_hand.cards[0].face_up = True
        croupier_hand.cards[1].face_up = True

        valid_hands = (x for x in self.player.hands if 0 < x.value <= 21)
        for player_hand in valid_hands:
            if croupier_hand.has_blackjack and player_hand.has_blackjack:
                multiplier = 1
            elif croupier_hand.has_blackjack:
                multiplier = 0
            elif player_hand.has_blackjack:
                multiplier = 2
            else:
                # No blackjack scenario
                # Croupier has defined strategy
                while croupier_hand.value <= 16:
                    croupier_hand.add(self.decks.get())

                if croupier_hand.value > 21 or player_hand.value > croupier_hand.value:
                    multiplier = 2
                elif player_hand.value == croupier_hand.value:
                    multiplier = 1
                else:
                    multiplier = 0

            self.state.winnings += self.state.bid * multiplier
        self.player.account_balance += self.state.winnings
        self.state.phase = "end_game"

    @action(from_phases=("awaiting", "end_game"), to_phase="begin_game")
    def begin_game(self, bid: int):
        self.croupier.clear()
        self.player.clear()
        self.did_split = False

        self.player.account_balance -= bid
        self.state.bid = bid
        self.state.winnings = 0

        self.croupier.hand.add(self.decks.get(), face_up=False)
        self.croupier.hand.add(self.decks.get(), face_up=True)
        self.player.hand.add(self.decks.get(), face_up=True)
        self.player.hand.add(self.decks.get(), face_up=True)

    @action(from_phases=("begin_game", "in_game"), to_phase="in_game")
    def hit(self):
        self.player.hand.add(self.decks.get(), face_up=True)
        if self.player.hand.value > 21:
            self.player.hand.playing = False

    @action(from_phases=("begin_game", "in_game"), to_phase="in_game")
    def stand(self):
        self.player.hand.playing = False

    @action(from_phases="begin_game", to_phase="in_game")
    def double_down(self):
        self.player.account_balance -= self.state.bid
        self.state.bid *= 2
        self.player.hand.add(self.decks.get(), face_up=True)
        self.player.hand.playing = False

    @action(from_phases=("begin_game",), to_phase="in_game")
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

    @action(from_phases=("begin_game",), to_phase="in_game")
    def insure(self):
        # TODO put additional 0.5 bid if croupier has ace (blackjack possibility)
        raise InvalidMove("Not yet implemented")

    @action(from_phases=("in_game",), to_phase="begin_game")
    def surrender(self):
        # TODO abandon bid and start new game (open croupier's card ?)
        raise InvalidMove("Not yet implemented")
