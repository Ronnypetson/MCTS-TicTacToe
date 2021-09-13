import unittest
from tictactoe import TicTacToeBoard


class TestTTTBoard(unittest.TestCase):
    def test_limits(self):
        self._ROWS = 3
        self._COLUMNS = 3

        def inner_test(first_player):
            # Trues
            for row in range(self._ROWS):
                for column in range(self._COLUMNS):
                    board = TicTacToeBoard(first_player)
                    self.assertTrue(board.play(row, column))

            # Falsies
            high_out = self._ROWS + 500
            valid = list(range(self._ROWS))
            invalid = [-1, -high_out, high_out, self._ROWS]
            for row in invalid:
                for column in invalid + valid:
                    board = TicTacToeBoard(first_player)
                    with self.assertRaises(AssertionError):
                        board.play(row, column)
                    with self.assertRaises(AssertionError):
                        board.play(column, row)
        
        inner_test('x')
        inner_test('o')
    
    def test_game_end(self):
        self._ROWS = 3
        self._COLUMNS = 3

        def inner_test(first_player):
            second_player = 'x' if first_player == 'o' else 'o'

            # Row-wise, first player wins
            for row in range(self._ROWS):
                board = TicTacToeBoard(first_player)
                row2 = (row + 1) % self._ROWS
                board.play(row, 0)
                board.play(row2, 0)
                board.play(row, 1)
                board.play(row2, 1)
                board.play(row, 2)
                self.assertTrue(board.check_winner() == first_player)
            
            # Column-wise, first player wins
            for column in range(self._COLUMNS):
                board = TicTacToeBoard(first_player)
                column2 = (column + 1) % self._COLUMNS
                board.play(0, column)
                board.play(0, column2)
                board.play(1, column)
                board.play(1, column2)
                board.play(2, column)
                self.assertTrue(board.check_winner() == first_player)
            
            # Diagonals, first player wins
            for diagonal in [(1, 0), (-1, self._ROWS - 1)]:
                board = TicTacToeBoard(first_player)
                for row in range(self._ROWS):
                    column = diagonal[0] * row + diagonal[1]
                    board.play(row, column)
                    board.play((row + 1) % self._ROWS, column)
                self.assertTrue(board.check_winner() == first_player)

            # Row-wise, second player wins
            for row in range(self._ROWS):
                board = TicTacToeBoard(first_player)
                row2 = (row + 1) % self._ROWS
                board.play(row, 0)
                board.play(row2, 0)
                board.play(row, 1)
                board.play(row2, 1)
                board.play((row + 2) % self._ROWS, 0)
                board.play(row2, 2)
                self.assertTrue(board.check_winner() == second_player)
            
            # Column-wise, second player wins
            for column in range(self._COLUMNS):
                board = TicTacToeBoard(first_player)
                column2 = (column + 1) % self._COLUMNS
                board.play(0, column)
                board.play(0, column2)
                board.play(1, column)
                board.play(1, column2)
                board.play(2, (column + 2) % self._COLUMNS)
                board.play(2, column2)
                self.assertTrue(board.check_winner() == second_player)
            
            # Diagonals, second player wins
            for diagonal in [(1, 0), (-1, self._ROWS - 1)]:
                board = TicTacToeBoard(first_player)
                for row in range(self._ROWS):
                    column = diagonal[0] * row + diagonal[1]
                    board.play((row + 1) % self._ROWS, column)
                    board.play(row, column)
                self.assertTrue(board.check_winner() == second_player)
            
            # Draw
            board = TicTacToeBoard(first_player)
            board.play(0, 0)
            board.play(1, 1)
            board.play(1, 0)
            board.play(2, 0)
            board.play(0, 2)
            board.play(0, 1)
            board.play(2, 1)
            board.play(1, 2)
            board.play(2, 2)
            self.assertTrue(board.check_winner() == None)

        inner_test('x')
        inner_test('o')


if __name__ == '__main__':
    unittest.main()
