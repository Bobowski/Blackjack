from functools import wraps
from random import shuffle
# TODO:braukuje po przekroczeniu 21 i zakończeniu wyświetlenia tego
from random import Random
from typing import List


players = {}
tables = {}


class InvalidMove(Exception):
    def __init__(self, message):
        Exception.__init__(self)
        self.message = message


class Card:
    colors = ['Diamond', 'Clubs', 'Hearts', 'Spades']
    ranks = list(range(1, 14))

    def __init__(self, color: str, rank: int, face_up: bool=False):
        self.color = color
        self.rank = rank
        self.face_up = face_up

    def to_dict(self):
        return {
            "color": self.color if self.face_up else "face_down",
            "rank": self.rank if self.face_up else "face_down"
        }

    @staticmethod
    def make_deck():
        return [
            Card(color=color, rank=rank)
            for color in Card.colors
            for rank in Card.ranks
        ]


class Decks:
    def __init__(self, seed: int=42):
        self.cards = []
        self.random = Random(seed)

    def new_deck(self):
        self.cards = Card.make_deck()
        self.random.shuffle(self.cards)

    def get_card(self):
        if len(self.cards) == 0:
            self.new_deck()
        return self.cards.pop()


class Hand:
    def __init__(self):
        self.playing = True
        self.cards = []

    def add_card(self, card: Card, face_up: bool=True):
        card.face_up = face_up
        self.cards.append(card)

    def to_dict(self):
        return {"cards": [a.to_dict() for a in self.cards]}


def calculate_hand_value(cards: List(Card)):
    aces = len([x for x in cards if x.rank == 1])
    value = sum([10 if x.rank > 10 else x.rank for x in cards]) + aces * 10

    if value <= 21 or aces == 0:
        return value

    while aces > 0 and value > 21:
        value -= 10
        aces -= 1
    return value

    # def try_split(self):
    #     if len(self.cards) == 2 and self.cards[0].rank == self.cards[1].rank:
    #         new_hand = Hand()
    #         new_hand.add_card(self.cards.pop())
    #         return new_hand
    #     raise InvalidMove("Cannot perform split")




class Player:
    def __init__(self, cash: int):
        self.balance = cash
        self.table = None


        self.hands = []
        self.did_double = False
        self.did_split = False
        self.game_state = "awaiting"
        self.bid = 0


    def join_table(self, table_id: int, bid: int):
        tables[table_id].sit(self)

        self.game_state = "begin_game"

        self.hands = [Hand()]


        table.start()
        self.game_state = "begin_game"
        self.table = table
        self.hands = []
        self.hands.append(Hand())
        self.hands[0].add_card(self.table.deck.get_card())
        self.hands[0].add_card(self.table.deck.get_card())
        self.has_double = False
        self.has_split = False
        self.bid = bid
        self.balance -= bid
        if self.hands[0].count_cards() == 21: self.end_game()

    def get_card(self):
        if self.table is not None and self.game_state != "end_game":
            for hand in self.hands:
                if hand.playing:
                    hand.add_card(self.table.deck.get_card())
                    if hand.count_cards() >= 21:
                        hand.playing = False
            end = True
            for hand in self.hands:
                if hand.playing:
                    end = False
                    break
            if end:
                self.end_game()
            else:
                self.game_state = "in_game"

    def double(self):
        if self.table is not None:
            if not self.has_double and self.game_state == "begin_game":
                self.bid *= 2
                self.has_double = True
                self.get_card()
            else:
                raise Exception("Cannot double")

    def split(self):
        if self.table is not None:
            if not self.has_split and len(self.hands) == 1 and self.game_state == "begin_game":
                t = self.hands[0].try_split()
                if t is not None:
                    self.hands.append(Hand(t))
                    self.has_split = True
                else:
                    raise Exception("Cannot split - cards are different")
            else:
                raise Exception("Cannot split")

    def insure(self):
        if self.table is not None:
            if self.table.can_insure():
                self.balance -= 0.5 * self.bild
                if self.croupier_hand.cards[1].rank == 10:
                    self.balance += self.bid
                self.table.end_game()
            else:
                raise Exception("Cannot insure")
        else:
            raise Exception("Cannot insure")

    def pas(self, hand_number=0):
        if self.table is not None and self.game_state != "end_game":
            if hand_number >= len(self.hands):
                raise Exception("Hand number out of bounds.")
            if not self.hands[hand_number].playing:
                raise Exception("Hand already passed.")
            self.hands[hand_number].playing = False
            end = True
            for hand in self.hands:
                if hand.playing:
                    end = False
                    break
            if end:
                self.end_game()
            return 0

    def end_game(self):
        self.game_state = "end_game"
        best_hand = None
        for hand in self.hands:
            if best_hand is None or best_hand.count_cards() < hand.count_cards() <= 21:
                best_hand = hand
        self.table.end_game(best_hand)
        if self.table.winner == "player":
            self.balance += 2 * self.bid

    def to_dict(self):
        if self.game_state == "end_game":
            return {
                "header": "end_game",
                "winner": self.table.winner,
                "hands": [a.to_dict() for a in self.hands],
                "croupier": self.table.croupier_hand.to_dict()
            }
        return {
            "header": "in_game",
            "insurance": False,
            "bid": self.bid,
            "hands": [a.to_dict() for a in self.hands],
            "croupier": self.table.croupier_hand.to_dict()
        }

    def quit_table(self):
        self.table.quit()
        self.table = None
        self.hands = None
        self.has_double = None
        self.has_split = None
        self.game_state = "awaiting"
        self.bid = None


