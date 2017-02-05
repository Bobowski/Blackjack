# API

|          |        |                        |                                       |
|:-------- | ------:|:---------------------- |:------------------------------------- |
| [register](#register) | `POST` | `/register`            | Register new player and obtain `uid`. |
| [begin](#begin)    | `POST` | `/player/<uid>/begin`  | Begin new deal with specified `bid`.  |
| [action](#action)   | `POST` | `/player/<uid>/action` | Perform `action`.                     |


### Register
First you need to register player and obtain `uid` that will allows to perform further actions.

- **URL:**

  `/register`
- **Method:**

  `POST`
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

### Begin
Beginning new game (deal) is only possible if table is in `awaiting` or `end_game` state.

- **URL:**

  `/player/<uid>/begin`
- **Method:**

  `POST`
- **Request JSON:**

```javascript
Begin
{
    "bid": number
}
```
- **Response JSON:**

  `Table`
  
### Action
Perform one of available actions.

- **URL:**

  `/player/<uid>/action`
- **Method:**

  `POST`
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
