import Row, Nonet, Cage
import BoardSolutionCreator
import random
import numpy as np

class Houses:
    """
        Sets a dictionary of houses and link their cells.

        Methods:
            __init__ - initializes a cage.
            get_row - returns the row of the given cell.
            get_col - returns the col of the given cell.
            get_nonet - returns the nonet of the given cell.
            set_cages - assign each cell to a cage with a random number of cells depending on the level
            get_cage - returns the cage of the given cell
    """
    def __init__(self, seed):
        """
        initializes the dictionaries
        """
        self.rows = {
                    0: Row.Row(),
                    1: Row.Row(),
                    2: Row.Row(),
                    3: Row.Row(),
                    4: Row.Row(),
                    5: Row.Row(),
                    6: Row.Row(),
                    7: Row.Row(),
                    8: Row.Row()
                }
        self.cols = {
                    0: Row.Row(),
                    1: Row.Row(),
                    2: Row.Row(),
                    3: Row.Row(),
                    4: Row.Row(),
                    5: Row.Row(),
                    6: Row.Row(),
                    7: Row.Row(),
                    8: Row.Row()
                }
        self.nonets = {
                    0: Nonet.Nonet(),
                    1: Nonet.Nonet(),
                    2: Nonet.Nonet(),
                    3: Nonet.Nonet(),
                    4: Nonet.Nonet(),
                    5: Nonet.Nonet(),
                    6: Nonet.Nonet(),
                    7: Nonet.Nonet(),
                    8: Nonet.Nonet()
                }
        self.cages = {}
        self.reverse_cages = {}
        self.houses = {
            (0, 0): [self.rows[0], self.cols[0], self.nonets[0]],
            (0, 1): [self.rows[0], self.cols[1], self.nonets[0]],
            (0, 2): [self.rows[0], self.cols[2], self.nonets[0]],
            (0, 3): [self.rows[0], self.cols[3], self.nonets[1]],
            (0, 4): [self.rows[0], self.cols[4], self.nonets[1]],
            (0, 5): [self.rows[0], self.cols[5], self.nonets[1]],
            (0, 6): [self.rows[0], self.cols[6], self.nonets[2]],
            (0, 7): [self.rows[0], self.cols[7], self.nonets[2]],
            (0, 8): [self.rows[0], self.cols[8], self.nonets[2]],
            (1, 0): [self.rows[1], self.cols[0], self.nonets[0]],
            (1, 1): [self.rows[1], self.cols[1], self.nonets[0]],
            (1, 2): [self.rows[1], self.cols[2], self.nonets[0]],
            (1, 3): [self.rows[1], self.cols[3], self.nonets[1]],
            (1, 4): [self.rows[1], self.cols[4], self.nonets[1]],
            (1, 5): [self.rows[1], self.cols[5], self.nonets[1]],
            (1, 6): [self.rows[1], self.cols[6], self.nonets[2]],
            (1, 7): [self.rows[1], self.cols[7], self.nonets[2]],
            (1, 8): [self.rows[1], self.cols[8], self.nonets[2]],
            (2, 0): [self.rows[2], self.cols[0], self.nonets[0]],
            (2, 1): [self.rows[2], self.cols[1], self.nonets[0]],
            (2, 2): [self.rows[2], self.cols[2], self.nonets[0]],
            (2, 3): [self.rows[2], self.cols[3], self.nonets[1]],
            (2, 4): [self.rows[2], self.cols[4], self.nonets[1]],
            (2, 5): [self.rows[2], self.cols[5], self.nonets[1]],
            (2, 6): [self.rows[2], self.cols[6], self.nonets[2]],
            (2, 7): [self.rows[2], self.cols[7], self.nonets[2]],
            (2, 8): [self.rows[2], self.cols[8], self.nonets[2]],
            (3, 0): [self.rows[3], self.cols[0], self.nonets[3]],
            (3, 1): [self.rows[3], self.cols[1], self.nonets[3]],
            (3, 2): [self.rows[3], self.cols[2], self.nonets[3]],
            (3, 3): [self.rows[3], self.cols[3], self.nonets[4]],
            (3, 4): [self.rows[3], self.cols[4], self.nonets[4]],
            (3, 5): [self.rows[3], self.cols[5], self.nonets[4]],
            (3, 6): [self.rows[3], self.cols[6], self.nonets[5]],
            (3, 7): [self.rows[3], self.cols[7], self.nonets[5]],
            (3, 8): [self.rows[3], self.cols[8], self.nonets[5]],
            (4, 0): [self.rows[4], self.cols[0], self.nonets[3]],
            (4, 1): [self.rows[4], self.cols[1], self.nonets[3]],
            (4, 2): [self.rows[4], self.cols[2], self.nonets[3]],
            (4, 3): [self.rows[4], self.cols[3], self.nonets[4]],
            (4, 4): [self.rows[4], self.cols[4], self.nonets[4]],
            (4, 5): [self.rows[4], self.cols[5], self.nonets[4]],
            (4, 6): [self.rows[4], self.cols[6], self.nonets[5]],
            (4, 7): [self.rows[4], self.cols[7], self.nonets[5]],
            (4, 8): [self.rows[4], self.cols[8], self.nonets[5]],
            (5, 0): [self.rows[5], self.cols[0], self.nonets[3]],
            (5, 1): [self.rows[5], self.cols[1], self.nonets[3]],
            (5, 2): [self.rows[5], self.cols[2], self.nonets[3]],
            (5, 3): [self.rows[5], self.cols[3], self.nonets[4]],
            (5, 4): [self.rows[5], self.cols[4], self.nonets[4]],
            (5, 5): [self.rows[5], self.cols[5], self.nonets[4]],
            (5, 6): [self.rows[5], self.cols[6], self.nonets[5]],
            (5, 7): [self.rows[5], self.cols[7], self.nonets[5]],
            (5, 8): [self.rows[5], self.cols[8], self.nonets[5]],
            (6, 0): [self.rows[6], self.cols[0], self.nonets[6]],
            (6, 1): [self.rows[6], self.cols[1], self.nonets[6]],
            (6, 2): [self.rows[6], self.cols[2], self.nonets[6]],
            (6, 3): [self.rows[6], self.cols[3], self.nonets[7]],
            (6, 4): [self.rows[6], self.cols[4], self.nonets[7]],
            (6, 5): [self.rows[6], self.cols[5], self.nonets[7]],
            (6, 6): [self.rows[6], self.cols[6], self.nonets[8]],
            (6, 7): [self.rows[6], self.cols[7], self.nonets[8]],
            (6, 8): [self.rows[6], self.cols[8], self.nonets[8]],
            (7, 0): [self.rows[7], self.cols[0], self.nonets[6]],
            (7, 1): [self.rows[7], self.cols[1], self.nonets[6]],
            (7, 2): [self.rows[7], self.cols[2], self.nonets[6]],
            (7, 3): [self.rows[7], self.cols[3], self.nonets[7]],
            (7, 4): [self.rows[7], self.cols[4], self.nonets[7]],
            (7, 5): [self.rows[7], self.cols[5], self.nonets[7]],
            (7, 6): [self.rows[7], self.cols[6], self.nonets[8]],
            (7, 7): [self.rows[7], self.cols[7], self.nonets[8]],
            (7, 8): [self.rows[7], self.cols[8], self.nonets[8]],
            (8, 0): [self.rows[8], self.cols[0], self.nonets[6]],
            (8, 1): [self.rows[8], self.cols[1], self.nonets[6]],
            (8, 2): [self.rows[8], self.cols[2], self.nonets[6]],
            (8, 3): [self.rows[8], self.cols[3], self.nonets[7]],
            (8, 4): [self.rows[8], self.cols[4], self.nonets[7]],
            (8, 5): [self.rows[8], self.cols[5], self.nonets[7]],
            (8, 6): [self.rows[8], self.cols[6], self.nonets[8]],
            (8, 7): [self.rows[8], self.cols[7], self.nonets[8]],
            (8, 8): [self.rows[8], self.cols[8], self.nonets[8]]}
        self.seed = seed
        self.known_cells = []

    def get_row(self, place):
        """
        returns the row of the given cell
        """
        return self.houses[place][0]

    def get_col(self, place):
        """
        returns the col of the given cell
        """
        return self.houses[place][1]

    def get_nonet(self, place):
        """
        returns the nonet of the given cell
        """
        return self.houses[place][2]

    def set_cages(self, level, solution):
        """
        assign each cell to a cage with a random number of cells depending on the level
        :param lvl: an integer, the max size of a cage
        :param solution: the solution grid
        """

        lvl_cages_dict = {
            1: [2, 5, 2, 0, 0, 0, 0, 0, 0],
            2: [3, 4, 5, 1, 0, 0, 0, 0, 0],
            3: [3, 2, 5, 6, 1, 0, 0, 0, 0],
            4: [1, 3, 4, 5, 2, 0, 0, 0, 0],
            5: [1, 3, 3, 6, 4, 2, 0, 0, 0],
            6: [1, 3, 3, 5, 6, 3, 1, 0, 0],
            7: [0, 3, 3, 6, 7, 6, 3, 1, 0],
            8: [0, 3, 3, 3, 7, 8, 5, 4, 1],
            9: [0, 3, 3, 3, 6, 8, 7, 6, 2],
            10: [0, 2, 2, 2, 2, 6, 8, 8, 4]
        }

        lvl_choices = []

        for i, num in enumerate(lvl_cages_dict[level]):
            cage_lvl = i + 1
            for _ in range(num):
                lvl_choices.append(cage_lvl)

        def neighbor_cells(empty_cells, curr_cells, curr_values):
            """
            finds the neighbor cells that don't belong to a cage yet of the cells in curr_cells
            :param empty_cells: a list of tuples, cells that don't belong to any cage yet
            :param curr_cells: a list of tuples, cells we want to find their neighbor cells
            :return: list of the neighbor cells
            """
            neighbors = []
            for curr_cell in curr_cells:
                for i, j in [[-1, 0], [1, 0], [0, 1], [0, -1]]: # checks the cells above, below, and next to the current cell
                    temp_cell = (curr_cell[0] + i, curr_cell[1] + j)
                    if temp_cell in empty_cells:  # if the cell exists or doesn't belong to another cage
                        if solution.get_cell(temp_cell) not in curr_values:  # if there is already the same value in the cage
                            neighbors.append(temp_cell)
            return neighbors

        def get_sum(cage_cells):
            """
            :param cage_cells: tuples with int values, the cage's cells locations
            :return: sum of the cage's cells
            """
            result = 0
            for cage_cell in cage_cells:
                result += solution.get_cell(cage_cell)
            return result

        cells = list(self.houses.keys())
        all_colors = [(188, 143, 143),
                      (107,142,35),
                      (218, 165, 32),
                      (70,130,180),
                      (205, 133, 63),
                      (222, 184, 135),
                      (143,188,143),
                      (221, 160, 221),
                      (102, 221, 170),
                      (255, 99, 71),
                      (255, 165, 0), #t
                      (255, 192, 203),
                      (255, 159, 83),
                      (255, 209, 113),
                      (178, 201, 101),
                      (144, 223, 98),
                      (51, 204, 153),
                      (0, 206, 200),
                      (172, 223, 200),
                      (172, 187, 244),
                      (152, 152, 255),
                      (175, 137, 255),
                      (210, 137, 255),
                      (255, 186, 249),
                      (255, 101, 115),
                      (198, 181, 148),
                      (148, 174, 198),
                      (199, 218, 198)
                      ]

        colors = all_colors.copy()
        random.seed(self.seed)
        while cells:  # while there are still cells that aren't assigned to any cage
            random_lvl = random.choice(lvl_choices)  # chooses a random number of cells the cage will contain
            curr_cage = Cage.Cage(random_lvl)  # creates a new cage
            curr_cage_cells = []  # the cells in the current cage
            curr_values = []  # the values of the cells in our current cage
            for i in range(random_lvl):
                if i != 0:
                    neighbor_cells_list = neighbor_cells(cells, curr_cage_cells, curr_values)
                    if neighbor_cells_list:  # if there are neighbor cells pick one of them randomly
                        random_cell = random.choice(neighbor_cells(cells, curr_cage_cells, curr_values))
                    else:  # if the neighbor cells list is empty, break the loop and create a cage
                        size = len(curr_cage_cells)
                        curr_cage.size = size  # updates the size
                        break
                else:  # choose the first cell in random
                    random_cell = random.choice(cells)
                curr_values.append(solution.get_cell(random_cell))
                self.cages[random_cell] = curr_cage  # adds to cages dictionary the selected cell with the curr cage as its value
                self.houses[random_cell].append(curr_cage)  # adds to houses dictionary the cell's cage
                curr_cage_cells.append(random_cell)
                cells.remove(random_cell)
                self.reverse_cages[curr_cage] = curr_cage_cells
            if len(curr_cage_cells) == 1:
                random_color = (255, 255, 255)
                self.known_cells.append(curr_cage_cells[0])
            else:
                random_color = random.choice(colors)  # picks a color for the background of the current cage
                colors.remove(random_color)   # removes it from the colors list so we won't use it again for another cage
                if len(colors) == 0:
                    colors = all_colors.copy()
            killer = get_sum(curr_cage_cells)
            curr_cage.set_killer(killer)  # sets the killer number
            curr_cage.set_options()
            curr_cage.color = random_color
            curr_cage.cells = curr_cage_cells
            curr_cage.killer_cell = sorted(curr_cage_cells, key=lambda x: (x[0], x[1]))[0]

    def get_cage(self, place):
        """
        returns the cage of the given cell
        """
        return self.houses[place][3]
