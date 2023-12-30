import Board
import pygame
import sys
import time
import EndGame
import KillerSudoku
import LogSheet
from resource_path import resource_path

class Game:
    """
        runs the game window.

        Methods:
            __init__ - initializes display.
            get_ms - takes in seconds and returns minutes and seconds.
            pos_to_place - sets the selected cell.
            handle_mouse_click - takes in the position of where the player clicked and saves it as the selected cell.
            cell_starting_point - returns the starting point of the cell.
            highlight_mistakes - highlights all the cells with mistakes in it.
            draw_highlight - takes in the row and the col numbers of the selected cell and highlights it.
            handle_arrow_keys - takes in an arrow key and saves the selected cell.
            handle_key_input - activates an action based on the pressed key.
            draw_grid - draws vertical and horizontal lines.
            draw_cages - draws the cages and their killer numbers.
            draw_timer - draws the timer.
            draw_title - draws the title.
            draw_level - draws the level (game number - difficulty).
            draw_cell_options - draws cell options.
            draw_cage_options - draws cage options.
            draw_guesses_in_cell - draws guesses in the selected cell.
            draw_number - insert a number into a chosen cell.
            draw_pause - turns the screen into white and pauses the game.
            check_win_condition - checks if the player filled all the right numbers.
            calculate_points - calculates the score.
            save_log - sets the time, score and outcome and adds the game's log to the global log.
            run - runs the program.
    """
    def __init__(self, seed, lvl, user):
        """
        initializes display.
        """
        pygame.init()
        self.screen = pygame.display.set_mode((630, 740))
        pygame.display.set_caption("Killer Sudoku")
        icon = pygame.image.load(resource_path("icon.png"))
        pygame.display.set_icon(icon)
        # grid sizes
        self.top_grid = (0, 0, self.screen.get_width(), 40)  # start weight, start height, end weight, end height
        self.sudoku_grid = (0, 40, 630, 670)
        self.bottom_grid = (0, 630, self.screen.get_width(), self.screen.get_height())
        self.cell_size = self.sudoku_grid[2] // 9
        self.grid_size = 9
        # modes
        self.guess_mode = False
        self.paused = False
        self.cell_options_mode = True
        self.cage_options_mode = True
        self.mistakes_found = []

        self.seed = seed  # game number
        self.lvl = lvl  # difficulty

        self.board = Board.Board(seed, self.lvl)
        self.grid_values = self.board.get_board()
        self.solution = self.board.get_solution()._get_board()

        self.selected_cell = (0, 0)
        self.selected_cell_options = self.board.get_cell(self.selected_cell).get_options()
        self.selected_cell_guesses = self.board.get_cell(self.selected_cell).get_guesses()
        self.selected_cage_options = self.board.get_cell(self.selected_cell).get_cage_options()

        self.last_start_time = time.time()
        self.last_pause_time = 0
        self.paused_total_time = 0
        self.total_time = 0

        self.user = user
        self.log = {
            'User': self.user,
            'Game Number': str(seed),
            'Difficulty': str(lvl),
            'Time': 0,
            'Moves': 0,
            'Hints': 0,
            'Check Board': 0,
            'Mistakes': 0,
            'Score': 0,
            'Outcome': 'loss'
        }

    def get_ms(self, start):
        """
        takes in seconds and returns minutes and seconds.
        """
        elapsed_time = start
        return int(elapsed_time//60), int(elapsed_time%60)

    def pos_to_place(self, pos):
        """
        sets the selected cell
        :param pos: tuple of two integers, stands for a place on the screen.
        """
        sudoku_grid_height_start = self.sudoku_grid[1]
        col = pos[0] // self.cell_size
        row = (pos[1] - sudoku_grid_height_start) // self.cell_size
        return (row, col)


    def handle_mouse_click(self, pos):
        """
        takes in the position of where the player clicked and saves it as the selected cell.
        """
        top, bottom, left, right = (self.sudoku_grid[1], self.sudoku_grid[3], self.sudoku_grid[0], self.sudoku_grid[2])
        # if the player clicked outside of the sudoku grid, do nothing
        if top > pos[1] or bottom < pos[1] or left > pos[0] or right < pos[0]:
            pass
        else:  # set the cell the player click on as the selected cell
            self.selected_cell = self.pos_to_place(pos)

    def cell_starting_point(self, place):
        """
        returns the starting point of the cell.
        :param place: tuple of two integers, the first one is the row of the cell and the second one is the column.
        :return: a tuple with the starting point for our border
        """
        x = place[1] * self.cell_size
        y = place[0] * self.cell_size + self.sudoku_grid[1]

        return x, y


    def highlight_mistakes(self, color=(255, 0, 0)):
        """
        highlights all the cells with mistakes in it.
        """

        for place in self.mistakes_found:
            x, y = self.cell_starting_point(place)
            border_width = 4

            # draws the borders
            # top border
            pygame.draw.rect(self.screen, color, (x, y, self.cell_size, border_width))
            # bottom border
            pygame.draw.rect(self.screen, color,
                             (x, y + self.cell_size - border_width + 2, self.cell_size, border_width))
            # left border
            pygame.draw.rect(self.screen, color, (x, y, border_width, self.cell_size))
            # right border
            pygame.draw.rect(self.screen, color,
                             (x + self.cell_size - border_width + 2, y, border_width, self.cell_size))

    def draw_highlight(self, place, color=(255, 164, 15)):
        """
        takes in the row and the col numbers of the selected cell and highlights it.
        :param place: tuple of two integers, the first one is the row of the cell and the second one is the column.
        """
        if self.guess_mode:
            color = (132, 127, 127)
        x, y = self.cell_starting_point(place)
        border_width = 4

        # draws the borders
        # top border
        pygame.draw.rect(self.screen, color, (x, y, self.cell_size, border_width))
        # bottom border
        pygame.draw.rect(self.screen, color, (x, y + self.cell_size-border_width+2, self.cell_size, border_width))
        # left border
        pygame.draw.rect(self.screen, color, (x, y, border_width, self.cell_size))
        # right border
        pygame.draw.rect(self.screen, color, (x + self.cell_size-border_width+2, y, border_width, self.cell_size))

    def handle_arrow_keys(self, key):
        """
        takes in an arrow key and saves the selected cell.
        """
        row, col = self.selected_cell

        if key in [pygame.K_UP, pygame.K_w]:
            row = (row - 1) % self.grid_size
        elif key in [pygame.K_DOWN, pygame.K_s]:
            row = (row + 1) % self.grid_size
        elif key in [pygame.K_LEFT, pygame.K_a]:
            col = (col - 1) % self.grid_size
        elif key in [pygame.K_RIGHT, pygame.K_d]:
            col = (col + 1) % self.grid_size

        self.selected_cell = (row, col)
    def handle_key_input(self, key):
        """
        activates an action based on the pressed key
        """
        # if the game is paused, dont do anything
        if not self.paused:
            # if the player press a number, insert a number in the selected cell
            if (key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8,
                        pygame.K_9, pygame.K_KP1, pygame.K_KP2, pygame.K_KP3, pygame.K_KP4, pygame.K_KP5, pygame.K_KP6,
                        pygame.K_KP7, pygame.K_KP8, pygame.K_KP9)
                    and self.selected_cell not in self.board.known_cells):
                key_name = pygame.key.name(key)
                if len(key_name) != 1:
                    key_val = int(key_name[1])
                else:
                    key_val = int(key_name)
                # if guess mode is active, insert value as a guess
                if self.guess_mode:
                    self.board.set_cells_guess(self.selected_cell, key_val)
                # if guess mode isn't active, insert value as player's value
                else:
                    self.log["Moves"] = self.log["Moves"] + 1
                    self.board.set_cells_value(self.selected_cell, key_val)
                    if self.selected_cell in self.mistakes_found:
                        self.mistakes_found.remove(self.selected_cell)  # removes the cell from the mistake found list
                    self.grid_values = self.board.get_board()  # updates the cell's options
            # if the player pressed 'h' (for hint), set the cell's value for its true value
            elif key == pygame.K_h and self.selected_cell not in self.board.known_cells:
                self.log["Moves"] = self.log["Moves"] + 1
                self.log["Hints"] = self.log["Hints"] + 1
                self.board.set_cells_value(self.selected_cell, -1)
                self.grid_values = self.board.get_board()
            # if the player pressed 'f' (for find mistakes), highlight the cells with mistakes
            elif key == pygame.K_f:
                self.mistakes_found = self.board.find_mistakes()
                self.log['Check Board'] += 1
                self.log['Mistakes'] += len(self.mistakes_found)
            # deletes the number in the selected cell using backspace
            elif key == pygame.K_BACKSPACE and self.selected_cell not in self.board.known_cells:
                if self.guess_mode:  # if in guess mode, deletes the last guess that was added
                    self.board.get_cell(self.selected_cell).delete_guess()
                else:
                    self.board.set_cells_value(self.selected_cell, 0)
                    self.grid_values = self.board.get_board()  # updates the cell's options
                if self.selected_cell in self.mistakes_found:
                    self.mistakes_found.remove(self.selected_cell)  # removes the cell from the mistake found list
            # if the player press an arrow, move the selected cell
            elif key == pygame.K_SPACE:
                # turn on and off guess mode using "Space"
                self.guess_mode = not self.guess_mode
            elif key == pygame.K_p:  # pauses the game
                self.paused = not self.paused
            elif key == pygame.K_r:  # resets the board
                self.board.reset_board()
            # elif key == pygame.K_c:  # cell options mode
            #     self.cell_options_mode = not self.cell_options_mode
            elif key == pygame.K_c:  # cage options mode
                self.cage_options_mode = not self.cage_options_mode
            elif key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT,
                         pygame.K_w, pygame.K_d, pygame.K_s, pygame.K_a):
                self.handle_arrow_keys(key)
        else:  # if the player press p again, the game continues
            if key == pygame.K_p:
                self.paused = not self.paused


    def draw_grid(self):
        """
        draws vertical and horizontal lines.
        """

        grid_height_start, grid_width_end, grid_height_end = self.sudoku_grid[1], self.sudoku_grid[2], self.sudoku_grid[3]
        grid_height_end = self.sudoku_grid[3]
        for i in range(self.grid_size + 1):
            # draws vertical lines
            if i == 0 or i % 3 == 0:
                pygame.draw.line(self.screen, (0, 0, 0), (i * self.cell_size, grid_height_start),
                                 (i * self.cell_size, grid_height_end),
                                 4)
            else:
                pygame.draw.line(self.screen, (0, 0, 0), (i * self.cell_size, grid_height_start),
                                 (i * self.cell_size, grid_height_end), 2)

            # draws horizontal lines
            if i == 0 or i % 3 == 0:
                pygame.draw.line(self.screen, (0, 0, 0), (0, i * self.cell_size + grid_height_start),
                                 (grid_width_end, i * self.cell_size + grid_height_start),
                                 4)

            else:
                pygame.draw.line(self.screen, (0, 0, 0), (0, i * self.cell_size + grid_height_start),
                                 (grid_width_end, i * self.cell_size + grid_height_start),
                                 2)

    def draw_cages(self):
        """
        draws the cages and their killer numbers
        """
        text_font = pygame.font.SysFont("Gisha", 14)
        grid_height_start = self.sudoku_grid[1]
        for cage in self.board.all_houses.reverse_cages.keys():
            if cage.size == 1:
                pass
            else:
                killer_cell = cage.killer_cell
                killer = cage.killer
                color = cage.color
                cells = cage.cells
                for cell in cells:
                    x = cell[1] * self.cell_size
                    y = cell[0] * self.cell_size
                    pygame.draw.rect(self.screen, color, (x + 6, y + 6 + grid_height_start,
                                                          self.cell_size - 10, self.cell_size - 10))
                    if cell == killer_cell:
                        text = text_font.render(str(killer), True, (0, 0, 0))
                        text_rect = text.get_rect(topleft=(x+7, y + 5 + grid_height_start))
                        self.screen.blit(text, text_rect)

    def draw_timer(self, timer):
        """
        draws the timer
        """
        text_font = pygame.font.SysFont("Gisha", 20)
        x = 3
        y = self.sudoku_grid[1] - 24

        # convert elapsed_time to minutes and seconds
        minutes, seconds = timer
        timer_text = text_font.render(f"{minutes:02d}:{seconds:02d}", True, (0, 0, 0))

        timer_rect = timer_text.get_rect(topleft=(x, y))
        self.screen.blit(timer_text, timer_rect)

    def draw_title(self):
        """
        draws the title.
        """
        grid_height_start = self.sudoku_grid[1]
        text_font = pygame.font.Font(resource_path("GrinchedRegular.ttf"), 38)
        x = self.screen.get_width() // 2
        y = grid_height_start - 18

        text = text_font.render(f"Killer Sudoku", True, (0, 0, 0))
        timer_rect = text.get_rect(center=(x, y))
        self.screen.blit(text, timer_rect)


    def draw_level(self):
        """
        draws the level (game number - difficulty)
        """
        grid_height_start = self.sudoku_grid[1]
        text_font = pygame.font.SysFont("Gisha", 20)
        x = self.screen.get_width() - 3
        y = grid_height_start - 24

        text = text_font.render(f"{self.seed}-{self.lvl}", True, (0, 0, 0))
        timer_rect = text.get_rect(topright=(x, y))
        self.screen.blit(text, timer_rect)

    def draw_cell_options(self):
        """
        draws cell options
        """
        self.selected_cell_options = self.board.get_cell(self.selected_cell).get_options()
        x = self.screen.get_width() // 2
        y = self.screen.get_height() - 85
        text_font = pygame.font.SysFont("Gisha", 18)

        if not self.selected_cell_options:
            text = "No Cell Options"
        else:
            text = f"Cell Options: {str(self.selected_cell_options)[1:-1]}"

        text_render = text_font.render(text, True, (0, 0, 0))
        text_rect = text_render.get_rect(topleft=(3, y))
        self.screen.blit(text_render, text_rect)

    def draw_cage_options(self):
        """
        draws cage options.
        """
        if self.selected_cell in self.board.known_cells:
            pass
        else:
            self.selected_cage_options = self.board.get_cell(self.selected_cell).get_cage().get_options()
            x = self.screen.get_width() // 2
            y = self.screen.get_height() - 55
            text_font = pygame.font.SysFont("Gisha", 16)

            len_of_options = len(self.selected_cage_options)  # number of options

            if len_of_options != 0:  # if the number of options is not 0, get the number of cells in the cage
                len_of_cage = len(self.selected_cage_options[0])

            if len_of_options == 0:  # if there aren't any options, don't draw anything
                pass

            temp_row = ''
            for i, opt in enumerate(self.selected_cage_options):
                if len_of_cage in [6, 7]:
                    if i % 3 == 0 and i != 0:
                        text_render = text_font.render(f"{temp_row[:-1]}", True, (0, 0, 0))
                        text_rect = text_render.get_rect(center=(x, y))
                        self.screen.blit(text_render, text_rect)
                        temp_row = ''
                        y += 20
                else:
                    if i % 5 == 0 and i != 0:
                        text_render = text_font.render(f"{temp_row[:-1]}", True, (0, 0, 0))
                        text_rect = text_render.get_rect(center=(x, y))
                        self.screen.blit(text_render, text_rect)
                        temp_row = ''
                        y += 20
                temp_row += f'{opt}, '
            text_render = text_font.render(f"{temp_row[:-2]}", True, (0, 0, 0))
            text_rect = text_render.get_rect(center=(x, y))
            self.screen.blit(text_render, text_rect)

    def draw_guesses_in_cell(self, place):
        """
        draws guesses in the selected cell
        """
        cell_guesses = self.board.get_cell(place).get_guesses()
        cell_size = self.screen.get_width() // self.grid_size
        text_font = pygame.font.SysFont("Gisha", 12)

        row1, row2, row3 = ['  ', '  ', '  '], ['  ', '  ', '  '], ['  ', '  ', '  ']
        rows = [row1, row2, row3]
        for i, num in enumerate(cell_guesses):
            if num <= 3:
                row1[num-1] = num
            elif num <= 6:
                row2[num-4] = num
            else:
                row3[num - 7] = num

        for j, row in enumerate(rows):
            curr_row = f'{row[0]}   {row[1]}   {row[2]}'
            # curr_row = str(row).replace(', ', "   ")

            # x and y are the coordinates of the center of the cell
            x, y = place[1] * cell_size + cell_size // 2, place[0] * cell_size + cell_size//2 + 15 + 15*(j+1)
            text_render = text_font.render(curr_row, True, (0, 0, 0))
            text_rect = text_render.get_rect(center=(x, y))
            self.screen.blit(text_render, text_rect)

    def draw_number(self, number, place):
        """
        insert a number into a chosen cell
        :param number: int, the cell's value that the player typed in
        :param place: tuple of two integers, the first one is the row of the cell and the second one is the column.
        """
        grid_height_start = self.sudoku_grid[1]
        curr_cage = self.board.get_cell(place).get_cage()
        cage_color = curr_cage.color
        killer = curr_cage.killer
        killer_cell = curr_cage.killer_cell
        cage_size = curr_cage.size

        x = place[1] * self.cell_size
        y = place[0] * self.cell_size
        pygame.draw.rect(self.screen, cage_color, (x + 6, y + 6 + grid_height_start,
                                              self.cell_size - 10, self.cell_size - 10))

        if place == killer_cell and cage_size > 1:
            # text_font = pygame.font.SysFont(resource_path("GrinchedRegular.ttf"), 14)
            text_font = pygame.font.SysFont("Gisha", 14)
            text = text_font.render(str(killer), True, (0, 0, 0))
            text_rect = text.get_rect(topleft=(x + 7, y + 5 + grid_height_start))
            self.screen.blit(text, text_rect)

        # x and y are the coordinates of the center of the cell
        x = place[1] * self.cell_size + self.cell_size // 2
        y = place[0] * self.cell_size + self.cell_size // 2 + grid_height_start

        # text_font = pygame.font.SysFont("couriernew", 32)
        text_font = pygame.font.Font(resource_path("GrinchedRegular.ttf"),32)
        # text_font = pygame.font.SysFont("Gisha",32)
        text = text_font.render(str(number), True, (0, 0, 0))
        text_rect = text.get_rect(center=(x, y))
        self.screen.blit(text, text_rect)

    def draw_pause(self):
        """
        turns the screen into white and pauses the game
        :return:
        """
        self.screen.fill((255, 255, 255))
        font = pygame.font.SysFont("droidsansmono", 60)
        paused_text = font.render("Paused", True, (0, 0, 0))
        text_rect = paused_text.get_rect(center=(315, 380))
        self.screen.blit(paused_text, text_rect)

    def check_win_condition(self):
        """
        checks if the player filled all the right numbers
        :return: Boolean.
        """
        return self.grid_values == self.solution

    def calculate_points(self):
        """
        calculates the score
        """

        initial_score = 6500
        diff_scores = {
            1: 700, 2: 1500, 3: 2300, 4: 3400, 5: 4800, 6: 6000, 7: 7200, 8: 8400, 9: 9200, 10: 10000
        }

        moves_value = self.log["Moves"]
        moves_score = (moves_value-81)*(-10)

        hints_score = self.log["Hints"]*(-300)
        if hints_score == 0:
            hints_score = 500

        check_value = self.log["Check Board"]

        if check_value == 0:
            check_score = 1000
        else:
            check_score = check_value*(-100)

        mistakes_score = self.log["Mistakes"]*(-30)

        time_value = self.log['Time']
        time_value_in_sec = int(time_value[:-3])*60 + int(time_value[-2:])
        time_score = (time_value_in_sec-600)*(-1)

        self.log['Score'] = max(0,(initial_score + diff_scores[self.lvl] + moves_score + hints_score
                             + mistakes_score + time_score + check_score))

    def save_log(self, win=False):
        """
        sets the time, score and outcome and adds the game's log to the global log
        """
        # set time
        logsheet = LogSheet.LogSheet()
        final_time = self.get_ms(self.total_time)
        self.log["Time"] = f"{final_time[0]:02d}:{final_time[1]:02d}"

        # set outcome
        if win:
            self.log['Outcome'] = 'win'
            # set score
            self.calculate_points()
        else:
            self.log['Score'] = 0

        return logsheet.insert_row(self.log)



    def run(self):
        """
        runs the game
        """
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.save_log()
                    KillerSudoku.main(self.user)
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not self.paused:
                    self.handle_mouse_click(pygame.mouse.get_pos())  # get the position where the player clicked on
                elif event.type == pygame.KEYDOWN:
                    self.handle_key_input(event.key)

            self.screen.fill((255, 255, 255))
            if self.paused:
                if not self.last_pause_time:  # save the time the pauses started at
                    self.last_pause_time = time.time()
                self.draw_pause()
                pygame.display.flip()
                continue
            else:
                if self.last_pause_time:  # if the game was resumed, save the total time the game was paused for
                    self.paused_total_time += time.time() - self.last_pause_time
                    self.last_pause_time = 0
                # save the total time of the game minus the time it was paused for
                self.total_time = time.time() - self.last_start_time - self.paused_total_time
                self.draw_timer(self.get_ms(self.total_time))

            self.draw_grid()
            self.draw_cages()
            if self.cage_options_mode:
                self.draw_cage_options()
            self.highlight_mistakes((255, 0, 0))
            self.draw_title()
            self.draw_level()

            # updates all cells
            for row in range(9):
                for col in range(9):
                    place = (row, col)
                    number = self.board.get_cell_value(place)
                    if self.board.get_cell(place).cage.size == 1:
                        number = self.board.get_cell(place).true_value
                    self.draw_guesses_in_cell(place)
                    if number != 0:
                        self.draw_number(number, place)

            # highlights the selected cell
            self.draw_highlight(self.selected_cell)

            if self.check_win_condition():
                log_id = self.save_log(win=True)
                end_window = EndGame.EndGame(self.log['Time'], self.user, log_id, self.log['Score'])
                end_window.run()
                pygame.quit()
                sys.exit()
            else:
                pygame.display.flip()
