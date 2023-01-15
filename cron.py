from parking_bot.google_sheet import GoogleSheetClient
from config import Config
from parking_bot.func_handler_bot import FuncHandBot


if __name__ == "__main__":
    GoogleSheetClient().clear_sheet(Config.sheet_key, Config.main_sheet_id)
    GoogleSheetClient().create_migration(Config.sheet_key, Config.main_sheet_id)
    FuncHandBot().status_notification(Config.chat_id)

