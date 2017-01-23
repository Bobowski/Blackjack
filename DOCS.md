# Structures
## Client
Client requests may vary depending on game state

**Begin game**
```javascript
Register
{
    "header": "register",
    "cash": number
}
```
```javascript
BeginGame
{
    "header": "begin_game",
    "table_id": number,
    "bid": number
}
```
**In game**
```javascript
ActionInGame
{
    "header": string //one of the following "split", "insure", "double", "take", "pass", "quit"
}
```
## Server
Server response may vary depending on game state

```javascript
Error
{
    "header": "error",
    "message": string
}
```
**Begin Game**
```javascript
ID
{
    "header": "confirm_register",
    "id": number,
}
```
**In Game**
```javascript
TableInGame
{
    "header": "in_game",
    "insurance": number,
    "hands": [Hand],
    "bid": number,
    "croupier": Hand
}
```
**End Game**
```javascript
TableEndGame
{
    "header": "end_game",
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