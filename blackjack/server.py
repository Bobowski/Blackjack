from flask import Flask, request, jsonify

from blackjack.logic import Player, Table


app = Flask(__name__)
clients = {}
tables = {}


# Server return messages
def error(msg):
    return jsonify({"header": "error", "message": msg})


def confirm_register(cid):
    return jsonify({"header": "confirm_register", "id": cid})


def game_state(table):
    return jsonify(table.to_dict())


@app.route('/register', methods=['POST'])
def register():
    cid = max(clients) + 1 if clients else 0
    clients[cid] = Player(request.json["cash"])
    return confirm_register(cid)


@app.route('/player/<int:cid>/begin', methods=['POST'])
def begin_game(cid: int):
    tid = request.json["table_id"]
    if tid not in tables.keys() or tables[tid] is not None:
        tables[tid] = Table()
    clients[cid].join_table(tables[tid], int(request.json["bid"]))

    return game_state(clients[cid])


@app.route('/player/<int:cid>/action', methods=['POST'])
def make_action(cid: int):
    actions = {
        "split": Player.split,
        "double": Player.double,
        "insure": Player.insure,
        "pass": Player.pas,
        "get": Player.get_card,
        "quit": Player.quit_table
    }
    actions[request.json["action"]](clients[cid])
    return game_state(clients[cid])
