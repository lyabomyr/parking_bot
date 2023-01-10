import os
import telebot
from telebot import types
from sheet_parser import get_busy_places, get_free_places, get_list_with_all_places, get_busy_places_list
from parking_bot.google_sheet import GoogleSheetClient
from config import Config
user_dict = {}

class User:
    def __init__(self, name):
        self.name = name
        self.car_num = None
        self.parking_number = None
    

BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot =  telebot.TeleBot(BOT_TOKEN)

bot.delete_my_commands(scope=None, language_code=None)

bot.set_my_commands(
    commands=[
        telebot.types.BotCommand("reserve", "reserve a parking space"),
        telebot.types.BotCommand("list_reserved_spaces", "List of reserved parking spaces"),
        telebot.types.BotCommand("remove_reserve", "remove reserve")
    ],
)
cmd = bot.get_my_commands(scope=None, language_code=None)

@bot.chat_join_request_handler()
def make_some(message: telebot.types.ChatJoinRequest):
    bot.send_message(message.chat.id, 'I accepted a new user!')
    bot.approve_chat_join_request(message.chat.id, message.from_user.id)

@bot.message_handler(commands='remove_reserve')
def remove_reserve(message):
    user = f'@{message.chat.username}'
    df = GoogleSheetClient().get_sheet(Config.sheet_key,Config.main_sheet_id)
    try:
        if f'@{message.chat.username}' in df['user_name'].values.tolist():
            GoogleSheetClient().remove_row_from_sheet(Config.sheet_key, Config.main_sheet_id, user)
            bot.reply_to(message, f'You removed reserve from places: *{df.booking_place[df.user_name == user].values.tolist()}*', parse_mode="Markdown")
        else:
            bot.reply_to(message, 'You can\'t reserve if you didn\'t create it')
    except Exception as e:
        bot.reply_to(message, 'You have not reserved place')

#list reserve spaces
@bot.message_handler(commands='list_reserved_spaces')
def list_reserved_spaces(message):
    resp = get_busy_places()
    bot.reply_to(message, resp, parse_mode="Markdown")
    

#reserve
@bot.message_handler(commands='reserve')
def reserve(message):

    try:
        busy_list= get_free_places()
        if busy_list:
            print(busy_list)
            chat_id = message.chat.id
            name = f'@{message.chat.username}'
            user = User(name)
            user_dict[chat_id] = user
            msg = bot.reply_to(message, 'Pls input Vehicle registration number!')
            bot.register_next_step_handler(msg, process_car_number_step)
        else:
            bot.reply_to(message, "All places already busy")
    except Exception as e:
        bot.reply_to(message, 'oooops')


def process_car_number_step(message):
    try:
        chat_id = message.chat.id
        car_number = message.text
        user = user_dict[chat_id]
        user.car_num = car_number
        msg = bot.reply_to(message, f'Please enter any free space from list {get_free_places()}')
        bot.register_next_step_handler(msg, enter_parking_place_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')


def enter_parking_place_step(message):
    try:
        chat_id = message.chat.id
        parking_number = message.text
        user = user_dict[chat_id]
        busy_list= get_busy_places_list()
        if parking_number in busy_list:
            print(busy_list)
            msg = bot.reply_to(message, 'This parking space is already taken')
            bot.register_next_step_handler(msg, enter_parking_place_step)
            return
        if parking_number not in get_list_with_all_places():
            msg = bot.reply_to(message, 'This parking space are not exist')
            bot.register_next_step_handler(msg, enter_parking_place_step)
            return
        user.parking_number = parking_number
        print(user.name,'--',user.car_num,'--',user.parking_number)
        GoogleSheetClient().append_row_to_sheet(Config.sheet_key,Config.main_sheet_id,user.name, user.car_num,user.parking_number)
        bot.reply_to(message, f'Added new booking for place: {user.parking_number}\n by USER: {user.name},\n with  Vehicle registration number: {user.car_num}')
    except Exception as e:
        bot.reply_to(message, 'oooops')



bot.enable_save_next_step_handlers(delay=1)
bot.load_next_step_handlers()
bot.infinity_polling(allowed_updates=telebot.util.update_types)


