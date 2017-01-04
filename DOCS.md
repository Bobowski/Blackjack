# Structures
## Client
Client requests may vary depending on game state

**Begin game**
```json
    ActionBegin
    {
        "action": string //must be "register",
        "bid": int
    }
```
**In game**
```json
    ActionInGame
    {
        "action": string //one of the following "split", "insure", "double", "take", "pass"
    }
```

## Server
Server response may vary depending on game state

**In Game**
```json
    TableInGame
    {
        "game_state": string//must be "in_game",
        "insurance": int,
        "hands": [Hand],
        "bid": int,
        "croupier": Hand,
    }
```

## Other structures
```json
    Hand
    {
        "cards": [Card]
    }
```
```json
    Card
    {
        "color": string //onr of the following "Diamonds", "Hearts", "Clubs", "Spades"
        "rank": int //from 1 to 13
    }
```