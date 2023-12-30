
class Cell:
    """
        creates a cell.

        Methods:
            __init__ - initializes a cage.
            get_cell - returns the cell.
            get_place - returns a tuple of two integers between 0 and 8,
                        the first one is the row and the second one if the column of the selected cell.
            _set_true_value - sets the true_value to a number between 1 and 9.
            _get_true_value - returns the true_value.
            set_players_value - sets the value the player inserted to the selected cell.
                                if the value is already the cell's value, removes it.
            delete_players_value - deletes the player's value of the selected cell
            check_val - returns boolean, true if the player's value is true, or false if not.
            update_houses - updates the cell's houses.
            update - updates the selected cell's connected_cells, connected cell's values, cage options and the cells options.
            set_guess - add an integer between 1 and 9 to the list of guesses of the selected cell.
                        if the value is already in the list, removes it.
            get_guesses - returns the selected cell's list of guesses.
            delete_guess - deletes the last guess that was inserted to the guesses list.
            delete_all_guesses - deletes the last guess that was inserted to the guesses list.
            get_options - returns the selected cell's options.
            get_cage_options - returns the selected cage's options.
            set_row - sets the selected cell's row.
            get_row - returns the selected cell's row.
            set_col - sets the selected cell's col.
            get_col - returns the selected cell's col.
            set_cage - sets the selected cell's cage.
            get_cage - returns the selected cell's cage.
            set_nonet - sets the selected cell's nonet.
            get_nonet - returns the selected cell's nonet.

    """
    def __init__(self, true_value, place, all_houses):
        """
        initializes a cell
        """
        self.true_value = true_value
        self.players_value = 0
        self.guesses = []
        self.place = place
        self.row = all_houses.get_row(self.place)
        self.col = all_houses.get_col(self.place)
        self.cage = all_houses.get_cage(self.place)
        self.nonet = all_houses.get_nonet(self.place)
        self.connected_cells = list(set(self.row.get_all_cells() + self.col.get_all_cells() +
                                         self.nonet.get_all_cells() + self.cage.get_all_cells()))
        self.connected_cells_values = list(set(self.row.get_all_values() + self.col.get_all_values() +
                                               self.nonet.get_all_values() + self.cage.get_all_values()))
        self.cage_options = self.cage.get_options()
        self.flattened_cage_options = set([num for sublist in self.cage_options for num in sublist])
        # set the cell options to be number that aren't already in the cell's houses and not in the cage options
        self.cell_options = [num for num in range(1, 10) if (num not in self.connected_cells_values and num in self.flattened_cage_options)]

    def get_cell(self):
        """
        returns the cell
        """
        return self
    def get_place(self):
        """
        returns a tuple of two integers between 0 and 8,
        the first one is the row and the second one if the column of the selected cell.
        """
        return self.place

    def _set_true_value(self, value):
        """
        sets the true_value to a number between 1 and 9.
        """
        self.true_value = value

    def _get_true_value(self):
        """
        returns the true_value.
        """
        return self.true_value

    def set_players_value(self, value):
        """
        sets the value the player inserted to the selected cell.
        if the value is already the cell's value, removes it.
        :param value: integer between 1 and 9.
        """
        # if the player's value is the same value that is already in the cell, remove the value
        if self.players_value == value:
            self.players_value = 0
        else:  # else, set a new value for the selected cell
            self.players_value = value
        # update all the cells and houses
        self.update_houses()
        self.update()

    def delete_players_value(self):
        """
        deletes the player's value of the selected cell
        """
        self.set_players_value(0)

    def check_val(self):
        """
        returns boolean, true if the player's value is true, or false if not.
        """
        return self.players_value == self.true_value

    def update_houses(self):
        """
        updates the cell's houses
        """
        self.row.update_cell(self.get_place(), self.players_value)
        self.col.update_cell(self.get_place(), self.players_value)
        self.nonet.update_cell(self.get_place(), self.players_value)
        self.cage.update_cell(self.get_place(), self.players_value)
    def update(self):
        """
        updates the selected cell's connected_cells, connected cell's values, cage options and the cells options
        """
        # update the connected cells
        self.connected_cells = list(
            set(self.row.get_all_cells() + self.col.get_all_cells() + self.nonet.get_all_cells() + self.cage.get_all_cells()))
        self.connected_cells_values = list(
            set(self.row.get_all_values() + self.col.get_all_values() + self.nonet.get_all_values() + self.cage.get_all_values()))
        # update the cage options and the cell options
        self.cage_options = self.cage.get_options()
        self.flattened_cage_options = set([num for sublist in self.cage_options for num in sublist])
        if self.players_value != 0:  # if the player inserted a value, delete the options
            self.cell_options = []
        else:
            # set the cell options to be number that aren't already in the cell's houses and not in the cage options
            self.cell_options = [num for num in range(1, 10) if (num not in self.connected_cells_values and num in self.flattened_cage_options)]

    def set_guess(self, val):
        """
        add an integer between 1 and 9 to the list of guesses of the selected cell.
        if the value is already in the list, removes it.
        :param val: integer between 1 and 9.
        """
        if val not in self.guesses:
            self.guesses.append(val)
        else:
            self.guesses.remove(val)

    def get_guesses(self):
        """
        returns the selected cell's list of guesses.
        """
        return sorted(self.guesses)

    def delete_guess(self):
        """
        deletes the last guess that was inserted to the guesses list.
        """
        self.guesses = self.guesses[:-1]

    def delete_all_guesses(self):
        """
        deletes the last guess that was inserted to the guesses list.
        """
        self.guesses = []

    def get_options(self):
        """
        returns the selected cell's options.
        """
        return self.cell_options

    def get_cage_options(self):
        """
        returns the selected cage's options.
        """
        return self.cage_options

    def set_row(self, row):
        """
        sets the selected cell's row.
        """
        self.row = row

    def get_row(self):
        """
        returns the selected cell's row.
        """
        return self.row

    def set_col(self, col):
        """
        sets the selected cell's column.
        """
        self.col = col

    def get_col(self):
        """
        returns the selected cell's column.
        """
        return self.col

    def set_cage(self, cage):
        """
        sets the selected cell's cage.
        """
        self.cage = cage

    def get_cage(self):
        """
        returns the selected cell's cage.
        """
        return self.cage

    def set_nonet(self, nonet):
        """
        sets the selected cell's nonet.
        """
        self.nonet = nonet

    def get_nonet(self):
        """
        returns the selected cell's nonet.
        """
        return self.nonet

    def __str__(self):
        return f'cell: {self.get_place()}, cell value: {self.players_value}, cell true value: {self._get_true_value()}'

    def __repr__(self):
        return f'cell: {self.get_place()}, cell value: {self.players_value}, cell true value: {self._get_true_value()}'



