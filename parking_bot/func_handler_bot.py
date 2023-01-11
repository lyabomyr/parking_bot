from datetime import timedelta
from datetime import datetime
from parking_bot.google_sheet import GoogleSheetClient
from sheet_parser import get_free_parking_lots, get_list_with_all_parking_lots, get_busy_parking_lots_list
from config import Config



class User:
    def __init__(self, name):
        self.name = name
        self.surname = None
        self.parking_number = None

class FuncHandlerBot():
    def __init__(self, bot, message):
        self.bot = bot
        self.message = message
        self.name = f'@{message.chat.username}'
        self.user = User(self.name)
        

    def process_surnames_step(self, message):
        try:
            surname = message.text
            if surname.strip()[0]=='/':
                return
            self.user.surname = surname
            msg = self.bot.reply_to(message, f'Please select any available  parking lots from the list:  {get_free_parking_lots()}')
            self.bot.register_next_step_handler(msg, self.enter_parking_lots_step(message))
        except Exception as e:
            print(e)
            self.bot.reply_to(message, 'oooops')
        self.bot.enable_save_next_step_handlers(delay=1)



    def enter_parking_lots_step(self,message):
        try:
            parking_number = message.text
            busy_list= get_busy_parking_lots_list()
            
            if parking_number in busy_list:
                msg = self.bot.reply_to(message, 'This parking lot is already taken')
                self.bot.register_next_step_handler(msg, self.enter_parking_lots_step(message))
                return
            elif parking_number.strip()[0]=='/':
                return
            elif parking_number not in get_list_with_all_parking_lots():
                msg = self.bot.reply_to(message, 'This parking lot does not exist')
                self.bot.register_next_step_handler(msg, self.enter_parking_lots_step(message))
                return
            time_now = (datetime.utcnow() + timedelta(hours=2)).strftime("%D %H:%M:%S") 
            self.user.parking_number = parking_number
            GoogleSheetClient().append_row_to_sheet(Config.sheet_key,Config.main_sheet_id,self.user.name, self.user.surname,self.user.parking_number, time_now)
            self.bot.reply_to(message, f'Added new booking for parking lot: {self.user.parking_number}\nby USER: {self.user.name},\nwith  SURNAME: {self.user.surname} \nIN: {time_now}')
        except Exception as e:
            print(e)
            self.bot.reply_to(message, 'oooops')
        

        # self.bot.enable_save_next_step_handlers(delay=1)
        # self.bot.load_next_step_handlers()
                