import gspread
from config import Config
import pandas as pd
from gspread_dataframe import set_with_dataframe
import datetime
import os



class GoogleSheetClient():
    def __init__(self) -> None:
        self.service_account_file = Config.service_account_file
        self.google_credentials = gspread.service_account(self.service_account_file)
    def get_sheet(self, sheet_key, sheet_id):
        data = self.google_credentials.open_by_key(sheet_key).get_worksheet(sheet_id).get_all_values()
        if data:
            headers = data.pop(0)
            return pd.DataFrame(data, columns=headers)
        else:
            self.create_migration(sheet_key, sheet_id)
       

    def set_sheet(self,  sheet_key, sheet_id, df):
        set_with_dataframe(self.google_credentials.open_by_key(sheet_key).get_worksheet(sheet_id), df)
        print('updated to\n',df)

    def clear_sheet(self, sheet_key, sheet_id):
        self.google_credentials.open_by_key(sheet_key).get_worksheet(sheet_id).clear()

    def append_row_to_sheet(self,  sheet_key, sheet_id, *row):
        df = self.get_sheet(sheet_key, sheet_id)
        df.loc[len(df.index)] = [*row]
        self.set_sheet(sheet_key, sheet_id, df)
        print('----- added', *row)

    def create_migration(self,  sheet_key, sheet_id):
        data = {"user_name":[], "car_number":[], "booking_place":[]}
        df = pd.DataFrame(data)
        self.set_sheet(sheet_key, sheet_id, df)

    def remove_row_from_sheet(self, sheet_key, sheet_id, place):
        df = self.get_sheet(sheet_key, sheet_id)
        df = df[df.user_name != place]
        self.clear_sheet(sheet_key, sheet_id)
        self.create_migration(sheet_key, sheet_id)
        print(f'Removed row where booking_place != {place}',df)
        self.set_sheet(sheet_key, sheet_id, df)


    
        


