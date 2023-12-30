import Cell
import BoardSolutionCreator
import Houses

class Board:
    """
        Board creates the sudoku board.

        Methods:
            __init__ - initializes a new sudoku board.
            get_board - returns the board.
            get_solution - returns the solution.
            get_cell - given a place of the cell, returns it.
            get_cell_value - returns the given cell's value.
            set_cells_value - sets the given cell's value
            update_all_cells - updates all the cells in the grid
            set_cells_guess - sets the cell's guesses
            find_mistakes - returns all the cells places with mistakes in them
            reset_board - resets the values the player inserted
            __str__ - returns a string representation of the board.
    """
    def __init__(self, seed, lvl):
        """
        initializes a new sudoku board.
        """
        self.solution = BoardSolutionCreator.BoardSolutionCreator(seed)
        self.solution.fill_board()
        self.all_houses = Houses.Houses(seed)
        self.all_houses.set_cages(lvl, self.solution)
        self.cells = [[Cell.Cell(self.solution.get_cell((row, col)), (row, col), self.all_houses) for col in range(9)] for row in range(9)]
        self.board = [[self.cells[i][j].players_value for i in range(9)] for j in range(9)]
        self.places = [(i//9, i % 9) for i in range(81)]
        self.known_cells = self.all_houses.known_cells  # all the cells that belong to a cage with only 1 cell
        for cell in self.known_cells:  # sets the value each one of the known cells as its true value
            self.set_cells_value(cell, self.get_cell(cell).true_value)


    def get_board(self):
        """
        returns the board.
        """
        return self.board

    def get_solution(self):
        """
        returns the solution.
        """
        return self.solution

    def get_cell(self, place):
        """
        given a place of the cell, returns it.
        :param place: tuple of two integers, the first one is the row of the cell and the second one is the column.
        :return: cell type, the cell in the given place.
        """
        row = place[0]
        col = place[1]
        return self.cells[row][col]

    def get_cell_value(self, place):
        """
        returns the given cell's value.
        :param place: tuple of two integers, the first one is the row of the cell and the second one is the column.
        :return: integer, the cell's value.
        """
        return self.get_cell(place).players_value

    def set_cells_value(self, place, val=-1):
        """
        sets the given cell's value
        :param place: tuple of two integers, the first one is the row of the cell and the second one is the column.
        :param val: integer, value between 1 and 9. if the value is -1, it sets the cell's value to be its true value.
        """
        row = place[0]
        col = place[1]
        if val == -1:  # sets the cell's value to be its true value
            val = self.get_cell(place).true_value
        self.get_cell(place).set_players_value(val)
        self.board[row][col] = val
        self.update_all_cells()

    def update_all_cells(self):
        """
        updates all the cells in the grid
        """
        for row in self.cells:
            for cell in row:
                cell.update()

    def set_cells_guess(self, place, val):
        """
        sets the cell's guesses
        """
        self.get_cell(place).set_guess(val)

    def find_mistakes(self):
        """
        returns all the cells places with mistakes in them
        """
        cells_with_mistakes = []
        for place in self.places:
            curr_cell = self.get_cell(place)
            if curr_cell.players_value != curr_cell._get_true_value() and curr_cell.players_value != 0:
                cells_with_mistakes.append(place)
        return cells_with_mistakes

    def reset_board(self):
        """
        resets the values the player inserted
        """
        for place in self.places:
            if place not in self.known_cells:
                self.set_cells_value(place, 0)
                self.get_cell(place).delete_all_guesses()
                self.get_cell(place).update()


    def __str__(self):
        """
        returns a string representation of the board.
        """
        result = ""
        for i in range(9):
            if i % 3 == 0 and i != 0:
                result += "-" * 21 + "\n"

            for j in range(9):
                if j % 3 == 0 and j != 0:
                    result += "| "

                result += str(self.get_cell_value((i, j))) + " "
            result += "\n"

        return result




