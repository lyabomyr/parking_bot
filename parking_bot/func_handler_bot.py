from datetime import timedelta
from datetime import datetime
from parking_bot.init_bots import BotInits
from parking_bot.google_sheet import GoogleSheetClient
from mysql_connection.db_connection import mysql_execute, get_query_to_pandas
from parking_bot.sheet_parser import get_free_parking_lots, get_list_with_all_parking_lots, get_busy_parking_lots_list, \
    get_busy_parking_lots
from config import Config, Querry, ColumnName
import logging
from telebot import types
import pandas as pd


class User:
    def __init__(self, name):
        self.name = name
        self.surname = None
        self.parking_number = None


class FuncHandBot:
    def protect_flow(self, message):
        if message.strip()[0] == '/':
            raise Exception

    def oops_mes(self, bot, message):
        markup = types.ReplyKeyboardRemove(selective=False)
        bot.reply_to(message, 'oooops', reply_markup=markup)

    def time_now(self):
        return (datetime.utcnow() + timedelta(hours=2)).strftime("%D %H:%M:%S")

    def track_request(self, message, text):
        logging.info(f'Request from user {message.chat.username} on command {text}')

    def status_notification(self, chat_id):
        BotInits().status_bot.send_message(chat_id, get_busy_parking_lots(), parse_mode="HTML")


class SyncData:
    def google_available_lots_list(self) -> list:
        resp = GoogleSheetClient().get_sheet(Config.sheet_key, Config.avail_parking_lots_sheet_id)[
            ColumnName.all_parking_places].values.tolist()
        return resp

    def google_reserved_lots(self) -> list:
        return GoogleSheetClient().get_sheet(Config.sheet_key, Config.main_sheet_id)

    def db_available_parking_lots(self):
        return get_query_to_pandas(Querry.select_all_parking_lot)[ColumnName.all_parking_places].values.tolist()

    def db_reserved_lots(self):
        return get_query_to_pandas(Querry.select_reserved_list)

    def sync_available_list(self):
        google_source = self.google_available_lots_list()
        db_source = self.db_available_parking_lots()
        for google_rec in google_source:
            if google_rec not in db_source:
                mysql_execute(Querry.insert_avalots(google_rec))
        for db_rec in db_source:
            if db_rec not in google_source:
                mysql_execute(Querry.delete_from_avalots(db_rec))
        return print('slots number are synced')

    def share_to_google_sheet(self):
        GoogleSheetClient().clear_sheet(Config.sheet_key, Config.main_sheet_id)
        GoogleSheetClient().set_sheet(Config.sheet_key, Config.main_sheet_id, self.db_reserved_lots())

    def copy_reserve_from_google_to_df(self):
        google_df = GoogleSheetClient().get_sheet(Config.sheet_key, Config.main_sheet_id)
        for index, row in google_df.iterrows():
            Querry().insert_reserve(row[ColumnName.user_name], row[ColumnName.surname], row[ColumnName.parking_lots],
                                    row[ColumnName.reservation_time])

    def copy_user_data_from_db_to_google(self):
        GoogleSheetClient().set_sheet(Config.sheet_key, Config.user_data_sheet_id,
                                      get_query_to_pandas(Querry.select_all_user_data))
        print('synced user_data')
