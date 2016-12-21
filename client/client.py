import requests

state = 0
while():
    if state == 0:
        bid = input("Podaj stawke")
        r = requests.post("http://127.0.0.1:5000/begin",bid)
        state = 1
        # TODO przerobic r.json do zmiennych w kliencie
        if 'id' in r.json():
            cid = r.json()['id']
        print(r.text)
    operation = input("Podaj operacje")
    r = requests.post("http://127.0.0.1:5000/game-"+str(cid),operation)
    print(r.text)

