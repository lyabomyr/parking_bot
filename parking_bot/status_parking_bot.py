import time

time.sleep(10)
import telebot
from config import Config
from sheet_parser import get_busy_parking_lots
from func_handler_bot import FuncHandBot
from parking_bot.init_bots import BotInits
import logging

status_bot = BotInits().status_telebot()


@status_bot.message_handler(commands=[Config.commands[1]])
def list_reserved_parking_lots(message):
    FuncHandBot().track_request(message, Config.commands[0])
    try:
        resp = get_busy_parking_lots()
        print(resp)
        status_bot.reply_to(message, resp, parse_mode="HTML")
    except Exception as e:
        logging.warning(e)
        FuncHandBot().oops_mes(status_bot, message)
