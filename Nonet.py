from House import House

class Nonet(House):
    """
    Sets a nonet, a type of house.

    Methods:
        __init__ - initializes a nonet.
        update_cell - updates a cell value in the selected house and the house itself.
        get_all_cells - returns a list of tuples, of two integers between 0 and 8,
                        the first one is the row and the second one if the column of the selected cell.
                        all the house's cells places.
        get_all_values - returns a list of integers between 1 and 9, that are the house's cell values.
        """
    def __init__(self):
        super().__init__()
        self.values = []
        self.sum = 45
        self.size = 9
