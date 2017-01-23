from flask import Flask, request, jsonify

from blackjack.logic import Player, Table

clients = {}
tables = {}
actions = {
    "split": Player.split,
    "double": Player.double,
    "insure": Player.insure,
    "pass": Player.pas,
    "get": Player.get_card,
    "quit": Player.quit_table
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
            clients[cid] = Player(input_json["cash"])
            return jsonify({"header": "confirm_register", "id": cid})
        except Exception as e:
            return error(str(e))

    else:
        return error("Invalid command")


@app.route('/player-<client_id>', methods=['POST'])
def handle_request(client_id):
    input_json = request.get_json()
    try:
        cid = int(client_id)
        if input_json["header"] == "begin_game":
            tid = input_json["table_id"]
            if tid not in tables.keys() or tables[tid] is not None:
                tables[tid] = Table()
            clients[cid].join_table(tables[tid], int(input_json["bid"]))
        else:
            actions[input_json["header"]](clients[cid])
        if clients[cid].table is None:
            raise Exception("You are not in a game")
        return jsonify(clients[cid].to_dict())
    except Exception as e:
        return error(str(e))
