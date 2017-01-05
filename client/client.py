import requests
import os

server = "http://localhost:5000/"

run = True


def enter_game():
    js = requests.post(server + "begin", json={"header": "register", "bid": 10}).json()
    if js["header"] == "error":
        raise Exception(js["message"])
    return js["id"]


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

gid = enter_game()
actions = {
    "split": split,
    "double": double,
    "pas": pas,
    "insure": insure,
    "get": get
}
while run:
    command = input()
    cls()
    print("Game started (id " + str(gid) + ")")
    try:
        js = actions[command](gid)
        if js["header"] == "in_game":
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
    except Exception as e:
        print("Error: " + str(e))

print(gid)
