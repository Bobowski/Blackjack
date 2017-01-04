import requests

server = "http://localhost:5000/"
id = -1;


def enter_game():
    return requests.post(server + "begin", json={"header": "register", "bid": 10})

#TODO add function split
#TODO add function double
#TODO add function pass
#TODO add function insure
#TODO exception handling



print(enter_game().json())

