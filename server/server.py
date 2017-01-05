from random import shuffle

import flask
from flask import Flask, request, jsonify

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
    def __init__(self, card=None):
        self.playing = True
        if card is None:
            self.cards = []
            return
        if isinstance(card, Card):
            raise Exception("Variable is not Card")
        self.cards = [card]

    def add_card(self, card):
        self.cards.append(card)

    def get_card(self, deck):
        if self.playing:
            self.cards.append(deck.get_card())

    def count_card(self):
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
        return jsonify({"header": "in_game", "insurance": self.insurance, "hands": self.client_hands, "bid": self.bid,
                        "croupier": self.croupier_card})

    # TODO: co ma być zwracane dla kard krupiera w zależności od stanu gry (tworzyć zmienną jedna karta do zwrotu, czy jak będzie)

    def add_card(self):
        if len(self.client_hands) == 2:
            if self.client_hands[1].playing:
                self.client_hands[1].add_card(self.deck.get_card())
                if self.client_hands[1].count_card() > 21:
                    self.client_hands[1].playing = False
        if self.client_hands[0].playing:
            self.client_hands[0].add_card(self.deck.get_card())
            if self.client_hands[0].count_card() > 21:
                self.client_hands[0].playing = False
        self.game_state = "in_game"

    def double(self):
        if self.game_state == "begin_game":
            self.bid *= 2
        self.add_card()

    def split(self):
        t = self.client_hands[0].try_split
        if t is not None:
            self.client_hands.append(Hand())
            self.client_hands[1].cards[0].append(t)

    def insure(self):
        if self.game_state == "begin_game":
            if len(self.croupier_cards) == 1 and (
                            self.croupier_cards[0].get_rank() == 10 or self.croupier_cards[0].get_rank() == 11):
                self.insurance = True

    def pas(self):
        # TODO pasowanie tylko jednej ręki
        return 0


# Game creation

clients = {}
actions = {"split": Table.split, "double": Table.double, "insure": Table.insure, "pas": Table.pas}

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
        actions[input_json["action"]](clients[client_id])
        return clients[client_id].to_json()
    except Exception as e:
        return error(str(e))


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=False)
