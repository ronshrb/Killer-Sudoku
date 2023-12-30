import pandas as pd
from datetime import datetime as dt
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import random

from resource_path import resource_path


class LogSheet:
    """
    connects to the game log.

    Methods:
        __init__ - sets a connection to the log.
        insert_row - add a new row to the log.
        get_sheet - return the log as a pandas dataframe.
    """

    def __init__(self):
        """
        sets a connection to the log
        """
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            resource_path("killersudoku-82b083edafdc.json"), scope)
        client = gspread.authorize(creds)
        self.sheet = client.open("Killer Sudoku Stats")
        self.global_log = self.sheet.get_worksheet(0)
        records_data = self.global_log.get_all_records()
        self.table = pd.DataFrame.from_dict(records_data)

    def insert_row(self, data):
        """
        add a new row to the log
        """
        if data['User'] == '':  # if the username is empty, assign a random username
            all_users = self.table['User']
            temp_user = f'Player{random.randint(1,999999)}'
            while temp_user in all_users:
                temp_user = f'Player{random.randint(1, 999999)}'
            data['User'] = temp_user

        # add the date to the data
        date_obj = dt.now().date()
        date_string = date_obj.strftime("%Y-%m-%d")
        # day = current_datetime.date()
        data = [date_string] + list(data.values())

        # add a unique key
        if len(self.table) == 0:
            log_id = 1
        else:
            log_id = max(self.table['Log ID']) + 1

        data = [log_id] + data

        # add the data as a row to the google sheets file and update the pandas df
        self.global_log.append_row(data)
        self.global_log = self.sheet.get_worksheet(0)
        records_data = self.global_log.get_all_records()
        self.table = pd.DataFrame.from_dict(records_data)

        return log_id

    def get_sheet(self):
        """
        return the log as a pandas dataframe
        """
        return self.table