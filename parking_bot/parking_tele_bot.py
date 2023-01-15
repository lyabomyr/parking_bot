from sheet_parser import get_busy_parking_lots, get_free_parking_lots, get_list_with_all_parking_lots, get_busy_parking_lots_list
from parking_bot.google_sheet import GoogleSheetClient
from config import Config
from datetime import timedelta
from datetime import datetime
from func_handler_bot import User, FuncHandBot
from parking_bot.init_bots import BotInits
from telebot import types
import logging

user_dict = {}
busy_list = None
park_bot = BotInits().parking_telebot()





#remove_reserve
@park_bot.message_handler(commands= [Config.commands[2]])
def remove_reserve(message):
    FuncHandBot().track_request(message,Config.commands[2])
    user = f'@{message.chat.username}'
    df = GoogleSheetClient().get_sheet(Config.sheet_key,Config.main_sheet_id)
    try:
        if user in df['user_name'].values.tolist():
            GoogleSheetClient().remove_row_from_sheet(Config.sheet_key, Config.main_sheet_id, user)
            park_bot.reply_to(message, f'You removed reserve from parking lot: *{df.parking_lots[df.user_name == user].values.tolist()}*', parse_mode="Markdown")
            FuncHandBot().status_notification(Config.chat_id)
        else:
            park_bot.reply_to(message, 'You can\'t remove if you didn\'t create it')
    except Exception as e:
        logging.warning(e)
        park_bot.reply_to(message, 'You have not reserved parking lots')

#reserve
@park_bot.message_handler(commands=[Config.commands[0]])
def reserve(message):
    try:
        busy_list = get_free_parking_lots()
        if busy_list:
            chat_id = message.chat.id
            name = f'@{message.chat.username}'
            FuncHandBot().track_request(message,Config.commands[0])
            user = User(name)
            user_dict[chat_id] = user
            markup = types.ReplyKeyboardRemove(selective=False)
            msg = park_bot.reply_to(message, 'Please enter your surname!', reply_markup=markup)
            park_bot.register_next_step_handler(msg, process_surnames_step)
        else:
            park_bot.reply_to(message, "All parking lots are already occupied")
    except Exception as e:
        logging.warning(e)
        FuncHandBot().oops_mes(park_bot,message)

def process_surnames_step(message):
    try:
        chat_id = message.chat.id
        surname = message.text
        user = user_dict[chat_id]
        FuncHandBot().protect_flow(surname)
        user.surname = surname
        busy_list = get_free_parking_lots()
        markup = types.ReplyKeyboardMarkup(row_width=2)
        for i in busy_list:
            markup.row(types.KeyboardButton(i)) 
        msg = park_bot.reply_to(message, f'Please select any available  parking lots from the list:  {busy_list}',reply_markup=markup)
        park_bot.register_next_step_handler(msg, enter_parking_lots_step)
    except Exception as e:
        logging.warning(e)
        FuncHandBot().oops_mes(park_bot,message)


def enter_parking_lots_step(message):
    try:
        busy_list = get_busy_parking_lots_list()
        chat_id = message.chat.id
        parking_number = message.text
        user = user_dict[chat_id]
        FuncHandBot().protect_flow(parking_number)
        if parking_number in busy_list:
            msg = park_bot.reply_to(message, 'This parking lot is already taken')
            park_bot.register_next_step_handler(msg, enter_parking_lots_step)
            return
        elif parking_number not in get_list_with_all_parking_lots():
            msg = park_bot.reply_to(message, 'This parking lot does not exist')
            park_bot.register_next_step_handler(msg, enter_parking_lots_step)
            return
        user.parking_number = parking_number
        markup = types.ReplyKeyboardRemove(selective=False)
        GoogleSheetClient().append_row_to_sheet(Config.sheet_key,Config.main_sheet_id,user.name, user.surname,user.parking_number, FuncHandBot().time_now())
        park_bot.reply_to(message, f'Added new booking for parking lot: {user.parking_number}\nby USER: {user.name},\nwith  SURNAME: {user.surname} \nIN: {FuncHandBot().time_now()}',reply_markup=markup)
        FuncHandBot().status_notification(Config.chat_id)        
    except Exception as e:
        FuncHandBot().oops_mes(park_bot,message)


park_bot.enable_save_next_step_handlers(delay=1)
park_bot.load_next_step_handlers()
park_bot.infinity_polling()


