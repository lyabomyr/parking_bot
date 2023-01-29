import telebot
from config import Config

class BotInits:
    def __init__(self) -> None:
        self.park_bot = telebot.TeleBot(Config.PARKING_BOT_TOKEN)
        self.status_bot = telebot.TeleBot(Config.STATUS_BOT_TOKEN)

    def parking_telebot(self):
        park_bot = self.park_bot
        park_bot = telebot.TeleBot(Config.PARKING_BOT_TOKEN)
        park_bot.delete_my_commands(scope=None, language_code=None)
        park_bot.set_my_commands(commands=[
        telebot.types.BotCommand(Config.commands[0], "Book a parking lot"),
        telebot.types.BotCommand(Config.commands[2], "Delete reserved parking lot"),
        telebot.types.BotCommand(Config.commands[1], "Status parking lots")])
        park_bot.get_my_commands(scope=None, language_code=None)
        return park_bot

    def status_telebot(self):
        status_bot = self.status_bot
        status_bot.set_my_commands(
        commands=[telebot.types.BotCommand(Config.commands[1], "List of reserved parking lots")])
        return status_bot
