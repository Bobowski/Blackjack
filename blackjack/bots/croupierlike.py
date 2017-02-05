from blackjack.bots.bot import Bot


b = Bot(cash=1000, seed=11)
wins = 0

for i in range(1000):
    t = b.begin(10)

    if b.state.phase == "end_game":
        continue

    while b.player.current_hand.value <= 16:
        b.hit()

    try:
        b.stand()
    except Exception:
        pass

    if b.state.winnings > 10:
        wins += 1

print(b.player.account_balance)
print(wins)