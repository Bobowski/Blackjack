# Structures
## Client
Client requests may vary depending on game state

**Begin game**
```javascript
    ActionBegin
    {
        "action": string //must be "register",
        "bid": int
    }
```
**In game**
```javascript
    ActionInGame
    {
        "action": string //one of the following "split", "insure", "double", "take", "pass"
    }
```

## Server
Server response may vary depending on game state

**In Game**
```javascript
    TableInGame
    {
        "game_state": "in_game",
        "insurance": int,
        "hands": [Hand],
        "bid": int,
        "croupier": Hand,
    }
```
**End Game**
```javascript
    TableEndGame
    {
        "game_state": "end_game",
        "winner": string //player or croupier
        "winning_hand": Hand
    }
```


## Other structures
```javascript
    Hand
    {
        "cards": [Card]
    }
```
```javascript
    Card
    {
        "color": string, //onr of the following "Diamonds", "Hearts", "Clubs", "Spades"
        "rank": int //from 1 to 13
    }
```
