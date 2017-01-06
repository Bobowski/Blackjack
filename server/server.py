from random import shuffle

from flask import Flask, request, jsonify

cards_points = {
    1: 2,
    2: 3,
    3: 4,
    4: 5,
    5: 6,
    6: 7,
    7: 8,
    8: 9,
    9: 10,
    10: 10,
    11: 10,
    12: 10,
    13: 11
}


class Card:
    def __init__(self, color, rank, face_up=False):
        # color - 'D' Diamonds, 'C' Clubs, 'H' Hearts, 'S' Spades
        # rank - number from 1 to 13
        self.color = color
        self.rank = rank
        self.face_up = face_up

    def get_rank(self):
        return self.rank

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

    def get_card(self, deck):
        if self.playing:
            self.cards.append(deck.get_card())

    def count_cards(self):
        aces = len([x for x in self.cards if x.rank == 13])
        value = sum([cards_points[x.rank] for x in self.cards])

        if value <= 21 or aces == 0:
            return value

        while aces > 0 and value > 21:
            value -= 10  # value = value - 11 (ace) + 1 (other value ace)
            aces -= 1
        return value

    def try_split(self):
        if len(self.cards) == 2 and self.cards[0].rank == self.cards[1].rank:
            return self.cards.pop()
        return None

    def is_playing(self):
        return self.playing

    def to_dict(self):
        return {"cards": [a.to_dict() for a in self.cards if a.face_up]}


class Table:
    def __init__(self, bid):
        self.winner = ""  # TODO think of better solution

        self.game_state = "begin_game"
        self.is_first_move = True
        self.client_hands = []
        self.client_hands.append(Hand())
        self.bid = bid
        self.deck = Deck()
        self.croupier_hand = Hand()
        self.croupier_hand.add_card(self.deck.get_card(), False)
        self.croupier_hand.add_card(self.deck.get_card())
        self.add_card()
        self.add_card()
        self.has_split = False
        self.has_double = False
        self.has_insurance = False
        # TODO: sprawdzic, czy to tak
        # TODO: make Monika write comments in english and investigate TODO above
        # self.client_card = self.croupier_hand[0].card[0]

    def to_dict(self):
        if self.game_state == "end_game":
            return {
                "header": "end_game",
                "winner": self.winner,
                "hands": [a.to_dict() for a in self.client_hands],
                "croupier": self.croupier_hand.to_dict()
            }
        return {
            "header": "in_game",
            "insurance": self.has_insurance,
            "bid": self.bid,
            "hands": [a.to_dict() for a in self.client_hands],
            "croupier": self.croupier_hand.to_dict()
        }

    def add_card(self):
        for hand in self.client_hands:
            if hand.playing:
                hand.add_card(self.deck.get_card())
                if hand.count_cards() >= 21:
                    hand.playing = False
        end = True
        for hand in self.client_hands:
            if hand.playing:
                end = False
                break
        if end:
            self.end_game()
        else:
            self.game_state = "in_game"

    def double(self):
        if not self.has_double and self.game_state == "begin_game":
            self.bid *= 2
            self.has_double = True
            self.add_card()
        else:
            raise Exception("Cannot double")

    def split(self):
        if not self.has_split and len(self.client_hands) == 1 and self.game_state == "begin_game":
            t = self.client_hands[0].try_split()
            if t is not None:
                self.client_hands.append(Hand(t))
                self.has_split = True
            else:
                raise Exception("Cannot split - cards are different")
        else:
            raise Exception("Cannot split")

    # TODO check if insurance is only against Blackjack
    def insure(self):
        if not self.has_insurance and self.game_state == "begin_game":
            if len(self.croupier_hand.cards) == 2 and \
                    (self.croupier_hand.cards[1].get_rank() == 10 or self.croupier_hand.cards[1].get_rank() == 11):
                self.has_insurance = True
            else:
                raise Exception("Cannot insure")
        else:
            raise Exception("Cannot insure")

    def pas(self, hand_number=0):
        if hand_number >= len(self.client_hands):
            raise Exception("Hand number out of bounds.")
        if not self.client_hands[hand_number].playing:
            raise Exception("Hand already passed.")
        self.client_hands[hand_number].playing = False
        end = True
        for hand in self.client_hands:
            if hand.playing:
                end = False
                break
        if end:
            self.end_game()
        return 0

    def end_game(self):
        self.game_state = "end_game"
        print("Game has ended")
        player_best_hand = self.client_hands[0]
        if len(self.client_hands) == 2 \
                and 21 >= self.client_hands[1].count_cards() > self.client_hands[0].count_cards():
            player_best_hand = self.client_hands[1]
        self.croupier_hand.cards[0].face_up = True
        while self.croupier_hand.count_cards() < 17:
            self.croupier_hand.add_card(self.deck.get_card())
        if self.croupier_hand.count_cards() > player_best_hand.count_cards() or player_best_hand.count_cards() > 21:
            self.winner = "croupier"
        else:
            self.winner = "player"


clients = {}
actions = {
    "split": Table.split,
    "double": Table.double,
    "insure": Table.insure,
    "pas": Table.pas,
    "get": Table.add_card
}

app = Flask(__name__)


# Handling requests


# Game beginning

def error(msg):
    return jsonify({"header": "error", "message": msg})


last_id = -1


def get_id():
    global last_id
    last_id += 1
    return last_id


@app.route('/begin', methods=['POST'])
def start_game():
    input_json = request.get_json()
    if input_json["header"] == "register":
        try:
            cid = get_id()
            clients[cid] = Table(input_json["bid"])
            return jsonify({"header": "begin_game", "id": cid, "table": clients[cid].to_dict()})
        except Exception as e:
            return error(str(e))

    else:
        return error("Invalid command")


@app.route('/game-<client_id>', methods=['POST'])
def handle_request(client_id):
    input_json = request.get_json()
    try:
        cid = int(client_id)
        actions[input_json["header"]](clients[cid])
        return jsonify(clients[cid].to_dict())
    except Exception as e:
        return error(str(e))


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=False)
