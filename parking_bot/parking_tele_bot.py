import os
import telebot
from telebot import types
from sheet_parser import get_busy_parking_lots, get_free_parking_lots, get_list_with_all_parking_lots, get_busy_parking_lots_list
from parking_bot.google_sheet import GoogleSheetClient
from config import Config
from datetime import timedelta
from datetime import datetime


user_dict = {}

class User:
    def __init__(self, name):
        self.name = name
        self.surname = None
        self.parking_number = None
    

BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot =  telebot.TeleBot(BOT_TOKEN)

bot.delete_my_commands(scope=None, language_code=None)

bot.set_my_commands(
    commands=[
        telebot.types.BotCommand(Config.commands[0], "Book a parking lot"),
        telebot.types.BotCommand(Config.commands[1], "List of reserved parking lots"),
        telebot.types.BotCommand(Config.commands[2], "Delete reserved parking lot"),
    ],
)
cmd = bot.get_my_commands(scope=None, language_code=None)

#remove_reserve
@bot.message_handler(commands= Config.commands[2])
def remove_reserve(message):
    user = f'@{message.chat.username}'
    df = GoogleSheetClient().get_sheet(Config.sheet_key,Config.main_sheet_id)
    try:
        if f'@{message.chat.username}' in df['user_name'].values.tolist():
            GoogleSheetClient().remove_row_from_sheet(Config.sheet_key, Config.main_sheet_id, user)
            bot.reply_to(message, f'You removed reserve from parking lot: *{df.parking_lots[df.user_name == user].values.tolist()}*', parse_mode="Markdown")
        else:
            bot.reply_to(message, 'You can\'t remove if you didn\'t create it')
    except Exception as e:
        bot.reply_to(message, 'You have not reserved parking lots')


#list reserve parking_lots
@bot.message_handler(commands=Config.commands[1])
def list_reserved_parking_lots(message):
    try: 
        resp = get_busy_parking_lots()
        bot.reply_to(message, resp, parse_mode="HTML")
    except Exception as e:
        bot.reply_to(message, 'oooops')


#reserve
@bot.message_handler(commands=Config.commands[0])
def reserve(message):
    try:
        busy_list= get_free_parking_lots()
        if busy_list:
            print(busy_list)
            chat_id = message.chat.id
            name = f'@{message.chat.username}'
            user = User(name)
            user_dict[chat_id] = user
            msg = bot.reply_to(message, 'Please enter your surname!')
            bot.register_next_step_handler(msg, process_surnames_step)
        else:
            bot.reply_to(message, "All parking lots are already occupied")
    except Exception as e:
        bot.reply_to(message, 'oooops')


def process_surnames_step(message):
    try:
        chat_id = message.chat.id
        surname = message.text
        user = user_dict[chat_id]
        protect_flow(surname)
        user.surname = surname
        msg = bot.reply_to(message, f'Please select any available  parking lots from the list:  {get_free_parking_lots()}')
        bot.register_next_step_handler(msg, enter_parking_lots_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')


def enter_parking_lots_step(message):
    try:
        chat_id = message.chat.id
        parking_number = message.text
        user = user_dict[chat_id]
        busy_list= get_busy_parking_lots_list()
        if parking_number in busy_list:
            msg = bot.reply_to(message, 'This parking lot is already taken')
            bot.register_next_step_handler(msg, enter_parking_lots_step)
            return
        elif parking_number in cmd or parking_number.strip()[0]=='/':
            raise Exception
        elif parking_number not in get_list_with_all_parking_lots():
            msg = bot.reply_to(message, 'This parking lot does not exist')
            bot.register_next_step_handler(msg, enter_parking_lots_step)
            return
        time_now = (datetime.utcnow() + timedelta(hours=2)).strftime("%D %H:%M:%S") 
        user.parking_number = parking_number
        GoogleSheetClient().append_row_to_sheet(Config.sheet_key,Config.main_sheet_id,user.name, user.surname,user.parking_number, time_now)
        bot.reply_to(message, f'Added new booking for parking lot: {user.parking_number}\nby USER: {user.name},\nwith  SURNAME: {user.surname} \nIN: {time_now}')
    except Exception as e:
        bot.reply_to(message, 'oooops')

def protect_flow(message):
    if message.strip()[0]=='/':
            raise Exception







bot.enable_save_next_step_handlers(delay=1)
bot.load_next_step_handlers()
bot.infinity_polling(allowed_updates=telebot.util.update_types)


