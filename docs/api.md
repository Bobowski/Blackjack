# API Overview

|                       |        |                        |                                       |
|:--------------------- | ------:|:---------------------- |:------------------------------------- |
| [register](#register) | `POST` | `/register`            | Register new player and obtain `uid`. |
| [begin](#begin)       | `POST` | `/player/<uid>/begin`  | Begin new deal with specified `bid`.  |
| [action](#action)     | `POST` | `/player/<uid>/action` | Perform `action`.                     |

# API
Blackjack API is failry simple. Using only three endpoints we are able to play game continously.
To play we first have to [register](#register) our player as return obtaining unique id.
To [begin](#begin) new card deal we have to privide amount of money for bid.
It's now possible to perform one of [actions](#action) in main game loop.

## Register
First you need to register player and obtain `uid` that will allow to perform further actions.

- **URL:**

  `POST` | `/register`
- **Request JSON:**

```javascript
Register
{
    "cash": number
}
```
- **Response JSON:**

```javascript
{
    "header": "confirm_register",
    "uid": number
}
```

## Begin
Beginning new game (deal) is only possible if table is in `awaiting` or `end_game` state.

- **URL:**

  `POST` | `/player/<uid>/begin`
- **Request JSON:**

```javascript
Begin
{
    "bid": number
}
```
- **Response JSON:**

  `Table`
  
## Action
Perform one of available actions.

- **URL:**

  `POST` | `/player/<uid>/action`
- **Request JSON:**

```javascript
Action
{
    "action": string  # split, double_down, stay, hit
}
```
- **Response JSON:**

  `Table`

#### Error Structure
If some operation was not allowed of caused error that should be handled by client then this error message is returned with `400` return code.
```javascript
{
    "header": "error",
    "message": string
}
```

#### Structures
```javascript
Table
{
    "header": "success"
    "state": State,
    "player": Player,
    "croupier": Croupier
}
```

```javascript
State
{
    "phase": string,
    "bid": number,
    "winnings": number
}
```

```javascript
Player
{
    "hands": [Hand],
    "current_hand": Hand,
    "account_balance": number
}
```

```javascript
Croupier
{
    "hand": Hand
}
```

```javascript
Hand
{
    "cards": [Card],
    "value": number,
    "playing": boolean
}
```

```javascript
Card
{
    "color": string,
    "rank": string
}
```