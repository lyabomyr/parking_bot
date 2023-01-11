import telebot
from sheet_parser import get_busy_parking_lots, get_free_parking_lots, get_list_with_all_parking_lots, get_busy_parking_lots_list
from parking_bot.google_sheet import GoogleSheetClient
from config import Config
from datetime import timedelta
from datetime import datetime
from func_handler_bot import User, FuncHandBot
user_dict = {}
bot =  telebot.TeleBot(Config.PARKING_BOT_TOKEN)
bot.delete_my_commands(scope=None, language_code=None)
bot.set_my_commands(commands=[
        telebot.types.BotCommand(Config.commands[0], "Book a parking lot"),
        telebot.types.BotCommand(Config.commands[2], "Delete reserved parking lot")])
cmd = bot.get_my_commands(scope=None, language_code=None)

#remove_reserve
@bot.message_handler(commands= Config.commands[2])
def remove_reserve(message):
    FuncHandBot().track_request(message,Config.commands[2])
    user = f'@{message.chat.username}'
    df = GoogleSheetClient().get_sheet(Config.sheet_key,Config.main_sheet_id)
    try:
        if user in df['user_name'].values.tolist():
            GoogleSheetClient().remove_row_from_sheet(Config.sheet_key, Config.main_sheet_id, user)
            bot.reply_to(message, f'You removed reserve from parking lot: *{df.parking_lots[df.user_name == user].values.tolist()}*', parse_mode="Markdown")
        else:
            bot.reply_to(message, 'You can\'t remove if you didn\'t create it')
    except Exception as e:
        bot.reply_to(message, 'You have not reserved parking lots')

#reserve
@bot.message_handler(commands=Config.commands[0])
def reserve(message):
    try:
        busy_list= get_free_parking_lots()
        if busy_list:
            chat_id = message.chat.id
            name = f'@{message.chat.username}'
            FuncHandBot().track_request(message,Config.commands[0])
            user = User(name)
            user_dict[chat_id] = user
            msg = bot.reply_to(message, 'Please enter your surname!')
            bot.register_next_step_handler(msg, process_surnames_step)
        else:
            bot.reply_to(message, "All parking lots are already occupied")
    except Exception as e:
        FuncHandBot().oops_mes(bot,message)

def process_surnames_step(message):
    try:
        chat_id = message.chat.id
        surname = message.text
        user = user_dict[chat_id]
        FuncHandBot().protect_flow(surname)
        user.surname = surname
        msg = bot.reply_to(message, f'Please select any available  parking lots from the list:  {get_free_parking_lots()}')
        bot.register_next_step_handler(msg, enter_parking_lots_step)
    except Exception as e:
        FuncHandBot().oops_mes(bot,message)


def enter_parking_lots_step(message):
    try:
        chat_id = message.chat.id
        parking_number = message.text
        user = user_dict[chat_id]
        FuncHandBot().protect_flow(parking_number)
        busy_list= get_busy_parking_lots_list()
        if parking_number in busy_list:
            msg = bot.reply_to(message, 'This parking lot is already taken')
            bot.register_next_step_handler(msg, enter_parking_lots_step)
            return
        elif parking_number not in get_list_with_all_parking_lots():
            msg = bot.reply_to(message, 'This parking lot does not exist')
            bot.register_next_step_handler(msg, enter_parking_lots_step)
            return
        user.parking_number = parking_number
        GoogleSheetClient().append_row_to_sheet(Config.sheet_key,Config.main_sheet_id,user.name, user.surname,user.parking_number, FuncHandBot().time_now())
        bot.reply_to(message, f'Added new booking for parking lot: {user.parking_number}\nby USER: {user.name},\nwith  SURNAME: {user.surname} \nIN: {FuncHandBot().time_now()}')
    except Exception as e:
        FuncHandBot().oops_mes(bot,message)


bot.enable_save_next_step_handlers(delay=1)
bot.load_next_step_handlers()
bot.infinity_polling()


