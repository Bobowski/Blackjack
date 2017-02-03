from functools import wraps

from namedlist import namedlist

from blackjack.game.decks import Decks
from blackjack.game.exceptions import InvalidMove
from blackjack.game.players import Player, Croupier

State = namedlist("State", ["phase", "bid", "winnings"])


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

    @action(from_phases=("begin_game",),  to_phase="in_game")
    def double_down(self):
        self.player.account_balance -= self.state.bid
        self.state.bid *= 2
        self.player.hand.add(self.decks.get(), face_up=True)
        self.player.hand.playing = False

    @action(from_phases=("begin_game",), to_phase="in_game")
    def split(self):
        first_hand, second_hand = self.player.hands
        if not (first_hand.is_empty or second_hand.is_empty):
            raise InvalidMove("Already did split")

        if first_hand.cards[0].rank != first_hand.cards[1].rank:
            raise InvalidMove("Cannot split cards")

        self.player.account_balance -= self.state.bid
        second_hand.add(first_hand.cards.pop())
        first_hand.add(self.decks.get(), face_up=True)
        second_hand.add(self.decks.get(), face_up=True)

    @action(from_phases=("begin_game",), to_phase="in_game")
    def insure(self):
        # TODO put additional 0.5 bid if croupier has ace (blackjack possibility)
        raise InvalidMove("Not yet implemented")

    @action(from_phases=("in_game",), to_phase="begin_game")
    def surrender(self):
        # TODO abandon bid and start new game (open croupier's card ?)
        raise InvalidMove("Not yet implemented")
