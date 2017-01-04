# Structures
## Client
Client requests may vary depending on game state

**Begin game**
```javascript
ActionBegin
{
    "action": string //must be "register",
    "bid": number
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

**Begin Game**
```javascript
ID
{
    "game_state": "begin_game",
    "id": number
}
```
**In Game**
```javascript
TableInGame
{
    "game_state": "in_game",
    "insurance": number,
    "hands": [Hand],
    "bid": number,
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
    "rank": number //from 1 to 13
}
```
