from blackjack.bot.cmds import *


cash = 1000
uid = register(cash, 11)["uid"]
wins = 0

for i in range(1000):
    t = begin(uid, 10)

    if t["state"]["phase"] == "end_game":
        continue

    while int(t["player"]["current_hand"]["value"] <= 16):
        t = hit(uid)

    try:
        t = stand(uid)
    except Exception:
        pass

    if t["state"]["winnings"] > 10:
        wins += 1

print(t["player"]["account_balance"])
print(wins)