# Blackjack
Simple client-server Blackjack game.

##Funcionality
Client can play Blackjack with table. There is only one table for each client and one deck for each game.

##Machanics
Client posts requests to different URL and recieves PublicTable structure packed in Json as an answer.


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
      
    def get_rank(self):
      return self.rank
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
```python
  class PublicTable:
    def __init__(self, bid):
      self.insurance = 0
      self.state = 0
      self.client_cards_1 = []
      self.client_cards_2 = []
      self.bid = bid
      self.croupier_cards = [c,] 
```
```python
  class Table:
    def __init__(self, c, bid):
      self.deck = Deck()
      self.croupier_card = self.deck.get_card()
      self.public_table = PublicTable(self.deck, bid)
      self.add_card()
      self.add_card()
      self.game_state = 0
     
    def add_card(self):
      if len(self.public_table.client_cards_2) != 0:
        self.public_table.client_cards_2.append(self.deck.get_card())
      self.public_table.client_cards_1.append(self.deck.get_card())
      self.game_state = 1
      
    def double(self)
      if self.game_state == 0:
        self.public_table.bid *= 2
      self.add_card()
      self.game_state = 1      
      
    def split(self)
      if self.game_state == 0:
        if len(self.public_table.client_cards_1) == 2 and self.public_table.client_cards_1[0].get_rank() == self.public_table.client_cards_1[1].get_rank():
          self.public_table.client_cards_2.append(self.public_table.client_cards_1.pop())
    
    def insure(self):
      if self.game_state == 0:
        if len(self.public_table.croupier_cards) == 1 and (self.public_table.croupier_cards[0].get_rank() == 10 or self.public_table.croupier_cards[0].get_rank() == 11):
          self.public_table.insurance = True   
        
    def pass(self):
        #TODO
```
```json
  {
  "bid": 10,
  "client_cards_1": [
    {
      "color": "H",
      "rank": 10
    },
    {
      "color": "D",
      "rank": 1
    }
  ],
  "client_cards_2": [],
  "croupier_cards": [
    {
      "color": "S",
      "rank": 10
    }
  ],
  "insurance": 0,
  "state": 0
}
```
    
    
