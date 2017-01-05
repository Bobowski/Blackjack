import requests
import os

server = "http://localhost:5000/"

run = True


def enter_game(bid):
    js = requests.post(server + "begin", json={"header": "register", "bid": bid}).json()
    if js["header"] == "error":
        raise Exception(js["message"])
    return js


def split(gid):
    js = requests.post(server + "game-" + str(gid), json={"header": "split"}).json()
    if js["header"] == "error":
        raise Exception(js["message"])
    return js


def double(gid):
    js = requests.post(server + "game-" + str(gid), json={"header": "double"}).json()
    if js["header"] == "error":
        raise Exception(js["message"])
    return js


def pas(gid):
    js = requests.post(server + "game-" + str(gid), json={"header": "pas"}).json()
    if js["header"] == "error":
        raise Exception(js["message"])
    return js


def insure(gid):
    js = requests.post(server + "game-" + str(gid), json={"header": "insure"}).json()
    if js["header"] == "error":
        raise Exception(js["message"])
    return js


def get(gid):
    js = requests.post(server + "game-" + str(gid), json={"header": "get"}).json()
    if js["header"] == "error":
        raise Exception(js["message"])
    return js

def print_table(js):
    print("insurance: " + str(js["insurance"]))
    print("bid: " + str(js["bid"]))
    hands = js["hands"]
    print()
    for hand in hands:
        print("hand: ")
        for card in hand["cards"]:
            print(ranks[card["rank"]] + " of " + colors[card["color"]] + " ")
    print("\ncroupier: ")
    for card in js["croupier"]["cards"]:
        print(ranks[card["rank"]] + " of " + colors[card["color"]] + " ")

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


ranks = {
    1: "2",
    2: "3",
    3: "4",
    4: "5",
    5: "6",
    6: "7",
    7: "8",
    8: "9",
    9: "10",
    10: "Jack",
    11: "Queen",
    12: "King",
    13: "Ace"
}
colors = {
    "D": "Diamonds",
    "S": "Spades",
    "H": "Hearts",
    "C": "Clubs"
}

init_js = enter_game(10)
gid = init_js["id"]
actions = {
    "split": split,
    "double": double,
    "pas": pas,
    "insure": insure,
    "get": get
}
print("Game started (id " + str(gid) + ")")
print_table(init_js["table"])
while run:
    command = input()
    cls()
    try:
        js = actions[command](gid)
        if js["header"] == "in_game":
            print_table(js)
    except Exception as e:
        print("Error: " + str(e))

print(gid)
