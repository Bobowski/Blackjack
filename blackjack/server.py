from functools import wraps

from jsonschema import validate, ValidationError
from flask import Flask, request, jsonify

from blackjack.game.table import Table, InvalidMove
from blackjack.schemas import schemas
from blackjack.describe import table_to_dict

app = Flask(__name__)


tables = {}


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
    cash = request.json["cash"]
    seed = request.json["seed"]
    uid = max(tables) + 1 if tables else 0
    tables[uid] = Table(account_balance=cash, seed=seed)
    return jsonify({"header": "confirm_register", "uid": uid})


@app.route('/player/<int:uid>/begin', methods=['POST'])
@validate_schema('begin_game')
def begin_game(uid: int):
    tables[uid].begin_game(request.json["bid"])

    table_dict = table_to_dict(tables[uid])
    table_dict["header"] = "success"
    return jsonify(table_dict)


@app.route('/player/<int:uid>/action', methods=['POST'])
@validate_schema('action_in_game')
def make_action(uid: int):
    actions = {
        "split": Table.split,
        "double_down": Table.double_down,
        "stand": Table.stand,
        "hit": Table.hit
    }
    actions[request.json["action"]](tables[uid])

    table_dict = table_to_dict(tables[uid])
    table_dict["header"] = "success"
    return jsonify(table_dict)
