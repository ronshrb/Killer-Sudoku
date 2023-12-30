class House:
    """
        sets a house, a group of cells.

        Methods:
            __init__ - initializes a house.
            update_cell - updates a cell value in the selected house and the house itself.
            get_all_cells - returns a list of tuples, of two integers between 0 and 8,
                            the first one is the row and the second one if the column of the selected cell.
                            all the house's cells places.
            get_all_values - returns a list of integers between 1 and 9, that are the house's cell values.
    """
    def __init__(self):
        """
        initializes a house
        """
        # a dictionary of the house's cells.
        # the keys are the cells' places, and the values are the cells' values.
        self.cells_dictionary = {}
        self.cells_indexes = list(self.cells_dictionary.keys())  # a list of all the house's cells places
        self.values = list(self.cells_dictionary.values())  # a list of all the house's cells values

    def update_cell(self, place, value):
        """
        updates a cell value in the selected house and the house itself.
        """
        self.cells_dictionary[place] = value
        self.cells_indexes = list(self.cells_dictionary.keys())
        self.values = list(self.cells_dictionary.values())

    def get_all_cells(self):
        """
        returns a list of tuples, of two integers between 0 and 8,
        the first one is the row and the second one if the column of the selected cell.
        all the house's cells places.
        """
        return self.cells_indexes

    def get_all_values(self):
        """
        returns a list of integers between 1 and 9, that are the house's cell values.
        """
        return self.values


