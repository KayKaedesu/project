from config import WHITE, BLACK, EMPTY
from copy import deepcopy

class Board(object):

    """rules"""

    def __init__(self):
        """base board"""
        self.board = [[0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 2, 1, 0, 0, 0],
                      [0, 0, 0, 1, 2, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0]]
        # 1 = black, 2 = white(config)
        self.valid_moves = []

    def update(self, i, j):
        return self.board[i][j]

    def lookup(self, row, column, color):
        """returns exists position (horizontal, vertical, diagonal)"""
        if color == BLACK:
            other = WHITE
        else:
            other = BLACK

        places = []

        if row < 0 or row > 7 or column < 0 or column > 7:
            return places

        # for นี่คือหาจุดที่วางได้
        for (x, y) in [
                (-1, 0),
                (-1, 1),
                (0, 1),
                (1, 1),
                (1, 0),
                (1, -1),
                (0, -1),
                (-1, -1)
            ]:
            pos = self.check_direction(row, column, x, y, other)
            if pos:
                places.append(pos)
        return places

    def check_direction(self, row, column, row_add, column_add, other_color):
        i = row + row_add
        j = column + column_add
        if (i >= 0 and j >= 0 and i < 8 and j < 8 and self.board[i][j] == other_color):
            i += row_add
            j += column_add
            while (i >= 0 and j >= 0 and i < 8 and j < 8 and self.board[i][j] == other_color):
                i += row_add
                j += column_add
            if (i >= 0 and j >= 0 and i < 8 and j < 8 and self.board[i][j] == EMPTY):
                return (i, j)

    def get_valid_moves(self, color):
        """get the avaiable positions to put a color"""
        places = []
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == color:
                    places = places + self.lookup(i, j, color)

        places = list(set(places))
        self.valid_moves = places
        return places

    def apply_move(self, move, color):
        """ apply the changes"""
        if move in self.valid_moves:
            self.board[move[0]][move[1]] = color
            for i in range(1, 9):
                self.flip(i, move, color)

    def flip(self, direction, position, color):
        """ แดกนั่นแหละ """

        if direction == 1:
            #north
            row_inc = -1
            col_inc = 0
        elif direction == 2:
            #northeast
            row_inc = -1
            col_inc = 1
        elif direction == 3:
            #east
            row_inc = 0
            col_inc = 1
        elif direction == 4:
            #southeast
            row_inc = 1
            col_inc = 1
        elif direction == 5:
            #south
            row_inc = 1
            col_inc = 0
        elif direction == 6:
            #southwest
            row_inc = 1
            col_inc = -1
        elif direction == 7:
            #west
            row_inc = 0
            col_inc = -1
        elif direction == 8:
            #northwest
            row_inc = -1
            col_inc = -1

        places = []     #pieces to flip
        i = position[0] + row_inc
        j = position[1] + col_inc

        if color == WHITE:
            other = BLACK
        else:
            other = WHITE

        if i in range(8) and j in range(8) and self.board[i][j] == other:
            # assures there is at least one piece to flip
            places = places + [(i, j)]
            i = i + row_inc
            j = j + col_inc
            while i in range(8) and j in range(8) and self.board[i][j] == other:
                # search for more pieces to flip
                places = places + [(i, j)]
                i = i + row_inc
                j = j + col_inc
            if i in range(8) and j in range(8) and self.board[i][j] == color:
                # found a piece of the right color to flip the pieces between
                for pos in places:
                    # flips
                    self.board[pos[0]][pos[1]] = color

    def get_changes(self):
        """ Return black and white counters. """

        whites, blacks, empty = self.count_stones()

        return (self.board, blacks, whites)

    def game_ended(self):
        """ Is the game ended? """
        # board full or wipeout
        whites, blacks, empty = self.count_stones()
        if whites == 0 or blacks == 0 or empty == 0:
            return True

        # no valid moves for both players
        if self.get_valid_moves(BLACK) == [] and \
        self.get_valid_moves(WHITE) == []:
            return True

        return False

    def print_board(self):
        for i in range(8):
            print(i, ' |', end=' ')
            for j in range(8):
                if self.board[i][j] == BLACK:
                    print('B', end=' ')
                elif self.board[i][j] == WHITE:
                    print('W', end=' ')
                else:
                    print(' ', end=' ')
                print('|', end=' ')
            print()

    def count_stones(self):
        """ count หมากในกระดาน """
        whites = 0
        blacks = 0
        empty = 0
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == WHITE:
                    whites += 1
                elif self.board[i][j] == BLACK:
                    blacks += 1
                else:
                    empty += 1
        return whites, blacks, empty

    def compare(self, otherBoard):
        diffBoard = Board()
        diffBoard.board[3][4] = 0
        diffBoard.board[3][3] = 0
        diffBoard.board[4][3] = 0
        diffBoard.board[4][4] = 0
        for i in range(8):
            for j in range(8):
                if otherBoard.board[i][j] != self.board[i][j]:
                    diffBoard.board[i][j] = otherBoard.board[i][j]
        return otherBoard

    def get_adjacent_count(self, color):
        """เช็คว่างข้างๆ"""
        adjCount = 0
        for x, y in [(a, b) for a in range(8) for b in range(8) if self.board[a][b] == color]:
            for i, j in [(a, b) for a in [-1, 0, 1] for b in [-1, 0, 1]]:
                if 0 <= x + i <= 7 and 0 <= y + j <= 7:
                    if self.board[x + i][y + j] == EMPTY:
                        adjCount += 1
        return adjCount

    def next_states(self, color):
        valid_moves = self.get_valid_moves(color)
        for move in valid_moves:
            newBoard = deepcopy(self)
            newBoard.apply_move(move, color)
            yield newBoard
            # yeild = return แต่กลับมาต่อได้
