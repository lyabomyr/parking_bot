import os

class Config:
    service_account_file = 'booking-parking-place-918d6fcf7e75.json'
    sheet_key='1AaOa3WcdB0qIDVNzeOqxJpSHM9gwYghqhcPnWVlElig'
    main_sheet_id = 0
    avail_parking_lots_sheet_id =1
    commands = ["reserve","list_reserved_parking_lots","remove_reserve"]
    PARKING_BOT_TOKEN = os.environ.get('PARKING_BOT_TOKEN') #'5944821419:AAESYXzxMM942idnIrITlZvkoEBNzQMAKmQ'
    STATUS_BOT_TOKEN =  os.environ.get('STATUS_BOT_TOKEN')  #'5934102533:AAFnDv8G8Of-gyB9YKSPYwGK_-3hb57whwM'
    #chat_id='-565980061' test
    chat_id ='-881152015' #production


