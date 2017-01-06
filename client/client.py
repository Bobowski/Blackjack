import requests
import os
import time

server = "http://localhost:5000/"

run = True
cards_points = {
    1: 2,
    2: 3,
    3: 4,
    4: 5,
    5: 6,
    6: 7,
    7: 8,
    8: 9,
    9: 10,
    10: 10,
    11: 10,
    12: 10,
    13: 11
}


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


def print_hand(hand):
    print("(value " + str(count_cards(hand)) + "):")
    for card in hand["cards"]:
        print(ranks[card["rank"]] + " of " + colors[card["color"]] + " ")


def print_table(js):
    print("insurance: " + str(js["insurance"]))
    print("bid: " + str(js["bid"]))
    hands = js["hands"]
    print()
    for hand in hands:
        print("hand ", end="")
        print_hand(hand)
    print("\ncroupier ", end="")
    print_hand(js["croupier"])


def print_end(js):
    print("winner: " + str(js["winner"]))
    hands = js["hands"]
    print()
    for hand in hands:
        print("hand ", end="")
        print_hand(hand)
    print("\ncroupier ", end="")
    print_hand(js["croupier"])


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def count_cards(hand):
    cards = hand["cards"]
    aces = len([x for x in cards if x["rank"] == 13])
    value = sum([cards_points[x["rank"]] for x in cards])

    if value <= 21 or aces == 0:
        return value

    while aces > 0 and value > 21:
        value -= 10  # value = value - 11 (ace) + 1 (other value ace)
        aces -= 1
    return value


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
    "hit": get
}
print("Game started (id " + str(gid) + ")")
print_table(init_js["table"])

while run:
    command = input()
    js = ""
    cls()
    if command == "quit":
        break
    try:
        js = actions[command](gid)
        if js["header"] == "in_game":
            print_table(js)
        elif js["header"] == "end_game":
            print_end(js)
            break
    except Exception as e:
        print("Error: " + str(e))
        print_table(js)
time.sleep(3)
cls()
