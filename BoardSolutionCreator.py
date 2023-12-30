import random

class BoardSolutionCreator:
    """
        Creates a sudoku board solution.

        Methods:
            __init__ - initializes a board for the solution.
            is_valid - checks if the given cell can have the given number.
            set_cell - sets the cell's value.
            get_cell - returns the cell.
            find_empty_cell - returns if True if there is an empty cell, else returns false.
            fill_board - fills the board using the backtracking algorithm.
            _get_board - returns the board.
            __str__ - returns a string representation of the solution.
    """

    def __init__(self, seed):
        """
        initializes a board for the solution.
        """
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.seed = seed
        self.all_cells = [(i//9, i % 9) for i in range(81)]

    def is_valid(self, place, val):
        """
        checks if the given cell can have the given number
        :param place: tuple of two integers between 0 and 8, the first one is the row and the second one is the column.
        :param val: integer between 1 and 9, the number we want to insert into the cell.
        :return: boolean, true if we can insert the number, false if not
        """
        row = place[0]
        col = place[1]
        for j in range(9):
            if (self.board[row][j] == val or
                    self.board[j][col] == val or
                    self.board[row - row % 3 + j // 3][col - col % 3 + j % 3] == val):
                return False
        return True

    def set_cell(self, place, val):
        """
        sets the cell's value
        :param place: tuple of two integers between 0 and 8, the first one is the row and the second one is the column.
        :param val: integer between 1 and 9, the number we want to insert into the cell.
        """
        row = place[0]
        col = place[1]
        self.board[row][col] = val

    def get_cell(self, place):
        """
        returns the cell
        :param place: tuple of two integers between 0 and 8, the first one is the row and the second one is the column.
        """
        row = place[0]
        col = place[1]
        return self.board[row][col]

    def find_empty_cell(self):
        """
        returns if True if there is an empty cell, else returns false
        """
        for row in self.board:
            for col in row:
                if col == 0:
                    return True
        return False

    def fill_board(self):
        """
        fills the board using the backtracking algorithm
        """
        for i, place in enumerate(self.all_cells):
            if self.get_cell(place) == 0:  # if the cells is empty, insert a random number
                numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                random.seed(self.seed*(i+1))
                random.shuffle(numbers)
                for num in numbers:
                    if self.is_valid(place, num):  # insert the selected number if it's valid
                        self.set_cell(place, num)
                        if self.fill_board():
                            return True
                        # backtrack if the current number is not valid
                        self.set_cell(place, 0)
                return False
        return True

    def _get_board(self):
        """
        returns the board
        """
        return self.board

    def __str__(self):
        """
        returns a string representation of the solution.
        """
        result = ""
        for i in range(9):
            if i % 3 == 0 and i != 0:
                result += "-" * 21 + "\n"

            for j in range(9):
                if j % 3 == 0 and j != 0:
                    result += "| "

                result += str(self.board[i][j]) + " "
            result += "\n"

        return result
