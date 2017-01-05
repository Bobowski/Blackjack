import requests

server = "http://localhost:5000/"


run = True


def enter_game():
    js = requests.post(server + "begin", json={"header": "register", "bid": 10}).json()
    if js["header"] == "error":
        raise Exception(js["message"])
    return js["id"]


def split(gid):
    js = requests.post(server + str(gid), json={"header": "split"}).json()
    if js["header"] == "error":
        raise Exception(js["message"])
    return js


def double(gid):
    js = requests.post(server + str(gid), json={"double": "split"}).json()
    if js["header"] == "error":
        raise Exception(js["message"])
    return js


def pas(gid):
    js = requests.post(server + str(gid), json={"pas": "split"}).json()
    if js["header"] == "error":
        raise Exception(js["message"])
    return js


def insure(gid):
    js = requests.post(server + str(gid), json={"insure": "split"}).json()
    if js["header"] == "error":
        raise Exception(js["message"])
    return js



gid = enter_game()
actions = {
    "split": split,
    "double": double,
    "pas": pas,
    "insure": insure
}
while run:
    command = input()
    try:
        actions[command](gid)
    except Exception as e:
        print(str(e))

print(gid)
