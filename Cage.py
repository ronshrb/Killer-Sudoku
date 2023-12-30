from House import House

class Cage(House):
    """
        Sets a cage, a type of house.

        Methods:
            __init__ - initializes a cage.
            update_cell - updates a cell value in the selected house and the house itself.
            get_all_cells - returns a list of tuples, of two integers between 0 and 8,
                            the first one is the row and the second one if the column of the selected cell.
                            all the house's cells places.
            get_all_values - returns a list of integers between 1 and 9, that are the house's cell values.
            set_killer - sets the killer number of the cage.
            get_killer - returns the killer number of the cage.
            set_options - creates a list of lists.
                          each list contains amount of integers as the size of the cage.
                          each integer is between 1 and 9, and can be used only once in a list.
            get_options - returns the current cage options.
    """
    def __init__(self, size):
        """
        initializes a cage.
        """
        super().__init__()
        self.values = []
        self.cells = []
        self.size = size
        self.killer = 0
        self.curr_cage_options = []
        self.all_cage_options = []
        self.color = (0,0,0)
        self.killer_cell = None

    def set_killer(self, killer):
        """
        sets the killer number of the cage.
        :param killer: integer, the sum of the cage's cells
        """
        self.killer = killer

    def get_killer(self):
        """
        returns the killer number of the cage.
        :param killer: integer, the sum of the cage's cells
        """
        return self.killer


    def set_options(self):
        """
        creates a list of lists.
        each list contains amount of integers as the size of the cage.
        each integer is between 1 and 9, and can be used only once in a list.
        """
        killer = self.killer
        size = self.size
        cage_options = []

        def rec_helper(temp_result, i):
            """
            a recursive function that goes over all the combinations for each cage and saves the ones that are valid
            """
            if sum(temp_result) == killer and len(temp_result) == size:
                cage_options.append(temp_result)
                return
            if sum(temp_result) > killer or len(temp_result) > size:
                return
            if len(temp_result) == size:
                return
            if i == 10:
                return
            rec_helper(temp_result + [i], i+1)
            rec_helper(temp_result, i + 1)

        rec_helper([], 1)

        self.all_cage_options = cage_options
        self.curr_cage_options = cage_options

    def get_options(self):
        """
        returns the current cage options
        """
        if 0 in self.values:
            self.values.remove(0)
        if len(self.values) == 0:  # if the cells are empty, return the original options
            self.curr_cage_options = self.all_cage_options

        else:
            new_options = []
            for option in self.all_cage_options:
                all_values = True
                for val in self.values:  # if there is an option without the value of the cell, drop this option
                    # if val not in option or val not in cells_options:
                    if val not in option:
                        all_values = False
                        break
                if all_values:
                    new_options.append(option)
            self.curr_cage_options = new_options
        return self.curr_cage_options

