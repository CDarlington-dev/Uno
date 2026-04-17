from typing import Optional
import random

class Card:
    def __init__(self, color: Optional[str], number: Optional[int] = None) -> None:
        self.number = number
        self.color = color
        
        


class Board:
    def __init__(self, players: int, startingCards: Optional[int] = 7) -> None:
        self.remaining = []
        colors = 'RGBY'
        for i in range(1,10):
            for color in colors:
                self.remaining.append(color + str(i))
                self.remaining.append(color + str(i))

        for color in colors:
            self.remaining.append(color + str(0))
        

        for color in colors:
            for i in range(2):
                self.remaining.append(color + 'S') #Skip
                self.remaining.append(color + 'R') #Reverse
                self.remaining.append(color + '+2') #+2
        
        for i in range(4):
            self.remaining.append('W') #play with <color|W> ex) RW, YW, RW+4, YW+4 -> keep color consistent
            self.remaining.append('W+4')
        random.shuffle(self.remaining)
        firstCard = 107
        while self.remaining[firstCard] == 'W+4':
            firstCard -= 1

        self.order = 1
        self.drawPile = [self.remaining.pop(firstCard)]
        if self.is_special(self.drawPile[0]):
            self.handle_special(self.drawPile[0], True)
        
        self.turn = 0
        self.players = players
        self.hands = [[] for _ in range(players)]
        
        
         
    def shuffle(self) -> None:
        self.remaining = self.drawPile[:-1]
        self.drawPile = [self.drawPile[-1]] #keep only top card
        random.shuffle(self.remaining)
    
    def draw(self) -> str:
        if self.remaining:
            self.hands[self.turn].append(self.remaining.pop())
            return self.hands[self.turn][-1]

        self.shuffle()
        if not self.remaining:
            return ''

        self.hands[self.turn].append(self.remaining.pop())
        return self.hands[self.turn][-1]
    
    def is_special(self, play:str):
        if len(play) == 2 and play[1] == 'R': #reverse
            return True

        if len(play) == 3 and play[1:] == '+2': #+2
            return True
        
        if len(play) == 3 and play[1:] == '+4': #+4
            return True

        if len(play) == 2 and play[1] == 'S': #Skip
            return True

    def handle_special(self, play:str, firstCard:bool):
        if len(play) == 2 and play[1] == 'R': #reverse
            self.order *= -1


        if not firstCard and self.players > 2: #2 players/first player don't skip
            self.turn = (self.turn + self.order) % 4

        if len(play) == 3 and play[1:] == '+2':
            self.draw()
            self.draw()
            self.turn = (self.turn + self.order) % 4
        
        if len(play) == 3 and play[1:] == '+4':
            self.draw()
            self.draw()
            self.draw()
            self.draw()
            self.turn = (self.turn + self.order) % 4

        if len(play) == 2 and play[1] == 'S':
            self.turn = (self.turn + self.order) % 4

    def play(self, play:str) -> str:
        if play == 'd':
            res = self.draw()
            self.turn = (self.turn + self.order) % 4
            return res

        self.hands[self.turn].remove(play)
        self.drawPile.append(play)

        if len(self.hands[self.turn]) == 0:
            return 'Win'
        

        if(self.is_special(play)):
            self.handle_special(play, False)
        
        
        return 'No Win'
    
    def playable(self):
        
        topCard = self.drawPile[-1]
        if topCard == 'W':
            return self.hands[self.turn]
        
        res = []
        for card in self.hands[self.turn]:
            if card == 'W' or card == 'W+4':
                res.append(card)
                continue
            
            if card[1:] == topCard[1:]:
                res.append(card)
                continue
            
            if card[0] == topCard[0]:
                res.append(card)
                continue
        
        return res
            
            

            

        

    

    

if __name__ == "__main__":
    game = Board(2)


