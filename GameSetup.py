import random
import pygame
import sys
import webbrowser
import Button
import GlobalStats
import UserStats
from resource_path import resource_path


class GameSetup:
    """
            runs the start menu window.

            Methods:
                __init__ - initializes display.
                draw_title - draws the title.
                draw_linkedin - draws linkedin.
                draw_rules - draws the rules of the game.
                draw_instructions - draws the instructions of the game.
                draw_buttons - draws the buttons of the game.
                input - handles the input the player inserted.
                draw_highlight - highlights the selected button.
                handle_key_input - lets the player pick cells using the keyboard, to insert input and to delete input.
                handle_mouse_click - takes in the position of where the player clicked and saves it as the selected cell.
                activate_start - starts the game,
                                 if the player didn't fill the game number and the level number, fill it randomly.
                activate_user_stats - opens the user statistics window.
                activate_global_stats - opens the global statistics window.
                run - runs the program.
        """
    def __init__(self, user=''):
        """
        initializes display.
        """
        pygame.init()
        self.screen = pygame.display.set_mode((700, 640))
        pygame.display.set_caption("KS - Menu")
        icon = pygame.image.load(resource_path("icon.png"))
        pygame.display.set_icon(icon)
        self.clock = pygame.time.Clock()
        self.user = user

        self.buttons = {
            "game_number": Button.Button((30, 450, 190, 49), pic='user_unselected.png', selected='user_selected.png', unselected='user_unselected.png'),
            "level_number": Button.Button((260, 450, 190, 49), pic='user_unselected.png', selected='user_selected.png',unselected='user_unselected.png'),
            "start_game": Button.Button((240, 540, 192, 96), pic='start.png'),
            "linkedin": Button.Button((640, 10, 45, 44), pic="lk.png"),
            "username": Button.Button((490, 450, 190, 49), user, pic='user_unselected.png', selected='user_selected.png', unselected='user_unselected.png'),
            "user stats": Button.Button((50, 555, 112, 70), pic='user stats.png'),
            "global stats": Button.Button((515, 555, 112, 70), pic='global stats.png')
        }
        self.selected_button = None

    def draw_title(self):
        """
        draws the title
        """
        img = pygame.image.load(resource_path("logo2.png")).convert()
        self.screen.blit(img, (80, 10))
    def draw_linkedin(self):
        """
        draws linkedin
        """
        linkedin_logo = pygame.image.load(resource_path(f"{self.buttons['linkedin'].pic}")).convert()
        self.screen.blit(linkedin_logo, (self.buttons["linkedin"].place[0], self.buttons["linkedin"].place[1]))
    def draw_rules(self):
        """
        draws the rules of the game
        """
        font = pygame.font.SysFont("Gisha", 22)
        rules_title = font.render("Rules:", True, (0, 0, 0))

        wikipedia_rules = (
            "The objective is to fill the grid with numbers from 1 to 9,",
            "in a way that the following conditions are met:",
            "  - Each row, column, and nonet contains each number exactly once.",
            "  - Sum of all numbers in a cage must match the small number in its corner.",
            "  - No number appears more than once in a cage.",
        )

        font = pygame.font.SysFont("Gisha", 20)
        lines = [font.render(line, True, (0, 0, 0)) for line in wikipedia_rules]
        lines_rects = [text.get_rect(topleft=(40, 180 + i * 30)) for i, text in enumerate(lines)]

        self.screen.blit(rules_title, (30, 150))
        for line, rect in zip(lines, lines_rects):
            self.screen.blit(line, rect)

    def draw_instructions(self):
        """
        draws the instructions of the game
        """
        font = pygame.font.SysFont("Gisha", 22)
        inst_title = font.render("How To Play?", True, (0, 0, 0))

        lines = (
            "  Space - Toggle guess mode        F - Check board       H - Hint",
            "  C - Toggle cage options              R - Reset board        P - Pause"
        )

        font = pygame.font.SysFont("Gisha", 20)
        inst_lines = [font.render(line, True, (0, 0, 0)) for line in lines]
        lines_rects = [text.get_rect(topleft=(40, 370 + i * 30)) for i, text in enumerate(inst_lines)]

        self.screen.blit(inst_title, (30, 340))
        for line, rect in zip(inst_lines, lines_rects):
            self.screen.blit(line, rect)

    def draw_buttons(self):
        """
        draws the buttons of the game
        """
        start_img = pygame.image.load(resource_path(f"{self.buttons['start_game'].pic}")).convert_alpha()
        global_img = pygame.image.load(resource_path(f"{self.buttons['global stats'].pic}")).convert_alpha()
        user_img = pygame.image.load(resource_path(f"{self.buttons['user stats'].pic}")).convert_alpha()
        username_pic = pygame.image.load(resource_path(f"{self.buttons['username'].pic}")).convert_alpha()
        game_number = pygame.image.load(resource_path(f"{self.buttons['game_number'].pic}")).convert_alpha()
        level_number = pygame.image.load(resource_path(f"{self.buttons['level_number'].pic}")).convert_alpha()

        self.screen.blit(username_pic,
                         (self.buttons["username"].place[0],self.buttons["username"].place[1]))
        self.screen.blit(game_number,
                         (self.buttons["game_number"].place[0],self.buttons["game_number"].place[1]))
        self.screen.blit(level_number,
                         (self.buttons["level_number"].place[0],self.buttons["level_number"].place[1]))
        self.screen.blit(start_img, (self.buttons["start_game"].place[0] + 10, self.buttons["start_game"].place[1]))
        self.screen.blit(global_img, (self.buttons["global stats"].place[0] + 10, self.buttons["global stats"].place[1]))
        self.screen.blit(user_img, (self.buttons["user stats"].place[0] + 10, self.buttons["global stats"].place[1]))

        if self.buttons['username'].value == '' and self.selected_button != 'username':
            x = self.buttons['username'].place[0] + 33
            y = self.buttons['username'].place[1] + 23
            text_font = pygame.font.SysFont("myriad", 30)
            text = text_font.render(f'USERNAME', True, (0, 0, 0))
            text_rect = text.get_rect(midleft=(x, y))
            self.screen.blit(text, text_rect)
        if not self.buttons['game_number'].value and self.selected_button != 'game_number':
            x = self.buttons['game_number'].place[0] + 11
            y = self.buttons['game_number'].place[1] + 24
            text_font = pygame.font.SysFont("myriad", 30)
            text = text_font.render('GAME NUMBER', True, (0, 0, 0))
            text_rect = text.get_rect(midleft=(x, y))
            self.screen.blit(text, text_rect)
        if not self.buttons['level_number'].value and self.selected_button != 'level_number':
            x = self.buttons['level_number'].place[0] + 1
            y = self.buttons['level_number'].place[1] + 24
            text_font = pygame.font.SysFont("myriad", 30)
            text = text_font.render('DIFFICULTY (1-10)', True, (0, 0, 0))
            text_rect = text.get_rect(midleft=(x, y))
            self.screen.blit(text, text_rect)

    def input(self, button_name, val):
        """
        handles the input the player inserted
        :param button_name: the selected cell
        :param val: the value inserted by the player
        """
        button = self.buttons[button_name]
        if button_name == 'username':
            if len(button.value) < 12:
                button.value += val
        else:
            if button.value == 0:
                button.value = None
            elif button.value is None:
                button.value = int(val)
            else:
                button.value = int(f'{button.value}{val}')
                if button_name == "level_number":
                    button.value = min(10, button.value)

        self.user = self.buttons['username'].value

    def draw_input(self):
        """
        draws the number that was inserted into the selected cell
        """
        for button_name in self.buttons.keys():
            button = self.buttons[button_name]
            place = button.place
            val = button.value
            if val is None:
                val = ''
            x = place[0] + 2
            y = place[1] + 24
            font_size = 20
            text_font = pygame.font.SysFont("couriernew", font_size)
            text = text_font.render(f'{val}', True, (0, 0, 0))
            text_rect = text.get_rect(midleft=(x, y))
            self.screen.blit(text, text_rect)

    def draw_highlight(self):
        """
        highlights the selected button
        """
        for button_name in self.buttons:
            curr_button = self.buttons[button_name]
            if not curr_button.unselected:
                continue
            elif button_name == self.selected_button:
                curr_button.pic = curr_button.selected
            elif button_name != self.selected_button:
                curr_button.pic = curr_button.unselected

    def handle_key_input(self, key):
        """
        lets the player pick cells using the keyboard, to insert input and to delete input
        """

        if self.selected_button == 'username':
            if key in (
                    pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8,
                    pygame.K_9, pygame.K_0, pygame.K_KP1, pygame.K_KP2, pygame.K_KP3, pygame.K_KP4, pygame.K_KP5,
                    pygame.K_KP6,
                    pygame.K_KP7, pygame.K_KP8, pygame.K_KP9, pygame.K_KP0
            ) or (pygame.K_a <= key <= pygame.K_z):
                key_name = pygame.key.name(key)
                if len(key_name) != 1:
                    key_val = key_name[1]
                else:
                    key_val = key_name
                self.input(self.selected_button, key_val)
            elif key == pygame.K_BACKSPACE: # use backspace to delete input
                curr_val = self.buttons[self.selected_button].value
                if len(curr_val) in [1, 0]:
                    self.buttons[self.selected_button].value = ''
                else:
                    self.buttons[self.selected_button].value = self.buttons[self.selected_button].value[:-1]
        elif key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8,
                     pygame.K_9, pygame.K_0, pygame.K_KP1, pygame.K_KP2, pygame.K_KP3, pygame.K_KP4, pygame.K_KP5,
                     pygame.K_KP6, pygame.K_KP7, pygame.K_KP8, pygame.K_KP9, pygame.K_KP0):
            key_name = pygame.key.name(key)
            if len(key_name) != 1:
                key_val = key_name[1]
            else:
                key_val = key_name
            self.input(self.selected_button, key_val)
        elif key == pygame.K_BACKSPACE:  # use backspace to delete input
            curr_val = self.buttons[self.selected_button].value
            if curr_val is None:
                pass
            elif len(str(curr_val)) in [1,0]:
                self.buttons[self.selected_button].value = None
            else:
                self.buttons[self.selected_button].value = int(str(self.buttons[self.selected_button].value)[:-1])

    def handle_mouse_click(self, pos):
        """
        takes in the position of where the player clicked and saves it as the selected cell.
        """
        for button_name in self.buttons.keys():
            button = self.buttons[button_name]
            right, left, top, bottom = button.place[0], button.place[0] + button.place[2], button.place[1], button.place[1] + button.place[3]
            if right <= pos[0] <= left and top <= pos[1] <= bottom:
                if button_name == 'start_game':
                    return self.activate_start()
                elif button_name == 'user stats':
                    self.activate_user_stats()
                elif button_name == 'global stats':
                    self.activate_global_stats()
                elif button_name == "linkedin":
                    link = "https://www.linkedin.com/in/ronshrb/"
                    webbrowser.open(link)
                    self.selected_button = button_name
                else:
                    self.selected_button = button_name
        return

    def activate_start(self):
        """
        starts the game
        if the player didn't fill the game number and the level number, fill it randomly
        """
        random_gen = random.Random()
        # if the game number wasn't filled, pick a random number
        if self.buttons["game_number"].value is None:
            self.buttons["game_number"].value = random_gen.randint(1, 1000)
        # if the game difficulty wasn't filled, pick a random number
        if self.buttons["level_number"].value is None:
            self.buttons["level_number"].value = random_gen.randint(1, 10)
        return self.buttons["game_number"].value, self.buttons["level_number"].value, self.buttons["username"].value

    def activate_user_stats(self):
        """
        opens the user statistics window
        """
        stats = UserStats.UserStats(self.user)
        stats.run()

    def activate_global_stats(self):
        """
        opens the global statistics window
        """
        stats = GlobalStats.GlobalStats(self.user)
        stats.run()
    def run(self):
        """
        runs the program
        """
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    result = self.handle_mouse_click(pygame.mouse.get_pos())
                    if result:
                        return result
                elif event.type == pygame.KEYDOWN and self.selected_button:
                    self.handle_key_input(event.key)

            self.screen.fill((255, 255, 255))
            self.draw_title()
            self.draw_rules()
            self.draw_instructions()
            self.draw_buttons()
            self.draw_linkedin()
            self.draw_highlight()
            self.draw_input()
            pygame.display.flip()