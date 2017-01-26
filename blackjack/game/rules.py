from typing import List

from blackjack.game.decks import Card


def calculate_hand_value(cards: List(Card)) -> int:
    aces = len([x for x in cards if x.rank == 1])
    value = sum([10 if x.rank > 10 else x.rank for x in cards]) + aces * 10

    if value <= 21 or aces == 0:
        return value

    while aces > 0 and value > 21:
        value -= 10
        aces -= 1
    return value
