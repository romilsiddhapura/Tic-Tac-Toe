"""
Created on Sun Oct 21 22:47:16 2018

@author: romil
"""

from Player import Player
from Board import Board, GameResult, NAUGHT, CROSS, EMPTY



class MY_player(Player):
    
    def __init__(self):
        self.side = None
        super().__init__()
        
        
    def move(self, board: Board) -> (GameResult, bool):
        
        
        pos = int(input("Enter your move"))
       # print(pos)
        print(type(self.side))
        _, res, finished = board.move(pos, self.side)
        
    def new_game(self, side: int):
        self.side = side
        
        
    def final_result(self, result: GameResult):
        pass