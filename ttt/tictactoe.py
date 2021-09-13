
class TicTacToeBoard(object):
    def __init__(self, first_player: str='x'):
        self._ROWS = 3
        self._COLUMNS = 3
        self._CELLS = self._ROWS * self._COLUMNS
        self._state = [['☐' for _ in range(self._COLUMNS)] for _ in range(self._ROWS)]
        self._possible_moves = ['o', 'x']
        self._int_map = {'☐': 0, 'x': 1, 'o': 10}
        self._state_sums = {'rows': [0] * self._ROWS,\
                            'columns': [0] * self._COLUMNS,\
                            'diagonals': [0] * 2}
        self._move_count = 0
        assert first_player in self._possible_moves,\
            '"first_player" should be "o" or "x".'
        self._current_player = first_player
        self._winner = None
    
    def __str__(self) -> str:
        return '\n' + '\n'.join([' '.join(row) for row in self._state])\
                + f'\nWinner: {self._winner}'
    
    def play(self, row: int, column: int) -> bool:
        ''' Checks if cell at "row" and "column" is available
            and if so, plays the move and returns True.
            Otherwise returns False.
        '''
        if self._move_count == self._CELLS:
            return False
        
        assert 0 <= row < len(self._state),\
            f'"row" should be between 0 and {len(self._state) - 1} inclusive.'
        assert 0 <= column < len(self._state[0]),\
            f'"column" should be between 0 and {len(self._state[0]) - 1} inclusive.'

        if self._state[row][column] in self._possible_moves:
            return False
        
        # Update board
        self._state[row][column] = self._current_player
        
        # Update sums
        self._state_sums['rows'][row] += self._int_map[self._current_player]
        self._state_sums['columns'][column] += self._int_map[self._current_player]        
        if row == column:
            self._state_sums['diagonals'][0] += self._int_map[self._current_player]
        if row == len(self._state) - column - 1:
            self._state_sums['diagonals'][1] += self._int_map[self._current_player]
        
        # Update current player
        if self._current_player == 'o':
            self._current_player = 'x'
        else:
            self._current_player = 'o'

        self._update_winner()
        self._move_count += 1

        return True
    
    def _update_winner(self):
        ''' Check if position is final and has winner.
        '''
        if self._winner:
            return self._winner
        
        for line in self._state_sums:
            for sum in self._state_sums[line]:
                if sum == self._ROWS * self._int_map['x']:
                    self._winner = 'x'
                    return
                elif sum == self._ROWS * self._int_map['o']:
                    self._winner = 'o'
                    return
    
    def check_winner(self):
        return self._winner
    
    def finished(self):
        return self._move_count == self._CELLS
    
    def get_player(self):
        return self._current_player


if __name__ == "__main__":
    board = TicTacToeBoard()
    print(board)
    assert board.play(0, 0)
    print(board)
    assert board.play(0, 1)
    print(board)
    assert board.play(1, 0)
    print(board)
    assert not board.play(1, 0)
    print(board)
    assert board.play(0, 2)
    print(board)
    assert board.play(2, 0)
    print(board)
