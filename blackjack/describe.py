from blackjack.game.decks import Card
from blackjack.game.players import Hand
from blackjack.game.table import Player, Croupier, State, Table


def card_to_dict(card: Card):
    return {
        "color": card.color if card.face_up else "face_down",
        "rank": card.rank if card.face_up else "face_down"
    }


def hand_to_dict(hand: Hand):
    return {
        "cards": [card_to_dict(card) for card in hand.cards],
        "value": hand.value,
        "playing": hand.playing
    }


def player_to_dict(player: Player):
    return {
        "hands": [hand_to_dict(hand) for hand in player.hands],
        "current_hand": hand_to_dict(player.hand),
        "account_balance": player.account_balance
    }


def croupier_to_dict(croupier: Croupier):
    return {
        "hand": hand_to_dict(croupier.hand)
    }


def state_to_dict(state: State):
    return {
        "phase": state.phase,
        "bid": state.bid,
        "winnings": state.winnings
    }


def table_to_dict(table: Table):
    return {
        "state": state_to_dict(table.state),
        "player": player_to_dict(table.player),
        "croupier": croupier_to_dict(table.croupier)
    }
