from datetime import timedelta
from datetime import datetime
from parking_bot.google_sheet import GoogleSheetClient
from sheet_parser import get_free_parking_lots, get_list_with_all_parking_lots, get_busy_parking_lots_list
from config import Config
import logging


class User:
    def __init__(self, name):
        self.name = name
        self.surname = None
        self.parking_number = None

class FuncHandBot:

    def protect_flow(self, message):
        if message.strip()[0]=='/':
                raise Exception

    def oops_mes(self, bot, message):
        bot.reply_to(message, 'oooops')

    def time_now(self): 
        return (datetime.utcnow() + timedelta(hours=2)).strftime("%D %H:%M:%S")

    def track_request(self, message, text):
        logging.info(f'Request from user {message.chat.username} on command {text}')



FuncHandBot().protect_flow('liubomyr')