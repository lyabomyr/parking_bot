from parking_bot.google_sheet import GoogleSheetClient
from config import Config, Querry
from parking_bot.func_handler_bot import FuncHandBot
from mysql_connection.db_connection import mysql_execute



if __name__ == "__main__":
    GoogleSheetClient().clear_sheet(Config.sheet_key, Config.main_sheet_id)
    mysql_execute(Querry.truncate_booking)
    GoogleSheetClient().create_migration(Config.sheet_key, Config.main_sheet_id)
    FuncHandBot().status_notification(Config.chat_id)


