from sheet_parser import get_busy_parking_lots, get_free_parking_lots, get_list_with_all_parking_lots, \
    get_busy_parking_lots_list
from parking_bot.google_sheet import GoogleSheetClient
from config import Config, Querry, ColumnName
from mysql_connection.db_connection import get_query_to_pandas, mysql_execute
from func_handler_bot import User, FuncHandBot, SyncData
from parking_bot.init_bots import BotInits
from telebot import types
import logging
from time import sleep
import threading
import regex
from parking_bot.status_parking_bot import status_bot

user_dict = {}
busy_list = None
park_bot = BotInits().parking_telebot()


# status
@park_bot.message_handler(commands=[Config.commands[1]])
def list_reserved_parking_lots(message):
    FuncHandBot().track_request(message, Config.commands[1])
    try:
        resp = get_busy_parking_lots()
        park_bot.reply_to(message, resp, parse_mode="HTML")
    except Exception as e:
        logging.warning(e)
        FuncHandBot().oops_mes(park_bot, message)


# remove_reserve
@park_bot.message_handler(commands=[Config.commands[2]])
def remove_reserve(message):
    FuncHandBot().track_request(message, Config.commands[2])
    user_id = message.from_user.id
    # df = GoogleSheetClient().get_sheet(Config.sheet_key,Config.main_sheet_id)
    df = get_query_to_pandas(Querry.select_reserved_list)
    try:
        if str(user_id) in df[ColumnName.user_id].values.tolist():
            # GoogleSheetClient().remove_row_from_sheet(Config.sheet_key, Config.main_sheet_id, user)
            mysql_execute(Querry().delete_from_reserve(user_id))
            park_bot.reply_to(message,
                              f'You removed reserve from parking lot: *{df.parking_lots[df.user_id == str(user_id)].values.tolist()}*',
                              parse_mode="Markdown")
            FuncHandBot().status_notification(Config.chat_id)
            mysql_execute(Querry.insert_google_flag)
        else:
            park_bot.reply_to(message, 'You can\'t remove if you didn\'t create it')
    except Exception as e:
        logging.warning(e)
        park_bot.reply_to(message, 'You have not reserved parking lots')


# reserve
@park_bot.message_handler(commands=[Config.commands[0]])
def reserve(message):
    print('start reserve')
    try:
        busy_list = get_free_parking_lots()
        if busy_list:
            user_id = (message.from_user.id)
            name = get_query_to_pandas(Querry().select_user_data_table(user_id))[ColumnName.user_name].values.tolist()
            df = get_query_to_pandas(Querry.select_reserved_list)
            if str(user_id) not in df[ColumnName.user_id].values.tolist():
                if name:
                    markup = types.ReplyKeyboardMarkup(row_width=2)
                    for i in busy_list:
                        markup.row(types.KeyboardButton(i))
                    msg = park_bot.reply_to(message,
                                            f'Please select any available  parking lots from the list:  {busy_list}',
                                            reply_markup=markup)
                    park_bot.register_next_step_handler(msg, enter_parking_lots_step)
                else:
                    chat_id = message.chat.id
                    name = f'@{message.chat.username}'
                    FuncHandBot().track_request(message, Config.commands[0])
                    user = User(name)
                    user_dict[chat_id] = user
                    markup = types.ReplyKeyboardRemove(selective=False)
                    msg = park_bot.reply_to(message, 'Please enter your surname!\nUse only Latin!', reply_markup=markup)
                    park_bot.register_next_step_handler(msg, process_surnames_step)
            else:
                park_bot.reply_to(message,
                                  f"You have already reserved parking lot!\nYour parking lot {df.parking_lots[df.user_id == str(user_id)].values.tolist()[0]} ")
        else:
            park_bot.reply_to(message, "All parking lots are already occupied")
    except Exception as e:
        print(e)
        logging.warning(e)
        FuncHandBot().oops_mes(park_bot, message)


def process_surnames_step(message):
    try:
        surname = message.text
        user_id = message.from_user.id
        FuncHandBot().protect_flow(surname)
        if regex.search(r'\p{IsCyrillic}', surname):
            msg = park_bot.reply_to(message, 'Please do not use Cyrillic, use only Latin!')
            park_bot.register_next_step_handler(msg, process_surnames_step)
            return
        mysql_execute(Querry().insert_user_data(user_id, surname))
        busy_list = get_free_parking_lots()
        markup = types.ReplyKeyboardMarkup(row_width=2)
        for i in busy_list:
            markup.row(types.KeyboardButton(i))
        msg = park_bot.reply_to(message, f'Please select any available  parking lots from the list:  {busy_list}',
                                reply_markup=markup)
        park_bot.register_next_step_handler(msg, enter_parking_lots_step)
    except Exception as e:
        print(e)
        logging.warning(e)
        FuncHandBot().oops_mes(park_bot, message)


def enter_parking_lots_step(message):
    try:

        busy_list = get_busy_parking_lots_list()
        user_id = message.from_user.id
        parking_number = message.text
        login_name = f"@{message.from_user.username}"
        surname = get_query_to_pandas(Querry().select_user_data_table(user_id))[ColumnName.user_name].values.tolist()
        FuncHandBot().protect_flow(parking_number)
        if parking_number in busy_list:
            msg = park_bot.reply_to(message, 'This parking lot is already taken')
            park_bot.register_next_step_handler(msg, enter_parking_lots_step)
            return
        elif parking_number not in get_list_with_all_parking_lots():
            msg = park_bot.reply_to(message, 'This parking lot does not exist')
            park_bot.register_next_step_handler(msg, enter_parking_lots_step)
            return
        markup = types.ReplyKeyboardRemove(selective=False)
        # GoogleSheetClient().append_row_to_sheet(Config.sheet_key,Config.main_sheet_id,user.name, user.surname,user.parking_number, FuncHandBot().time_now())
        mysql_execute(
            Querry().insert_reserve(user_id, login_name, surname[0], parking_number, FuncHandBot().time_now()))
        park_bot.reply_to(message,
                          f'Added new booking for parking lot: {parking_number}\nby USER: {login_name},\nwith  SURNAME: {surname[0]} \nIN: {FuncHandBot().time_now()}',
                          reply_markup=markup)
        FuncHandBot().status_notification(Config.chat_id)
        mysql_execute(Querry.insert_google_flag)
    except Exception as e:
        print(e)
        FuncHandBot().oops_mes(park_bot, message)


def park_bot_run():
    print("parking  bot is runing...")
    park_bot.enable_save_next_step_handlers(delay=1)
    park_bot.load_next_step_handlers()
    park_bot.infinity_polling()


def status_bot_run():
    print("status bot runing..")
    status_bot.infinity_polling()


def sync():
    while True:
        if not get_query_to_pandas(Querry.select_google_flag).empty:
            print("sync with google sheet")
            SyncData().sync_available_list()
            SyncData().share_to_google_sheet()
            SyncData().copy_user_data_from_db_to_google()
            mysql_execute(Querry.truncte_google_flag)
            sleep(20)


if __name__ == "__main__":
    threading.Thread(target=park_bot_run).start()
    threading.Thread(target=sync).start()
    threading.Thread(target=status_bot_run).start()
