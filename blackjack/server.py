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
    return None


@app.route('/begin', methods=['POST'])
def start_game():
    json = request.get_json()

    if json["header"] != "register":
        return error("Invalid command header: " + json["header"])

    try:
        cid = max(clients) + 1 if clients else 0
        clients[cid] = Player(json["cash"])
        return confirm_register(cid)
    except Exception as e:
        return error(str(e))


actions = {
    "split": Player.split,
    "double": Player.double,
    "insure": Player.insure,
    "pass": Player.pas,
    "get": Player.get_card,
    "quit": Player.quit_table
}


@app.route('/player-<int:cid>', methods=['POST'])
def handle_request(cid: int):
    json = request.get_json()

    try:
        cid = int(cid)
        if json["header"] == "begin_game":
            tid = json["table_id"]
            if tid not in tables.keys() or tables[tid] is not None:
                tables[tid] = Table()
            clients[cid].join_table(tables[tid], int(json["bid"]))
        else:
            actions[json["header"]](clients[cid])
        if clients[cid].table is None:
            raise Exception("You are not in a game")
        return jsonify(clients[cid].to_dict())
    except Exception as e:
        return error(str(e))
