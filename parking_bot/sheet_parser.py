from config import Config
from parking_bot.google_sheet import GoogleSheetClient


def get_list_with_all_parking_lots():
    all_parking_lots = GoogleSheetClient().get_sheet(Config.sheet_key,Config.avail_parking_lots_sheet_id)['all_parking_places'].values.tolist()
    return all_parking_lots

def get_free_parking_lots():
    busy_df = GoogleSheetClient().get_sheet(Config.sheet_key,Config.main_sheet_id)
    busy_df = busy_df['parking_lots']
    if busy_df.empty:
        busy_df=[]
    else:
        busy_df = busy_df.values.tolist()
    all_df =  get_list_with_all_parking_lots()
    free_parking_lots=[]
    for i in all_df:
        if i not in busy_df:
            free_parking_lots.append(i)
    return free_parking_lots

def get_busy_parking_lots_list():
    resp = GoogleSheetClient().get_sheet(Config.sheet_key,Config.main_sheet_id)['parking_lots'].values.tolist()
    return resp

def get_busy_parking_lots():
    free_parking_lots =  get_free_parking_lots()
    resp = GoogleSheetClient().get_sheet(Config.sheet_key,Config.main_sheet_id)
    message=''
    for index, row in resp.iterrows():
        message+= '<b>USER:</b> {}; <b>SURNAME:</b> {}; <b>RESERVE:</b> {};  <b>RESERVATION TIME:</b> {}|\n'.format(row['user_name'], row['surname'], row['parking_lots'], row["reservation_time"])
        print(message)
    if free_parking_lots:
        message+=f'\nFree parking lots: {free_parking_lots} \n\nPlease click on the following link to book: https://t.me/parking_suntech_astarta_bot'
    else:
        message+='There are no free parking lots<'
    return message


