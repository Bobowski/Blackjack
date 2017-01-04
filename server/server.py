from random import shuffle

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


class Table:
    def __init__(self, bid, id):
        self.insurance = 0
        self.state = 0
        self.client_cards_1 = []
        self.client_cards_2 = []
        self.bid = bid
        self.deck = Deck()
        self.croupier_card = self.deck.get_card()
        self.public_table = PublicTable(self.deck, bid, id)
        self.add_card()
        self.add_card()
        self.game_state = 0

    def to_json(self, bid):
        d = {'insurance': 0, 'state': 0, 'client_cards_1': self.client_cards_1, 'client_cards_2': self.client_cards_2,
             'bid': self.bid
             'croupier_cards': self.croupier_card}
        return flask.jsonify(**d)

    def add_card(self):
        if len(self.public_table.client_cards_2) != 0:
            self.public_table.client_cards_2.append(self.deck.get_card())
        self.public_table.client_cards_1.append(self.deck.get_card())
        self.game_state = 1

    def double(self):
        if self.game_state == 0:
            self.public_table.bid *= 2
        self.add_card()
        self.game_state = 1

    def split(self):
        if self.game_state == 0:
            if len(self.public_table.client_cards_1) == 2 and self.public_table.client_cards_1[0].get_rank() == \
                    self.public_table.client_cards_1[1].get_rank():
                self.public_table.client_cards_2.append(self.public_table.client_cards_1.pop())

    def insure(self):
        if self.game_state == 0:
            if len(self.public_table.croupier_cards) == 1 and (
                            self.public_table.croupier_cards[0].get_rank() == 10 or
                            self.public_table.croupier_cards[0].get_rank() == 11):
                self.public_table.insurance = True

    def pas(self):
        return 0;


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
        return cid


@app.route('/game-<client_id>', methods=['POST'])
def handle_request(client_id):
    input_json = request.get_json()
    actions[input_json["action"]](clients[client_id])
    return clients[client_id].to_json()


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
