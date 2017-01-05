import requests

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


gid = enter_game()
actions = {
    "split": split,
    "double": double,
    "pas": pas,
    "insure": insure
}
print("Game started (id " + str(gid) + ")")
while run:
    command = input()
    try:
        js = actions[command](gid)
        if js["header"] == "in_game":
            print("insurance: "+str(js["insurance"]))
            # for i in range(2):
            #     print("hand"+str(i)+": "+js["hands"][i])
            print("bid: "+str(js["bid"]))
    except Exception as e:
        print("Error: " + str(e))

print(gid)
