import pygame
import sys
import Game
import GameSetup
import LogSheet
from resource_path import resource_path


class EndGame:
    """
        runs the end game window.

        Methods:
            __init__ - initializes display.
            draw_winning_message - shows a winning message in case the player won.
            run - runs the program.
    """
    def __init__(self, finish_time, user, log_id, score):
        """
        initializes display.
        """
        self.finish_time = finish_time
        self.user = user
        self.log_id = log_id
        self.score = score
        self.screen = pygame.display.set_mode((700, 500))
        pygame.display.set_caption("Killer Sudoku")
        icon = pygame.image.load(resource_path("icon.png"))
        pygame.display.set_icon(icon)
        self.table = LogSheet.LogSheet().get_sheet()

    def draw_winning_message(self):
        """
        shows a winning message in case the player won
        """
        background_rect = pygame.Rect(0, 0, self.screen.get_width(), self.screen.get_height())
        pygame.draw.rect(self.screen, (200, 200, 200), background_rect)


        text_font = pygame.font.SysFont("Gisha", 40)
        winning_text = text_font.render(f"Congratulations, you won!", True, (0, 0, 0))
        win_text_rect = winning_text.get_rect(center=(self.screen.get_width() // 2, 80))

        minutes, seconds = self.finish_time.split(':')
        text_font = pygame.font.SysFont("Gisha", 32)
        row2 = text_font.render(
            f"You completed the game in", True,
            (0, 0, 0))
        row2_rect = row2.get_rect(center=(self.screen.get_width() // 2, 150))

        row3 = text_font.render(
            f"{minutes} minutes and {seconds} seconds", True,
            (0, 0, 0))
        row3_rect = row3.get_rect(center=(self.screen.get_width() // 2, 200))

        row4 = text_font.render(
            f"and with {self.score} points!", True,
            (0, 0, 0))
        row4_rect = row4.get_rect(center=(self.screen.get_width() // 2, 250))

        curr_game_log = self.table[self.table['Log ID'] == self.log_id]
        # table without the current game's row, and with the same game number
        other_rows = self.table[self.table['Log ID'] != self.log_id]
        other_rows = other_rows[other_rows['Game Number'] == curr_game_log['Game Number'].iloc[0]]

        number_of_other_games = len(other_rows)
        if number_of_other_games == 0:
            score_percentage = 100

        else:
            # score
            players_score = curr_game_log['Score'].iloc[0]
            # find the number of games that had a lower score
            number_of_rows_under = len(other_rows[other_rows['Score'] < players_score])
            score_percentage = round(number_of_rows_under*100/number_of_other_games,2)

        text_font = pygame.font.SysFont("Gisha", 28)
        row5 = text_font.render(
            f"Your score is higher than {score_percentage}%", True,
            (0, 0, 0))
        row5_rect = row5.get_rect(center=(self.screen.get_width() // 2, 310))

        row6 = text_font.render(
            "of other players scores for this level", True,
            (0, 0, 0))
        row6_rect = row6.get_rect(center=(self.screen.get_width() // 2, 350))

        text_font = pygame.font.SysFont("Gisha", 28)
        row7 = text_font.render(
            f"Start another game by pressing Enter", True,
            (0, 0, 0))
        row7_rect = row7.get_rect(center=(self.screen.get_width() // 2, 410))

        background_rect.inflate_ip(20, 20)
        pygame.draw.rect(self.screen, (255, 255, 255), background_rect)

        self.screen.blit(winning_text, win_text_rect)
        self.screen.blit(row2, row2_rect)
        self.screen.blit(row3, row3_rect)
        self.screen.blit(row4, row4_rect)
        self.screen.blit(row5, row5_rect)
        self.screen.blit(row6, row6_rect)
        self.screen.blit(row7, row7_rect)


    def run(self):
        """
        runs the program
        """
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        setup = GameSetup.GameSetup(self.user)
                        game_number, level, path = setup.run()
                        game = Game.Game(game_number, level,path)
                        game.run()

            self.draw_winning_message()
            pygame.display.flip()