from random import shuffle
# TODO:braukuje po przekroczeniu 21 i zakończeniu wyświetlenia tego


class InvalidMove(Exception):
    def __init__(self, message):
        Exception.__init__(self)
        self.message = message


class Card:
    def __init__(self, color, rank, face_up=False):
        # color - 'D' Diamonds, 'C' Clubs, 'H' Hearts, 'S' Spades
        # rank - number from 1 to 13
        self.color = color
        self.rank = rank
        self.face_up = face_up

    def to_dict(self):
        return {"color": self.color, "rank": self.rank}


class Deck:
    def __init__(self):
        self.cards = []
        colors = ['D', 'C', 'H', 'S']
        for c in colors:
            for r in range(1, 14):
                self.cards.append(Card(c, r))
        shuffle(self.cards)

    def shuffle(self):
        shuffle(self.cards)

    def get_card(self):
        if len(self.cards) == 0:
            colors = ['D', 'C', 'H', 'S']
            for c in colors:
                for r in range(1, 14):
                    self.cards.append(Card(c, r))
            shuffle(self.cards)
        return self.cards.pop()


class Hand:
    def __init__(self, card=None):
        self.playing = True
        if card is None:
            self.cards = []
            return
        if not isinstance(card, Card):
            raise Exception("Variable is not Card")
        self.cards = [card]

    def add_card(self, card, face_up=True):
        if not isinstance(card, Card):
            raise Exception("Variable is not Card")
        self.cards.append(Card(card.color, card.rank, face_up))

    def count_cards(self):
        aces = len([x for x in self.cards if x.rank == 1])
        value = sum([10 if x.rank > 10 else x.rank for x in self.cards]) + aces * 10

        if value <= 21 or aces == 0:
            return value

        while aces > 0 and value > 21:
            value -= 10
            aces -= 1
        return value

    def try_split(self):
        if len(self.cards) == 2 and self.cards[0].rank == self.cards[1].rank:
            return self.cards.pop()
        return None

    def to_dict(self):
        return {"cards": [a.to_dict() for a in self.cards if a.face_up]}


class Player:
    def __init__(self, cash):
        self.table = None
        self.hands = None
        self.has_double = None
        self.has_split = None
        self.game_state = "awaiting"
        self.bid = None
        self.balance = cash

    def join_table(self, table, bid):
        if not isinstance(table, Table):
            raise Exception("Variable is not table!")
        try:
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
        except Exception as e:
            raise e

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


class Table:
    def __init__(self):
        self.winner = None  # TODO think of better solution
        self.game_state = "awaiting"
        self.deck = Deck()
        self.croupier_hand = None

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
