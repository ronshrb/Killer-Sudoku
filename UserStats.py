import io

import pandas as pd
import plotly.express as px
import plotly.io as pio
import pygame
import sys
import Button
import KillerSudoku
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pandasql import sqldf

from resource_path import resource_path



class UserStats:
    """
       runs the user statistics window.

       Methods:
           __init__ - initializes display.
           handle_mouse_click - takes in the position of where the player clicked and saves it as the selected cell.
           draw_buttons - draws the buttons.
           number_of_games_played - returns the number of games that were played.
           number_of_games_completed - returns the number of games that were won.
           number_of_games_quit - returns the number of games that were lost.
           convert_time_to_seconds - converts the time value to seconds.
           convert_time_to_minutes - converts the time value to minutes.
           draw_title - draws the title.
           leaderboard_ranking - grouping by user and finding the average value of the given column for each user.
           draw_main_stats - draws the main written stats.
           draw_stats - draws the written stats.
           win_loss_ratio_chart - draws pie chart of how many the user won and lost.
           games_won_chart - draws a pie chart of how many games were completed for each difficulty.
           total_time_chart - draw a pie chart of how much time was spent on each difficulty.
           last_5_games - draws a bar chart of the last 5 games, the game number as the x-axis, the score as the y-axis and the color as difficulty.
           run - runs the program.
       """
    def __init__(self, user):
        """
        initializes display.
        """
        pygame.init()
        self.screen = pygame.display.set_mode((900, 760))
        pygame.display.set_caption("KS - User Stats")
        icon = pygame.image.load(resource_path("icon.png"))
        pygame.display.set_icon(icon)
        self.user = user

        # data
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(resource_path('killersudoku-82b083edafdc.json'), scope)
        client = gspread.authorize(creds)
        self.sheet = client.open("Killer Sudoku Stats").sheet1
        records_data = self.sheet.get_all_records()
        self.table = pd.DataFrame.from_dict(records_data)
        self.table['Difficulty'] = self.table['Difficulty'].astype(str)
        self.table['Game Number'] = self.table['Game Number'].astype(str)
        self.user_table = self.table.copy()[self.table["User"] == self.user]

        self.color_map = {
            "1": 'steelblue',
            "2": 'mediumaquamarine',
            "3": 'darkseagreen',
            "4": 'olivedrab',
            "5": 'goldenrod',
            "6": 'peru',
            "7": 'burlywood',
            "8": 'rosybrown',
            "9": 'plum',
            "10": 'tomato'}

        self.buttons = {
            "1": Button.Button((20, 60, 60, 40), False, (70, 130, 180), pic='1selected', selected='1selected',
                               unselected='1unselected'),
            "2": Button.Button((100, 60, 60, 40), False, (102, 221, 170), pic='2selected', selected='2selected',
                               unselected='2unselected'),
            "3": Button.Button((180, 60, 60, 40), False, (143, 188, 143), pic='3selected', selected='3selected',
                               unselected='3unselected'),
            "4": Button.Button((260, 60, 60, 40), False, (107, 142, 35), pic='4selected', selected='4selected',
                               unselected='4unselected'),
            "5": Button.Button((340, 60, 60, 40), False, (218, 165, 32), pic='5selected', selected='5selected',
                               unselected='5unselected'),
            "6": Button.Button((420, 60, 60, 40), False, (205, 133, 63), pic='6selected', selected='6selected',
                               unselected='6unselected'),
            "7": Button.Button((500, 60, 60, 40), False, (222, 184, 135), pic='7selected', selected='7selected',
                               unselected='7unselected'),
            "8": Button.Button((580, 60, 60, 40), False, (188, 143, 143), pic='8selected', selected='8selected',
                               unselected='8unselected'),
            "9": Button.Button((660, 60, 60, 40), False, (221, 160, 221), pic='9selected', selected='9selected',
                               unselected='9unselected'),
            "10": Button.Button((740, 60, 60, 40), False, (255, 99, 71), pic='10selected', selected='10selected',
                                unselected='10unselected'),
            "All": Button.Button((820, 60, 60, 40), True, (0, 0, 0), pic='allselected', selected='allselected',
                                 unselected='allselected')
        }

        self.all_difficulties = list(set(self.user_table["Difficulty"]))
        self.selected_difficulties = self.all_difficulties

        if self.buttons['All'].value:
            for button in self.buttons.keys():
                if button in self.all_difficulties and button != 'All':
                    self.buttons[button].value = True

        self.filtered_table = self.table[self.table['Difficulty'].isin(self.selected_difficulties)]
        self.filtered_user_table = self.user_table[self.user_table['Difficulty'].isin(self.selected_difficulties)]

    def handle_mouse_click(self, pos):
        """
        takes in the position of where the player clicked, if the position is on a button, activate the button.
        """
        button_num = (10*pos[0])//800 + 1  # finds the estimated button the player clicked on

        if button_num > 11:
            pass
        else:
            if button_num == 11:
                button_name = 'All'
            else:
                button_name = str(button_num)
            selected_button = self.buttons[button_name]
            right, left, top, bottom = (selected_button.place[0], selected_button.place[0] + selected_button.place[2],
                                        selected_button.place[1], selected_button.place[1] + selected_button.place[3])
            if right <= pos[0] <= left and top <= pos[1] <= bottom:
                # if the button is the all button and is selected, dont do anything
                if self.buttons[button_name].value and button_name == 'All':
                    pass
                # if the button is the all button and is not selected, select it and all the available difficuties
                elif not self.buttons[button_name].value and button_name == 'All':
                    self.buttons['All'].value = True
                    self.selected_difficulties = self.all_difficulties
                    for button in self.all_difficulties:
                        self.buttons[button].value = True
                # if the button is the only one selected dont deselect it by clicking on it
                elif button_name in self.selected_difficulties and len(self.selected_difficulties) == 1:
                    pass
                # if the difficulty isnt an option, dont do anything
                elif button_name not in self.all_difficulties:
                    pass
                else:  # select the button and unselect all other buttons
                    self.selected_difficulties = [button_name]
                    for button in self.buttons.keys():
                        if button == button_name:
                            self.buttons[button].value = True
                        else:
                            self.buttons[button].value = False

        # update the filtered tables
        self.filtered_table = self.table[self.table['Difficulty'].isin(self.selected_difficulties)]
        self.filtered_user_table = self.user_table[self.user_table['Difficulty'].isin(self.selected_difficulties)]

    def draw_buttons(self):
        """
        draws the buttons
        """
        for button in self.buttons.keys():
            curr_button = self.buttons[button]
            if curr_button.value:
                curr_button.pic = curr_button.selected
            else:
                curr_button.pic = curr_button.unselected

            pic = pygame.image.load(f"{resource_path(self.buttons[button].pic)}.png").convert_alpha()
            self.screen.blit(pic, (self.buttons[button].place[0], self.buttons[button].place[1]))


    def number_of_games_played(self, user=True):
        """
        returns the number of games the user played
        """
        if not user:
            result = len(self.filtered_table)
        else:
            result = len(self.filtered_user_table)
        return result

    def number_of_games_won(self, user=True):
        """
        returns the number of games the user won
        """
        if not user:
            result = len(self.filtered_table[self.filtered_table['Outcome'] == 'win'])
        else:
            result = len(self.filtered_user_table[self.filtered_user_table['Outcome'] == 'win'])
        return result

    def number_of_games_lost(self, user=True):
        """
        returns the number of games the user lost
        """
        if not user:
            result = len(self.filtered_table[self.filtered_table['Outcome'] == 'loss'])
        else:
            result = len(self.filtered_user_table[self.filtered_user_table['Outcome'] == 'loss'])
        return result


    def convert_time_to_seconds(self, time):
        """
        converts and returns the time value to seconds
        """
        if time != 0:
            converted_time = int(time[:-3])*60 + int(time[-2:])
        else:
            converted_time = 0
        return converted_time


    def convert_time_to_minutes(self, time):
        """
        converts and returns the time value to minutes
        """
        if time != 0:
            converted_time = int(time[:-3])
        else:
            converted_time = 0
        return converted_time

    def draw_title(self):
        """
        draws the title of the page
        """
        text = 'User Statistics'
        font = pygame.font.SysFont("Gisha", 30)
        title = font.render(text, True, (0, 0, 0))
        text_surface = title.get_rect()
        self.screen.blit(title, (self.screen.get_width() // 2 - text_surface.width // 2, 10))

    def leaderboard_ranking(self, col, table, asc=True):
        """
        grouping by user and finding the average value of the given column for each user
        :param col: string, the name of the column
        :param table: pandas dataframe
        :return: pandas dataframe with average value for each user and their rank
        """
        table_for_sql = table

        if asc:
            order = 'ASC'
        else:
            order = 'DESC'

        query = (
            "SELECT "
            "User, "
            f"AVG({col}) AS avg_val, "
            "COUNT(User) AS rows_count, "
            f"RANK() OVER (ORDER BY AVG({col}) {order}) AS rank "
            "FROM table_for_sql "
            "GROUP BY User;"
        )

        return sqldf(query, locals())

    def draw_main_stats(self):
        """
        draws the main written stats
        """
        # win loss ratio
        games_played = len(self.filtered_user_table)
        if self.number_of_games_lost() == 0:
            ratio = self.number_of_games_won()
        elif self.number_of_games_won() == 0:
            ratio = 1 / self.number_of_games_lost()
        else:
            ratio = self.number_of_games_won() / self.number_of_games_lost()
        # total score
        total_score = sum(self.filtered_user_table['Score'])
        font = pygame.font.SysFont("Gisha", 22)
        text = font.render(f"Win-Loss Ratio: {round(ratio,2)}", True, (0, 0, 0))
        self.screen.blit(text, (40, 135))
        font = pygame.font.SysFont("Gisha", 22)
        text = font.render(f"Games played: {games_played}", True, (0, 0, 0))
        self.screen.blit(text, (250, 135))
        font = pygame.font.SysFont("Gisha", 22)
        text = font.render(f"Total Score: {total_score}", True, (0, 0, 0))
        self.screen.blit(text, (440, 135))
    def draw_stats(self):
        """
        draws the written stats
        """
        table_without_loss = self.filtered_user_table[self.filtered_user_table['Outcome'] == 'win']
        table_for_sql = self.filtered_table.copy()
        table_for_sql = table_for_sql[table_for_sql['Outcome'] == 'win']

        font = pygame.font.SysFont("Gisha", 22)
        # dictionary of cells and their values for the stats table
        stat_table = {
            (0, 1): "Average",
            (0, 2): "Best",
            (0, 3): "Global Rank"
        }

        # time
        # average time
        times_without_loss = table_without_loss['Time']
        total_time = sum([self.convert_time_to_seconds(time) for time in times_without_loss])

        if total_time == 0 or self.number_of_games_won() == 0:
            average_time = 0
        else:
            average_time = total_time // self.number_of_games_won()
        final_average_time = f'{average_time // 60:02d}:{average_time % 60:02d}'

        # top time
        if len(times_without_loss) == 0:
            final_top_time = None
        else:
            top_time = min([self.convert_time_to_seconds(time) for time in times_without_loss])
            final_top_time = f"{top_time // 60:02d}:{top_time % 60:02d}"

        # leaderboard place
        table_for_sql['Seconds'] = table_for_sql['Time'].apply(self.convert_time_to_seconds)

        ranking = self.leaderboard_ranking('Seconds', table_for_sql)
        users_rank = list(ranking[ranking['User'] == self.user]['rank'])[0]

        # add to table dictionary
        stat_table[(1, 0)] = "Time"
        stat_table[(1, 1)] = f'{final_average_time}'
        stat_table[(1, 2)] = f'{final_top_time}'
        stat_table[(1, 3)] = f'         {users_rank}'

        # moves
        # total moves
        total_moves = sum(table_without_loss['Moves'])
        if total_moves == 0:
            average_moves = 0
        else:
            average_moves = total_moves/self.number_of_games_won()

        # min moves
        least_moves = min(table_without_loss['Moves'])

        # global rank
        ranking = self.leaderboard_ranking('Moves', table_for_sql)
        users_rank = list(ranking[ranking['User'] == self.user]['rank'])[0]

        # add to table dictionary
        stat_table[(2, 0)] = "Moves"
        stat_table[(2, 1)] = f'{round(average_moves,2)}'
        stat_table[(2, 2)] = f'{least_moves}'
        stat_table[(2, 3)] = f'         {users_rank}'

        # hints
        # average hints
        total_hints = sum(table_without_loss['Hints'])
        if total_hints == 0:
            average_hints = 0
        else:
            average_hints = total_hints/self.number_of_games_won()

        # least hints
        least_hints = min(table_without_loss['Hints'])

        # global rank
        ranking = self.leaderboard_ranking('Hints', table_for_sql)
        users_rank = list(ranking[ranking['User'] == self.user]['rank'])[0]

        # add to table dictionary
        stat_table[(3, 0)] = "Hints"
        stat_table[(3, 1)] = f'{round(average_hints,2)}'
        stat_table[(3, 2)] = f'{least_hints}'
        stat_table[(3, 3)] = f'         {users_rank}'

        # check board
        # average and least check
        total_checks = sum(table_without_loss['Check Board'])
        if total_checks == 0:
            average_checks = 0
        else:
            average_checks = total_checks / self.number_of_games_won()

        least_checks = min(table_without_loss['Check Board'])

        # global rank
        ranking = self.leaderboard_ranking('"Check Board"', table_for_sql)
        users_rank = list(ranking[ranking['User'] == self.user]['rank'])[0]

        # add to table dictionary
        stat_table[(4, 0)] = "Checks"
        stat_table[(4, 1)] = f'{round(average_checks,2)}'
        stat_table[(4, 2)] = f'{least_checks}'
        stat_table[(4, 3)] = f'         {users_rank}'

        # mistakes
        # average and total mistakes
        total_mistakes = sum(table_without_loss['Mistakes'])
        if total_mistakes == 0:
            average_mistakes = 0
        else:
            average_mistakes = total_mistakes / self.number_of_games_won()

        least_mistakes = min(table_without_loss['Mistakes'])

        # global rank
        ranking = self.leaderboard_ranking('Mistakes', table_for_sql)
        users_rank = list(ranking[ranking['User'] == self.user]['rank'])[0]

        # add to table dictionary
        stat_table[(5, 0)] = "Mistakes"
        stat_table[(5, 1)] = f'{round(average_mistakes, 2)}'
        stat_table[(5, 2)] = f'{least_mistakes}'
        stat_table[(5, 3)] = f'         {users_rank}'

        # score
        # average and top score
        total_score = sum(table_without_loss['Score'])
        if total_score == 0:
            average_score = 0
        else:
            average_score = total_score / self.number_of_games_won()

        top_score = max(table_without_loss['Score'])

        # global rank
        ranking = self.leaderboard_ranking('Score', table_for_sql, asc=False)
        users_rank = list(ranking[ranking['User'] == self.user]['rank'])[0]

        # add to table dictionary
        stat_table[(6, 0)] = "Score"
        stat_table[(6, 1)] = f'{round(average_score, 2)}'
        stat_table[(6, 2)] = f'{top_score}'
        stat_table[(6, 3)] = f'         {users_rank}'

        width = 130
        height = 40

        for row in range(7):
            for col in range(4):
                x = 75 + col * width
                y = 185 + row * height
                pygame.draw.rect(self.screen, (0, 0, 0), (x, y, width, height), 2)
                if (row, col) in stat_table.keys():
                    text = font.render(f"{stat_table[(row, col)]}", True, (0, 0, 0))
                    self.screen.blit(text, (x+5, y+5))

    def win_loss_ratio_chart(self):
        """
        draws pie chart of how many the user won and lost
        """
        # count how many wins and loses the user has
        grouped_by_outcome = self.filtered_user_table.groupby('Outcome').size().reset_index(name='count')

        color_map = {'win': 'darkseagreen', 'loss': 'tomato'}

        fig = px.pie(
            grouped_by_outcome,
            values='count',
            names='Outcome',
            color='Outcome',
            color_discrete_map=color_map
        )

        fig.update_layout(
            width=300,
            height=300,
            showlegend=False
        )

        image_bytes = pio.to_image(fig, format='png')
        plot_surface = pygame.image.load(io.BytesIO(image_bytes))
        self.screen.blit(plot_surface, (630, 80))

        font = pygame.font.SysFont("Gisha", 18)
        text = font.render(f"Games Won and Lost", True, (0, 0, 0))
        self.screen.blit(text, (695, 110))

    def games_won_chart(self):
        """
        draws a pie chart of how many games were completed for each difficulty
        """
        grouped = self.user_table[self.user_table['Outcome'] == 'win'].groupby('Difficulty').size().reset_index(name='count')

        fig = px.pie(
            grouped,
            values='count',
             names='Difficulty',
             color='Difficulty',
             color_discrete_map=self.color_map)

        fig.update_layout(
            width=300,
            height=300,
            showlegend=False
        )

        image_bytes = pio.to_image(fig, format='png')
        plot_surface = pygame.image.load(io.BytesIO(image_bytes))
        self.screen.blit(plot_surface, (630, 290))

        font = pygame.font.SysFont("Gisha", 18)
        text = font.render(f"Games Completed", True, (0, 0, 0))
        self.screen.blit(text, (710, 320))


    def total_time_chart(self):
        """
        draw a pie chart of how much time was spent on each difficulty
        """
        converted_table = self.user_table.copy()
        converted_table['ConvertedTime'] = converted_table['Time'].apply(self.convert_time_to_seconds)

        # group the table by difficulty and sum the time for each difficulty
        grouped = (
            converted_table[converted_table['Time'] != 0]
            .groupby('Difficulty')['ConvertedTime']
            .sum()
            .reset_index()
            .rename(columns={'ConvertedTime': 'sum'})
        )

        fig = px.pie(
            grouped,
            values='sum',
            names='Difficulty',
            color='Difficulty',
            color_discrete_map=self.color_map)

        fig.update_layout(
            width=300,
            height=300,
            showlegend=False
        )

        image_bytes = pio.to_image(fig, format='png')
        plot_surface = pygame.image.load(io.BytesIO(image_bytes))
        self.screen.blit(plot_surface, (630, 520))

        font = pygame.font.SysFont("Gisha", 18)
        text = font.render("Total Time Played", True, (0, 0, 0))
        self.screen.blit(text, (710, 550))

    def last_5_games(self):
        """
        draws a bar chart of the last 5 games, the game number as the x-axis, the score as the y-axis and the color as difficulty.
        """
        last_5_rows = self.filtered_user_table[self.filtered_user_table['Outcome'] == 'win'].tail(5)
        last_5_rows['Log ID'] = last_5_rows['Log ID'].astype(str)

        # fig = px.bar(
        #     last_5_rows,
        #     x="Log ID",
        #     y="Score",
        #     color="Difficulty",
        #     height=400,
        #     color_discrete_map=self.color_map)
        #
        # fig.update_layout(
        #     width=600,
        #     height=300,
        #     showlegend=False
        # )
        fig = px.bar(
            last_5_rows,
            x="Log ID",
            y="Score",
            color="Difficulty",
            height=400,
            color_discrete_map=self.color_map,
            category_orders={"Log ID": last_5_rows["Log ID"].tolist()}  # Set the order of Log ID
        )

        fig.update_layout(
            width=600,
            height=300,
            showlegend=False,
            xaxis=dict(
                tickvals=last_5_rows["Log ID"].tolist(),  # Set tick values to match Log ID
                ticktext=last_5_rows["Game Number"].tolist(),  # Set tick labels to Game Number
            )
        )

        image_bytes = pio.to_image(fig, format='png')
        plot_surface = pygame.image.load(io.BytesIO(image_bytes))
        self.screen.blit(plot_surface, (50, 480))

        font = pygame.font.SysFont("Gisha", 18)
        text = font.render("Last 5 Games", True, (0, 0, 0))
        self.screen.blit(text, (300, 510))

    def run(self):
        """
        runs the program
        """
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    KillerSudoku.main(self.user)
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.handle_mouse_click(pygame.mouse.get_pos())  # get the position where the player clicked on

            # background
            background_rect = pygame.Rect(0, 0, self.screen.get_width(), self.screen.get_height())
            pygame.draw.rect(self.screen, (255, 255, 255), background_rect)

            self.draw_title()
            if len(self.filtered_user_table[self.filtered_user_table['Outcome'] == 'win']) == 0:
                font = pygame.font.SysFont("Gisha", 34)
                text = font.render("This user didn't play or won a game yet", True, (0, 0, 0))
                self.screen.blit(text, (150, self.screen.get_height()//2))
            else:
                self.draw_stats()
                self.last_5_games()
                self.win_loss_ratio_chart()
                self.games_won_chart()
                self.total_time_chart()
            self.draw_buttons()
            self.draw_main_stats()
            pygame.display.flip()