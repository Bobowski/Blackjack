from random import Random


class Card:
    colors = ['Diamond', 'Clubs', 'Hearts', 'Spades']
    ranks = list(range(1, 14))

    def __init__(self, color: str, rank: int, face_up: bool=False):
        self.color = color
        self.rank = rank
        self.face_up = face_up

    def __eq__(self, other):
        return self.color == other.color and self.rank == other.rank


class Decks:
    def __init__(self, seed: int=42, count: int=1):
        self.random = Random(seed)
        self.count = count
        self.cards = []
        self._prepare()

    def _prepare(self):
        self.cards = [
            Card(color=color, rank=rank)
            for color in Card.colors
            for rank in Card.ranks
            for _ in range(self.count)
        ]
        self.random.shuffle(self.cards)

    def get(self) -> Card:
        if len(self.cards) == 0:
            self._prepare()
        return self.cards.pop()
