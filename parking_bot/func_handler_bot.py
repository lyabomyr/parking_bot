from datetime import timedelta
from datetime import datetime
from parking_bot.init_bots import BotInits
from parking_bot.google_sheet import GoogleSheetClient
from parking_bot.sheet_parser import get_free_parking_lots, get_list_with_all_parking_lots, get_busy_parking_lots_list, get_busy_parking_lots
from config import Config
import logging
from telebot import types


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
        markup = types.ReplyKeyboardRemove(selective=False)
        bot.reply_to(message, 'oooops',reply_markup=markup)

    def time_now(self): 
        return (datetime.utcnow() + timedelta(hours=2)).strftime("%D %H:%M:%S")

    def track_request(self, message, text):
        logging.info(f'Request from user {message.chat.username} on command {text}')

    def status_notification(self,chat_id):
        BotInits().status_bot.send_message(chat_id, get_busy_parking_lots(),parse_mode="HTML")




