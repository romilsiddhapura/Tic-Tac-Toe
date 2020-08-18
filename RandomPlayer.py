from Board import Board, GameResult
from Player import Player


class RandomPlayer(Player):
    def __init__(self):
        self.side = None
        super().__init__()

    def move(self, board: Board) -> (GameResult, bool):
        _, res, finished = board.move(board.random_empty_spot(), self.side)
        return res, finished

    def final_result(self, result: GameResult):
        pass

    def new_game(self, side: int):
        self.side = side
