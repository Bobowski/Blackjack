from random import Random
from typing import List


class Card:
    colors = ['Diamond', 'Clubs', 'Hearts', 'Spades']
    ranks = list(range(1, 14))

    def __init__(self, color: str, rank: int, face_up: bool=False):
        self.color = color
        self.rank = rank
        self.face_up = face_up

    # def to_dict(self):
    #     return {
    #         "color": self.color if self.face_up else "face_down",
    #         "rank": self.rank if self.face_up else "face_down"
    #     }


class Decks:
    def __init__(self, seed: int=42):
        self.random = Random(seed)
        self.cards = []

    def get(self) -> Card:
        if len(self.cards) == 0:
            self.cards = [
                Card(color=color, rank=rank)
                for color in Card.colors
                for rank in Card.ranks
            ]
            self.random.shuffle(self.cards)
        return self.cards.pop()
