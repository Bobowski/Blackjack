import requests

server = "http://localhost:5000/"
id = -1;


def enter_game():
    return requests.post(server + "begin", json={"action": "register", "bid": 10})

print(enter_game().json())


# state = 0
# while ():
#     if state == 0:
#         bid = input("Podaj stawke")
#         r = requests.post("http://127.0.0.1:5000/begin", bid)
#         state = 1
#         # TODO przerobic r.json do zmiennych w kliencie
#         if 'id' in r.json():
#             cid = r.json()['id']
#         print(r.text)
#     operation = input("Podaj operacje")
#     r = requests.post("http://127.0.0.1:5000/game-" + str(cid), operation)
#     print(r.text)
