import io
import pandas as pd
import plotly.express as px
import plotly.io as pio
import pygame
import sys
from pandasql import sqldf
import Button
import KillerSudoku
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from resource_path import resource_path

class GlobalStats:
    """
        runs the global statistics window.

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
            all_games_plot - draws a scatter plot with the number of minutes the game lasted as the x-axis,
                             the number of moves it took to complete the game as y-axis,
                             game difficulty as the color, and score as the size of the circle.
            avg_chart - draws a bar chart, with difficulty as the x-axis, and time/score/moves as th y-axis.
            leaderboard - draws the leaderboards
            run - runs the program.
        """
    def __init__(self, user):
        """
        initializes display.
        """
        pygame.init()
        self.screen = pygame.display.set_mode((900, 760))
        pygame.display.set_caption("KS - Global Stats")
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
            "1": Button.Button((20, 60, 60, 40), False, (70, 130, 180), pic='1selected.png', selected='1selected.png', unselected='1unselected.png'),
            "2": Button.Button((100, 60, 60, 40), False, (102, 221, 170), pic='2selected.png', selected='2selected.png', unselected='2unselected.png'),
            "3": Button.Button((180, 60, 60, 40), False, (143, 188, 143), pic='3selected.png', selected='3selected.png', unselected='3unselected.png'),
            "4": Button.Button((260, 60, 60, 40), False, (107, 142, 35), pic='4selected.png', selected='4selected.png', unselected='4unselected.png'),
            "5": Button.Button((340, 60, 60, 40), False, (218, 165, 32), pic='5selected.png', selected='5selected.png', unselected='5unselected.png'),
            "6": Button.Button((420, 60, 60, 40), False, (205, 133, 63), pic='6selected.png', selected='6selected.png', unselected='6unselected.png'),
            "7": Button.Button((500, 60, 60, 40), False, (222, 184, 135), pic='7selected.png', selected='7selected.png', unselected='7unselected.png'),
            "8": Button.Button((580, 60, 60, 40), False, (188, 143, 143), pic='8selected.png', selected='8selected.png', unselected='8unselected.png'),
            "9": Button.Button((660, 60, 60, 40), False, (221, 160, 221), pic='9selected.png', selected='9selected.png', unselected='9unselected.png'),
            "10": Button.Button((740, 60, 60, 40), False, (255, 99, 71), pic='10selected.png', selected='10selected.png', unselected='10unselected.png'),
            "All": Button.Button((820, 60, 60, 40), True, (0, 0, 0), pic='allselected.png', selected='allselected.png', unselected='allunselected.png')
        }
        self.all_difficulties = list(set(self.table["Difficulty"]))
        self.selected_difficulties = self.all_difficulties

        if self.buttons['All'].value:
            for button in self.buttons.keys():
                if button in self.all_difficulties and button != 'All':
                    self.buttons[button].value = True

        self.filtered_table = self.table[self.table['Difficulty'].isin(self.selected_difficulties)]

        self.chart_buttons = {
            "Score": Button.Button((30, 520, 110, 40), True, (0, 0, 0), pic='scoreselected.png', selected='scoreselected.png', unselected='scoreunselected.png'),
            "Moves": Button.Button((170, 520, 110, 40), False, (0, 0, 0), pic='movesselected.png', selected='movesselected.png', unselected='movesunselected.png'),
            "Time": Button.Button((310, 520, 110, 40), False, (0, 0, 0), pic='timeselected.png', selected='timeselected.png', unselected='timeunselected.png')}
        self.selected_chart_button = "Score"

    def handle_mouse_click(self, pos):
        """
        takes in the position of where the player clicked and saves it as the selected cell.
        """
        button_names = {
            1: "1",
            2: "2",
            3: "3",
            4: "4",
            5: "5",
            6: "6",
            7: "7",
            8: "8",
            9: "9",
            10: "10",
            11: "All",
            12: "Score",
            13: "Moves",
            14: "Time"
        }
        button_num = 0
        if 120 > pos[1]:
            button_num = (10*pos[0])//800 + 1  # finds the estimated button the player clicked on
        elif pos[1] > 500 and pos[0] < 500:
            button_num = pos[0] // 140 + 12

        if button_num:
            button_name = button_names[button_num]
            if button_num >= 12:  # if the button is one of the chart buttons
                selected_button = self.chart_buttons[button_name]
            else:  # else if it's one of the difficulties
                selected_button = self.buttons[button_name]
            right, left, top, bottom = (selected_button.place[0], selected_button.place[0] + selected_button.place[2],
                                    selected_button.place[1], selected_button.place[1] + selected_button.place[3])
            if right <= pos[0] <= left and top <= pos[1] <= bottom:
                # if the button is the all button and is selected, dont do anything
                if button_num >= 12:  # if the button is one of the chart buttons
                    self.selected_chart_button = button_name
                    # select the button
                    for button_name in self.chart_buttons.keys():
                        if button_name != self.selected_chart_button:
                            self.chart_buttons[button_name].value = False
                        else:
                            self.chart_buttons[button_name].value = True
                else:  # if the button is one of the difficulties
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
            self.filtered_table = self.table[self.table['Difficulty'].isin(self.selected_difficulties)]
    def draw_buttons(self):
        """
        draws the buttons
        """
        all_buttons = list(self.buttons.keys()) + list(self.chart_buttons.keys())
        for button in all_buttons:
            if button in self.buttons.keys():
                curr_dict = self.buttons
            else:
                curr_dict = self.chart_buttons
            curr_button = curr_dict[button]
            if curr_button.value:
                curr_button.pic = curr_button.selected
            else:
                curr_button.pic = curr_button.unselected

            pic = pygame.image.load(f"{resource_path(curr_dict[button].pic)}").convert_alpha()
            self.screen.blit(pic, (curr_dict[button].place[0], curr_dict[button].place[1]))


    def number_of_games_played(self):
        """
        returns the number of games that were played
        """
        return len(self.filtered_table)

    def number_of_games_completed(self):
        """
        returns the number of games that were won
        """
        return len(self.filtered_table[self.filtered_table['Outcome'] == 'win'])

    def number_of_games_quit(self):
        """
        returns the number of games that were lost
        """
        return len(self.filtered_table[self.filtered_table['Outcome'] == 'loss'])

    def convert_time_to_seconds(self, time):
        """
        converts the time value to seconds
        """
        if time != 0:
            converted_time = int(time[:-3])*60 + int(time[-2:])
        else:
            converted_time = 0
        return converted_time

    def convert_time_to_minutes(self, time):
        """
        converts the time value to seconds
        """
        if time != 0:
            converted_time = int(time[:-3])
        else:
            converted_time = 0
        return converted_time

    def draw_title(self):
        """
        draws the title
        """
        text = 'Global Statistics'
        font = pygame.font.SysFont("Gisha", 30)
        title = font.render(text, True, (0, 0, 0))
        text_surface = title.get_rect()
        self.screen.blit(title, (self.screen.get_width() // 2 - text_surface.width // 2, 10))

    def all_games_plot(self):
        """
        draws a scatter plot with the number of minutes the game lasted as the x-axis,
        the number of moves it took to complete the game as y-axis,
        game difficulty as the color, and score as the size of the circle.
        """
        converted_table = self.table.copy()
        converted_table['Minutes'] = converted_table['Time'].apply(self.convert_time_to_minutes)
        converted_table['Difficulty'] = converted_table['Difficulty'].astype(str)

        fig = px.scatter(
            converted_table,
            x="Minutes",
            y="Moves",
            color="Difficulty",
            size='Score',
            color_discrete_map=self.color_map)
        fig.update_layout(
            width=560,
            height=700,
            showlegend=False,
            yaxis=dict(title_standoff=1)
        )

        fig.update_yaxes(range=[60, converted_table['Moves'].max() + 10])

        image_bytes = pio.to_image(fig, format='png')
        plot_surface = pygame.image.load(io.BytesIO(image_bytes))
        self.screen.blit(plot_surface, (420, 90))

        font = pygame.font.SysFont("Gisha", 18)
        text = font.render("Score Distribution", True, (0, 0, 0))
        self.screen.blit(text, (620, 120))
    def avg_chart(self):
        """
        draws a bar chart, with difficulty as the x-axis, and time/score/moves as th y-axis.
        """
        transformed = self.table.copy()
        transformed['Difficulty'] = transformed['Difficulty'].astype(str)
        transformed['Time'] = transformed['Time'].apply(self.convert_time_to_minutes)
        final = transformed.groupby('Difficulty')[self.selected_chart_button].mean().reset_index()

        fig = px.bar(
            final,
            x="Difficulty",
            y=self.selected_chart_button,
            category_orders={"Difficulty": ["1", "2", "3", "4", "5", "6", "7", "8","9","10"]},
            color="Difficulty",
            color_discrete_map=self.color_map,
            height=400)

        fig.update_layout(
            width=500,
            height=300,
            showlegend=False,
            xaxis_title="",
            yaxis_title=""
        )

        image_bytes = pio.to_image(fig, format='png')
        plot_surface = pygame.image.load(io.BytesIO(image_bytes))
        self.screen.blit(plot_surface, (-25, 520))

    def leaderboard(self):
        """
        draws the leaderboards
        """
        leaderboard = self.filtered_table[self.filtered_table["Time"]!=0].copy()
        best_players = leaderboard.groupby("User")["Score"].sum().reset_index()
        best_players = best_players.sort_values(by="Score", ascending=False)
        top_three_players = best_players.head(3)

        font = pygame.font.SysFont("Gisha", 23)
        text = "Top Three Players"
        rendered_text = font.render(text, True, (0, 0, 0))
        self.screen.blit(rendered_text, (140, 120))

        font = pygame.font.SysFont("Gisha", 18)


        places = {
            1: '1st',
            2: '2nd',
            3: '3rd'
        }
        x = 30
        y = 170
        counter = 1
        for index, row in top_three_players.iterrows():
            text = f"{places[counter]} place - {row['User']} with total score of {row['Score']}"
            # text = f"{row['User']} in the {places[counter]} place with a total score of {row['Score']}"
            rendered_text = font.render(text, True, (0, 0, 0))
            self.screen.blit(rendered_text, (x,y))
            y += 40
            counter += 1

        # best_games = leaderboard.groupby("User")["Score"].sum().reset_index()
        best_games = leaderboard.sort_values(by="Score", ascending=False)
        top_three_games = best_games.head(3)

        font = pygame.font.SysFont("Gisha", 23)
        text = "Top Three Scores"
        rendered_text = font.render(text, True, (0, 0, 0))
        self.screen.blit(rendered_text, (140, 300))

        font = pygame.font.SysFont("Gisha", 18)

        counter = 1
        y = 350
        for index, row in top_three_games.iterrows():
            text = f"{places[counter]} place - {row['User']} with a score of {row['Score']}"
            rendered_text = font.render(text, True, (0, 0, 0))
            self.screen.blit(rendered_text, (x,y))
            y += 40
            counter += 1

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
            background_rect = pygame.Rect(0, 0, self.screen.get_width(), self.screen.get_height())
            pygame.draw.rect(self.screen, (255, 255, 255), background_rect)

            self.draw_title()
            self.avg_chart()
            self.all_games_plot()
            self.draw_buttons()
            self.leaderboard()
            pygame.display.flip()
