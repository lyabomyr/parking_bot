import telebot
from config import Config
from sheet_parser import get_busy_parking_lots
from func_handler_bot import FuncHandBot

bot =  telebot.TeleBot(Config.STATUS_BOT_TOKEN)

bot.set_my_commands(
    commands=[telebot.types.BotCommand(Config.commands[1], "List of reserved parking lots")])

@bot.message_handler(commands=Config.commands[1])
def list_reserved_parking_lots(message):
    FuncHandBot().track_request(message,Config.commands[0])
    try: 
        resp = get_busy_parking_lots()
        bot.reply_to(message, resp, parse_mode="HTML")
    except Exception as e:
        bot.reply_to(message, 'oooops')

bot.infinity_polling()


