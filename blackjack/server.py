from functools import wraps

from jsonschema import validate, ValidationError
from flask import Flask, request, jsonify

from blackjack.game import Player, Table, InvalidMove
from blackjack.schemas import schemas


app = Flask(__name__)


def validate_schema(schema_name):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kw):
            validate(request.json, schema=schemas[schema_name])
            return f(*args, **kw)
        return wrapper
    return decorator


@app.errorhandler(ValidationError)
@app.errorhandler(InvalidMove)
def handle_exception(exception):
    response = jsonify({"header": "error", "message": exception.message})
    response.status_code = 400
    return response


@app.route('/register', methods=['POST'])
@validate_schema('register')
def register():
    cid = max(clients) + 1 if clients else 0
    cash = int(request.json["cash"])
    clients[cid] = Player(cash)
    return jsonify({"header": "confirm_register", "id": cid})


@app.route('/player/<int:uid>/begin', methods=['POST'])
@validate_schema('begin_game')
def begin_game(uid: int):
    tid = request.json["table_id"]
    if tid not in tables.keys() or tables[tid] is not None:
        tables[tid] = Table()
    clients[uid].join_table(tables[tid], int(request.json["bid"]))

    return jsonify(clients[uid].to_dict())


@app.route('/player/<int:uid>/action', methods=['POST'])
@validate_schema('action_in_game')
def make_action(uid: int):
    actions = {
        "split": Player.split,
        "double": Player.double,
        "insure": Player.insure,
        "pass": Player.pas,
        "hit": Player.get_card,
        "quit": Player.quit_table
    }
    actions[request.json["action"]](clients[uid])
    return jsonify(clients[uid].to_dict())
