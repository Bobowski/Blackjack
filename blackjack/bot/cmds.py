import requests


url = "http://127.0.0.1:5000"


def post(path, json):
    json = requests.post(url + path, json=json).json()
    if json["header"] == "error":
        raise Exception(json["message"])
    return json


def action(uid, action_name):
    return post(
        "/player/{uid}/action".format(uid=uid),
        {"action": action_name}
    )


def register(cash):
    return post("/register", {"cash": cash})


def begin(uid, bid):
    return post(
        "/player/{uid}/begin".format(uid=uid),
        {"bid": bid}
    )


def hit(uid):
    return action(uid, "hit")


def split(uid):
    return action(uid, "split")


def double_down(uid):
    return action(uid, "double_down")


def insure(uid):
    return action(uid, "insure")


def stand(uid):
    return action(uid, "stand")


def surrender(uid):
    return action(uid, "surrender")
