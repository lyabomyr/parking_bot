from config import Config
from parking_bot.google_sheet import GoogleSheetClient


def get_list_with_all_places():
    all_places = GoogleSheetClient().get_sheet(Config.sheet_key,Config.avail_places_sheet_id)['parking_places'].values.tolist()
    return all_places

def get_free_places():
    busy_df = GoogleSheetClient().get_sheet(Config.sheet_key,Config.main_sheet_id)
    busy_df = busy_df['booking_place']
    if busy_df.empty:
        busy_df=[]
    else:
        busy_df = busy_df.values.tolist()
    all_df =  get_list_with_all_places()
    free_places=[]
    for i in all_df:
        if i not in busy_df:
            free_places.append(i)
    return free_places

def get_busy_places_list():
    resp = GoogleSheetClient().get_sheet(Config.sheet_key,Config.main_sheet_id)['booking_place'].values.tolist()
    return resp

def get_busy_places():
    free_places =  get_free_places()
    resp = GoogleSheetClient().get_sheet(Config.sheet_key,Config.main_sheet_id)
    message=''
    for index, row in resp.iterrows():
        message+= '*USER:* {}; *CAR:* {}; *RESERVE:* {}|\n'.format(row['user_name'], row['car_number'], row['booking_place'])
    if free_places:
        message+=f'Free places: {free_places}'
    else:
        message+='There are no free places'
    return message


