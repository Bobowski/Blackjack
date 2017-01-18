import requests
import os
import time

server = "http://127.0.0.1:5000/"

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


def register(cash):
    js = requests.post(server + "begin", json={"header": "register", "cash": cash}).json()
    if js["header"] == "error":
        raise Exception(js["message"])
    return js


def join_game(gid, pid):
    js = requests.post(server + "player-" + str(pid), json={"header": "begin_game", "table_id": gid, "bid": 10}).json()
    if js["header"] == "error":
        raise Exception(js["message"])
    return js


def split(pid):
    js = requests.post(server + "player-" + str(pid), json={"header": "split"}).json()
    if js["header"] == "error":
        raise Exception(js["message"])
    return js


def double(pid):
    js = requests.post(server + "player-" + str(pid), json={"header": "double"}).json()
    if js["header"] == "error":
        raise Exception(js["message"])
    return js


def pas(pid):
    js = requests.post(server + "player-" + str(pid), json={"header": "pass"}).json()
    if js["header"] == "error":
        raise Exception(js["message"])
    return js


def insure(pid):
    js = requests.post(server + "player-" + str(pid), json={"header": "insure"}).json()
    if js["header"] == "error":
        raise Exception(js["message"])
    return js


def get(pid):
    js = requests.post(server + "player-" + str(pid), json={"header": "get"}).json()
    if js["header"] == "error":
        raise Exception(js["message"])
    return js


def quit_table(pid):
    js = requests.post(server + "player-" + str(pid), json={"header": "quit"}).json()
    if js["header"] == "error":
        raise Exception(js["message"])
    return js


def print_hand(hand):
    print("(value " + str(count_cards(hand)) + "):")
    for card in hand["cards"]:
        # print(ranks[card["rank"]] + " of " + colors[card["color"]] + " ")
        print(chr(int("0x1F0" + colors[card["color"]] + ranks[card["rank"]], 16)) + " (" + ranks_names[card["rank"]] + " of " + colors_names[card["color"]] + ")")


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
    1: "1",  # U+1F0x1
    2: "2",  # U+1F0x2
    3: "3",  # U+1F0x3
    4: "4",  # U+1F0x4
    5: "5",  # U+1F0x5
    6: "6",  # U+1F0x6
    7: "7",  # U+1F0x7
    8: "8",  # U+1F0x8
    9: "9",  # U+1F0x9
    10: "A",  # U+1F0xA
    11: "B",  # U+1F0xB (Jack
    12: "D",  # U+1F0xC (Queen)
    13: "E",  # U+1F0xD (King)
}
colors = {
    "D": "C",  # U+1F0Cx
    "S": "A",  # U+1F0Ax
    "H": "B",  # U+1F0Bx
    "C": "D"  # U+1F0Dx
}

ranks_names = {
    1: "1",  # U+1F0x1
    2: "2",  # U+1F0x2
    3: "3",  # U+1F0x3
    4: "4",  # U+1F0x4
    5: "5",  # U+1F0x5
    6: "6",  # U+1F0x6
    7: "7",  # U+1F0x7
    8: "8",  # U+1F0x8
    9: "9",  # U+1F0x9
    10: "Ace",  # U+1F0xA
    11: "Jack",  # U+1F0xB (Jack
    12: "Queen",  # U+1F0xC (Queen)
    13: "King",  # U+1F0xD (King)
}
colors_names = {
    "D": "Diamonts",  # U+1F0Cx
    "S": "Spades",  # U+1F0Ax
    "H": "Hearts",  # U+1F0Bx
    "C": "Clubs"  # U+1F0Dx
}

init_js = register(100)
pid = init_js["id"]
actions = {
    "split": split,
    "double": double,
    "pas": pas,
    "insure": insure,
    "hit": get,
    "quit": quit_table
}
print("Player registered (id " + str(pid) + ")")
while run:
    command = input()
    js = None
    try:
        if command == "join_game":
            print("Type table id: ")
            tid = int(input())
            js = join_game(tid, pid)
        else:
            if command == "quit":
                js = None
            if command in actions.keys():
                js = actions[command](pid)
        if js is not None and js["header"] == "in_game":
            print_table(js)
        elif js is not None and js["header"] == "end_game":
            print_end(js)
    except Exception as e:
        print("Error: " + str(e))
        if js is not None and js["header"] == "in_game":
            print_table(js)
