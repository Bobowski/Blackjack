from random import shuffle

from flask import Flask, request, jsonify


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
        count = 0
        for x in self.cards:
            count += x.rank
        return count

    def try_split(self):
        if len(self.cards) == 2 and self.cards[0] == self.cards[1]:
            return self.cards.pop()
        return None

    def is_playing(self):
        return self.playing

    def to_dict(self):
        return {"cards": [a.to_dict() for a in self.cards if a.face_up]}


class Table:
    def __init__(self, bid):
        self.insurance = 0
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
        self.game_state = "begin_game"

    def to_json(self):
        return jsonify(
            {"header": "in_game", "insurance": self.insurance, "hands": [a.to_dict() for a in self.client_hands],
             "bid": self.bid, "croupier": self.croupier_hand.to_dict()})

    # TODO: co ma być zwracane dla kard krupiera w zależności od stanu gry (tworzyć zmienną jedna karta do zwrotu, czy jak będzie)

    def add_card(self):
        for hand in self.client_hands:
            if hand.playing:
                hand.add_card(self.deck.get_card())
                if hand.count_cards() > 21:
                    hand.playing = False
        end = True
        for hand in self.client_hands:
            if hand.playing:
                end = False
                break
        if end:
            self.end_game()
        self.game_state = "in_game"

    def double(self):
        if self.game_state == "begin_game":
            self.bid *= 2
        self.add_card()

    def split(self):
        t = self.client_hands[0].try_split()
        if t is not None:
            self.client_hands.append(Hand(t))

    def insure(self):
        if self.game_state == "begin_game":
            if len(self.croupier_hand.cards) == 2 and \
                    (self.croupier_hand.cards[1].get_rank() == 10
                     or self.croupier_hand.cards[1].get_rank() == 11):
                self.insurance = True

    def pas(self, hand_number=0):
        if hand_number < len(self.client_hands):
            self.client_hands[hand_number].playing = False
        else:
            raise Exception("Hand number out of bounds.")
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
        #TODO count cards or smth


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
            return jsonify({"header": "begin_game", "id": cid})
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
        return clients[cid].to_json()
    except Exception as e:
        return error(str(e))


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=False)
