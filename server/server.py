from random import shuffle

import flask
from flask import Flask, request

import json


class Card:
    def __init__(self, color, rank):
        # color - 'D' Diamonds, 'C' Clubs, 'H' Hearts, 'S' Spades
        # rank - number from 1 to 13
        self.color = color
        self.rank = rank

    def get_rank(self):
        return self.rank


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
    def __init__(self, cards = []):
        self.cards = []
        self.playing = True

    def add_card(self, card):
        self.cards.append(card)

    def get_card(self, deck):
        if self.playing:
            self.cards.append(deck.get_card())

    def count_card(self):
        count =0
        for x in self.cards:
            count += x
        return count

    def try_split(self):
        if len(self.cards) == 2 and self.cards[0] == self.cards[1]:
                return self.cards.pop()
        return None

class Table:
    def __init__(self, bid):
        self.insurance = 0
        self.is_first_move = True
        self.client_hands = []
        self.client_hands.append(Hand())
        self.bid = bid
        self.deck = Deck()
        self.croupier_card = self.deck.get_card()
        self.add_card()
        self.add_card()
        self.game_state = "begin_game"

    def to_json(self):
        d = {'insurance': 0, 'state': 0, 'client_hands': self.client_hands, 'bid': self.bid, 'croupier_cards': self.croupier_card}
        return flask.jsonify(**d)

    # TODO: co ma być zwracane dla kard krupiera w zależności od stanu gry (tworzyć zmienną jedna karta do zwrotu, czy jak będzie)

    def add_card(self):
        if len(self.client_hands) == 2:
            if self.client_hands[1].playing:
                self.client_hands[1].append(self.deck.get_card())
                if self.client_hands[1].count_card > 21:
                    self.client_hands[1].playing=False
        if self.client_hands[0].playing:
            self.client_hands[0].append(self.deck.get_card())
            if self.client_hands[0].count_card > 21:
                self.client_hands[0].playing=False
        self.game_state = "in_game"

    def double(self):
        if self.game_state == "begin_game":
            self.bid *= 2
        self.add_card()

    def split(self):
        t=self.client_hands[0].try_split
        if t is not None:
            self.client_hands.append(Hand())
            self.client_hands[1].cards[0].append(t)


    def insure(self):
        if self.game_state == "begin_game":
            if len(self.croupier_cards) == 1 and (self.croupier_cards[0].get_rank() == 10 or self.croupier_cards[0].get_rank() == 11):
                self.insurance = True

    def pas(self):
        #TODO pasowanie tylko jednej ręki
        return 0


# I don't know if this belong to server or client ;p object -> JSON
def toJSON(obj):
    return json.dumps(obj, default=lambda o: o.__dict__, sort_keys=True, indent=2)


# Game creation

clients = {}
last_id = -1
actions = {"split" : Table.split} #TODO

def get_id():
    return ++last_id

app = Flask(__name__)


# Handling requests


# Game beginning

@app.route('/begin', methods=['POST'])
def start_game():
    input_json = request.get_json()
    if input_json["action"] == "register":
        cid = get_id()
        clients[cid] = Table(input_json["bid"])
        return jsonify({"game_state": "begin_game", "id": cid})


@app.route('/game-<client_id>', methods=['POST'])
def handle_request(client_id):
    input_json = request.get_json()
    actions[input_json["action"]](clients[client_id])
    return clients[client_id].to_json()


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
