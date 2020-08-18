import numpy as np
from enum import Enum


class GameResult(Enum):
    NOT_FINISHED = 0
    NAUGHT_WIN = 1
    CROSS_WIN = 2
    DRAW = 3



EMPTY = 0  
NAUGHT = 1 
CROSS = 2  


BOARD_DIM = 3  # type: int
BOARD_SIZE = BOARD_DIM * BOARD_DIM  # type: int


class Board:

    WIN_CHECK_DIRS = {0: [(1, 1), (1, 0), (0, 1)],
                      1: [(1, 0)],
                      2: [(1, 0), (1, -1)],
                      3: [(0, 1)],
                      6: [(0, 1)]}

    def hash_value(self) -> int:

        res = 0
        for i in range(BOARD_SIZE):
            res *= 3
            res += self.state[i]

        return res

    @staticmethod
    def other_side(side: int) -> int:
        if side == EMPTY:
            raise ValueError("EMPTY has no 'other side'")

        if side == CROSS:
            return NAUGHT

        if side == NAUGHT:
            return CROSS

        raise ValueError("{} is not a valid side".format(side))

    def __init__(self, s=None):
        if s is None:
            self.state = np.ndarray(shape=(1, BOARD_SIZE), dtype=int)[0]
            self.reset()
        else:
            self.state = s.copy()

    def coord_to_pos(self, coord: (int, int)) -> int:
        return coord[0] * BOARD_DIM + coord[1]

    def pos_to_coord(self, pos: int) -> (int, int):
        return pos // BOARD_DIM, pos % BOARD_DIM

    def reset(self):
        self.state.fill(EMPTY)

    def num_empty(self) -> int:
        return np.count_nonzero(self.state == EMPTY)

    def random_empty_spot(self) -> int:
        index = np.random.randint(self.num_empty())
        for i in range(9):
            if self.state[i] == EMPTY:
                if index == 0:
                    return i
                else:
                    index = index - 1

    def is_legal(self, pos: int) -> bool:
        return (0 <= pos < BOARD_SIZE) and (self.state[pos] == EMPTY)

    def move(self, position: int, side: int) -> (np.ndarray, GameResult, bool):
       # print(self.state[position])
        #self.state[position] = side
        if self.state[position] != EMPTY:
            print('Illegal move')
            raise ValueError("Invalid move")
        print(self.state)
        print(position)
        self.state[position] = side

        if self.check_win():
            return self.state, GameResult.CROSS_WIN if side == CROSS else GameResult.NAUGHT_WIN, True

        if self.num_empty() == 0:
            return self.state, GameResult.DRAW, True

        return self.state, GameResult.NOT_FINISHED, False

    def apply_dir(self, pos: int, direction: (int, int)) -> int:
        row = pos // 3
        col = pos % 3
        row += direction[0]
        if row < 0 or row > 2:
            return -1
        col += direction[1]
        if col < 0 or col > 2:
            return -1

        return row * 3 + col

    def check_win_in_dir(self, pos: int, direction: (int, int)) -> bool:
        c = self.state[pos]
        if c == EMPTY:
            return False

        p1 = int(self.apply_dir(pos, direction))
        p2 = int(self.apply_dir(p1, direction))

        if p1 == -1 or p2 == -1:
            return False

        if c == self.state[p1] and c == self.state[p2]:
            return True

        return False

    def who_won(self) -> int:
        for start_pos in self.WIN_CHECK_DIRS:
            if self.state[start_pos] != EMPTY:
                for direction in self.WIN_CHECK_DIRS[start_pos]:
                    res = self.check_win_in_dir(start_pos, direction)
                    if res:
                        return self.state[start_pos]

        return EMPTY

    def check_win(self) -> bool:
        for start_pos in self.WIN_CHECK_DIRS:
            if self.state[start_pos] != EMPTY:
                for direction in self.WIN_CHECK_DIRS[start_pos]:
                    res = self.check_win_in_dir(start_pos, direction)
                    if res:
                        return True

        return False

    def state_to_char(self, pos, html=False):
        if (self.state[pos]) == EMPTY:
            return '&ensp;' if html else ' '

        if (self.state[pos]) == NAUGHT:
            return 'o'

        return 'x'

    def html_str(self) -> str:
        data = self.state_to_charlist(True)
        html = '<table border="1"><tr>{}</tr></table>'.format(
            '</tr><tr>'.join(
                '<td>{}</td>'.format('</td><td>'.join(str(_) for _ in row)) for row in data)
        )
        return html

    def state_to_charlist(self, html=False):
        res = []
        for i in range(3):
            line = [self.state_to_char(i * 3, html),
                    self.state_to_char(i * 3 + 1, html),
                    self.state_to_char(i * 3 + 2, html)]
            res.append(line)

        return res

    def __str__(self) -> str:
        board_str = ""
        for i in range(3):
            board_str += self.state_to_char(i * 3) + '|' + self.state_to_char(i * 3 + 1) \
                         + '|' + self.state_to_char(i * 3 + 2) + "\n"

            if i != 2:
                board_str += "-----\n"

        board_str += "\n"
        return board_str

    def print_board(self):
        for i in range(3):
            board_str = self.state_to_char(i * 3) + '|' + self.state_to_char(i * 3 + 1) \
                        + '|' + self.state_to_char(i * 3 + 2)

            print(board_str)
            if i != 2:
                print("-----")

        print("")
