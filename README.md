# Blackjack
Simple client-server Blackjack game.

##Funcionality
Client can play Blackjack with table. There is only one table for each client and one deck for each game.

##Machanics
Client posts requests to different URL and recieves TableState structure packed in Json as an answer.


**Types of requests:**
  1. **Begin game**
    * URL: http://[server]:[port]/begin 
    * Message: '[bid]'
    * Result: Server generates new ID for client and creates new Table structure.    
  2. **Split** *(Optional, only if it's the first move)*
    * URL: http://<server>:<port>/game-[client ID]
    * Message: 'SPLIT'
    * Result: If player has two equal cards, server splits player card set into two separate sets. From now on player has two card sets.
  3. **Insure** *(Optional, only if it's the first move)*
    * URL: http://<server>:<port>/game-[client ID]
    * Message: 'INSURE'
    * Result: If croupier has ace or 10, server marks boolean insured in Table. If croupier wins, client receives his bid back. 
  4. **Double** *(Optional, only if it's the first move)*
    * URL: http://<server>:<port>/game-[client ID]
    * Message: 'DOUBLE'
    * Result: Player doubles his bid.
  5. **Take**
    * URL: http://<server>:<port>/game-[client ID]
    * Message: 'TAKE'
    * Result: Player receives new card.
  6. **Pass**
    * URL: http://<server>:<port>/game-[client ID]
    * Message: 'PASS'
    * Result: Game ends. Croupier makes his moves, and server evaluates who wins.
    
    
**Structures:**
```python
  class Card:
    def __init__(self, color, rank) 
      #color - 'D' Diamonds, 'C' Clubs, 'H' Hearts, 'S' Spades
      #rank - number from 1 to 13
      self.color = color
      self.rank = rank
```
```python
  from random import shuffle
  class Deck:
    def __init__(self):
      self.cards = [];
      colors = ['D','C','H','S']
      for c in colors
        for r in range(1,14)
          self.cards.append(Card(c,r))
    def shuffle(self):
      shuffle(self.cards)
    def get_card(self):
      return self.cards.pop()
```

    
    
