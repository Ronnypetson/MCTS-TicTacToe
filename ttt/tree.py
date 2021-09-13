from copy import deepcopy
from tictactoe import TicTacToeBoard


class TTTState:
    def __init__(self, board: TicTacToeBoard, depth: int = 0):
        self.board = board
        self.Q = 0
        self.N = 0
        self.parent = None
        self.children = []
        self.depth = depth
        self.visited = False
        self.expanded = False
    
    def increase_Q(self):
        self.Q += 1

    def increase_N(self):
        self.N += 1
    
    def increase_draw(self):
        self.Q += 0.5
        self.N += 0.5
    
    def set_children(self):
        for row in range(self.board._ROWS):
            for column in range(self.board._COLUMNS):
                board = deepcopy(self.board)
                if board.play(row, column):
                    child = TTTState(board, self.depth + 1)
                    child.parent = self
                    self.children.append(child)
    
    def is_expanded(self):
        unvisited_children = [child for child in self.children if not child.visited]
        if len(unvisited_children) == 0:
            self.expanded = True
        return self.expanded
