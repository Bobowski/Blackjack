from blackjack.bots.cmds import *


for j in range(100):
    cash = 10000
    uid = register(cash, j)["uid"]
    wins = 0

    for i in range(1000):
        t = begin(uid, 10)

        first_card = 0
        second_card = 0

        if t["state"]["phase"] == "end_game":
            continue

        for card in t["player"]["current_hand"]["cards"]:
            if first_card == 0:
                first_card = card["rank"]
            else:
                second_card = card["rank"]

        if first_card == second_card:
            t = split(uid)


        first_hand, second_hand = t["player"]["hands"]

        if second_hand["value"] == 0:
            while int(t["player"]["current_hand"]["value"] <= 16):
                t = hit(uid)

        else:
            while first_hand["value"] <= 16 and second_hand["value"] <= 16:
                if int(t["player"]["current_hand"]["value"] <= 16):
                    try:
                        t = hit(uid)
                    except Exception:
                        pass
                elif int(t["player"]["current_hand"]["value"] <= 16):
                    try:
                        t = hit(uid)
                    except Exception:
                        pass
                else:
                    break

            first_hand, second_hand = t["player"]["hands"]

        try:
            t = stand(uid)
            t = stand(uid)
        except Exception:
            pass

        if 20>= t["state"]["winnings"] > 10:
            wins += 1
        elif t["state"]["winnings"] >20:
            wins += 2
    print(j,".",t["player"]["account_balance"]," / ",wins)