def only_in_state(state_name):
    def decorator(f):
        @wraps(f)
        def wrapper(self: Table, *args, **kw):
            if self.game_state == state_name:
                return f(*args, **kw)
            raise InvalidMove("Not in proper state")
        return wrapper
    return decorator


def requires_player():
    def decorator(f):
        @wraps(f)
        def wrapper(self: Table, *args, **kw):
            if self.player is not None:
                return f(*args, **kw)
            raise InvalidMove("No player by the table")
        return wrapper
    return decorator


class Table:
    def __init__(self, bid: int = 0):
        self.game_state = "awaiting"
        self.decks = Decks()
        self.player = None
        self.player_hands = None
        self.player_hand = None
        self.croupier_hand = None
        self.winner = None
        self.bid = bid

    @only_in_state("awaiting")
    @requires_player()
    def begin_game(self, bid):
        self.game_state = "begin_game"

        self.bid = bid

        self.croupier_hand = Hand()
        self.croupier_hand.add_card(self.decks.get_card(), face_up=False)
        self.croupier_hand.add_card(self.decks.get_card(), face_up=True)

        self.player_hand = Hand()
        self.player_hands = [self.player_hand]
        self.player_hand.add_card(self.decks.get_card(), face_up=True)
        self.player_hand.add_card(self.decks.get_card(), face_up=True)



    def start(self):
        if self.game_state == "begin_game" or self.game_state == "in_game":
            raise Exception("Table occupied")
        self.game_state = "begin_game"
        self.croupier_hand = Hand()
        self.croupier_hand.add_card(self.deck.get_card(), False)
        self.croupier_hand.add_card(self.deck.get_card())

    def can_insure(self):
        if self.game_state == "begin_game":
            return False
        if self.croupier_hand.cards[1].rank == 11:
            return True
        return False

    def end_game(self, player_hand):
        self.game_state = "end_game"

        if player_hand is None:
            self.winner = "croupier"

        self.croupier_hand.cards[0].face_up = True
        while self.croupier_hand.count_cards() < 17:
            self.croupier_hand.add_card(self.deck.get_card())

        if 21 >= self.croupier_hand.count_cards() > player_hand.count_cards():
            self.winner = "croupier"
        else:
            self.winner = "player"

    def quit(self):
        self.winner = None  # TODO think of better solution
        self.game_state = "awaiting"
        self.croupier_hand = None
