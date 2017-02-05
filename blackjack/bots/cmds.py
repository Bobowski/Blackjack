import requests


url = "http://127.0.0.1:5000"


def post(path: str, json: dict):
    json = requests.post(url + path, json=json).json()
    if json["header"] == "error":
        raise Exception(json["message"])
    return json


def action(uid: int, action_name: str):
    return post(
        "/player/{uid}/action".format(uid=uid),
        {"action": action_name}
    )


def register(cash: int, seed: int):
    return post("/register", {"cash": cash, "seed": seed})


def begin(uid: int, bid: int):
    return post(
        "/player/{uid}/begin".format(uid=uid),
        {"bid": bid}
    )


def hit(uid: int):
    return action(uid, "hit")


def split(uid: int):
    return action(uid, "split")


def double_down(uid: int):
    return action(uid, "double")


def insure(uid: int):
    return action(uid, "insure")


def stand(uid: int):
    return action(uid, "stand")


def surrender(uid: int):
    return action(uid, "surrender")
