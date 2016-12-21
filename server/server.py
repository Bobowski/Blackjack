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


class PublicTable:
    def __init__(self, deck, bid, id):
        self.insurance = 0
        self.state = 0
        self.client_cards_1 = []
        self.client_cards_2 = []
        self.bid = bid
        self.croupier_cards = [deck.get_card(), ]
        self.id = id


class Table:
    def __init__(self, bid, id):
        self.deck = Deck()
        self.croupier_card = self.deck.get_card()
        self.public_table = PublicTable(self.deck, bid, id)
        self.add_card()
        self.add_card()
        self.game_state = 0

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

class Client:
    clients_ids = []
    clients_list = []

    def __init__(self, bid):
        self.id = Client.get_id()
        self.table = Table(bid,self.id)

    @staticmethod
    def get_id():
        i = 1
        # Can I iterate through client's ids from clients_list list (containing only Client objects)
        # It would make clients_ids list redundand
        while i in Client.clients_ids:
            i += 1
        return i

    @staticmethod
    def get_client(client_id):
        for client in Client.clients_list:
            if client.id == client_id:
                return client


app = Flask(__name__)


# Handling requests


# Game beginning

@app.route('/begin', methods=['POST'])
def start_game():
    input_json = request.get_json(force=True)
    client = Client(int(input_json))
    # TODO przerobienie tego na slownik { id: client/stol}
    Client.clients_list.append(client)
    Client.clients_ids.append(client.id)
    answer = toJSON(client.table.public_table)
    return answer


@app.route('/game-<client_id>', methods=['POST'])
def handle_request(client_id):
    input_json = request.get_json(force=True)
    client = Client.get_client(int(client_id))
    if input_json == 'SPLIT':
        client.table.split()
    elif input_json == 'INSURE':
        client.table.insure()
    elif input_json == 'DOUBLE':
        client.table.double()
    elif input_json == 'TAKE':
        client.table.add_card()
    answer = toJSON(client.table.public_table)
    return answer


if __name__ == '__main__':
    app.run(debug=True)
