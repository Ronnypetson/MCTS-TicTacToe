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
        ''' Increases Q by 1, the number of (simulated) wins from the current
            position for the last player (not current player).
        '''
        self.Q += 1

    def increase_N(self):
        ''' Increases N by 1, the number of simulated matches finished from the
            current position.
        '''
        self.N += 1
    
    def increase_draw(self):
        ''' Increases both N and Q by 0.5, reflecting the simulated draws from
            the current position.
        '''
        self.Q += 0.5
        self.N += 0.5
    
    def set_children(self):
        ''' Sets up the node children (possible next states) if not set already.
        '''
        # self.children must be set only once.
        if len(self.children) > 0:
            return
        for row in range(self.board._ROWS):
            for column in range(self.board._COLUMNS):
                board = deepcopy(self.board)
                if board.play(row, column):
                    child = TTTState(board, self.depth + 1)
                    child.parent = self
                    self.children.append(child)
    
    def is_expanded(self):
        ''' Checks if all of the node's children are visited.
            If the node hasn't any children (terminal state), returns False.
        '''
        if len(self.children) == 0:
            return False
        unvisited_children = [child for child in self.children if not child.visited]
        if len(unvisited_children) == 0:
            self.expanded = True
        return self.expanded
